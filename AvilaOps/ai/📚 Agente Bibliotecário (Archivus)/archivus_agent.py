#!/usr/bin/env python3
"""
Archivus - Agente Bibliotecário com RAG
Sistema de indexação e consulta semântica para documentação Ávila
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

try:
    import chromadb
    from chromadb.utils import embedding_functions
except ImportError:
    print("⚠️ ChromaDB não instalado. Execute: pip install chromadb")
    chromadb = None

@dataclass
class Document:
    """Documento indexado"""
    doc_id: str
    content: str
    metadata: Dict
    source: str
    indexed_at: str

class ArchivusAgent:
    """
    Agente Archivus - Sistema RAG para documentação
    """
    
    def __init__(self, db_path: str = "./vector_store/chromadb"):
        """
        Inicializa Archivus com ChromaDB
        
        Args:
            db_path: Caminho para armazenamento do vector store
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        if chromadb is None:
            raise RuntimeError("ChromaDB é obrigatório para Archivus")

        self._load_env_vars()
        
        # Cliente ChromaDB persistente
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Embedding function (OpenAI text-embedding-3-large por padrão)
        openai_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = "text-embedding-3-large"
        if openai_key:
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=openai_key,
                model_name="text-embedding-3-large"
            )
        else:
            print("⚠️ OPENAI_API_KEY não configurada. Usando SentenceTransformer local (all-MiniLM-L6-v2).")
            try:
                self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
                self.embedding_model = "all-MiniLM-L6-v2"
            except Exception as exc:
                raise RuntimeError(
                    "SentenceTransformerEmbeddingFunction indisponível. Execute: pip install sentence-transformers"
                ) from exc
        
        # Coleção de documentos
        self.collection = self.client.get_or_create_collection(
            name="avila_docs",
            embedding_function=self.embedding_fn,
            metadata={"description": "Documentação Ávila (produtos, governance, analytics)"}
        )
        
        print(f"✅ Archivus inicializado | Documentos indexados: {self.collection.count()}")
    
    def index_directory(self, dir_path: Path, category: str, file_extensions: List[str] = [".md", ".txt"]) -> Dict[str, int]:
        """
        Indexa todos os arquivos de um diretório
        
        Args:
            dir_path: Caminho do diretório
            category: Categoria (products, governance, analytics, architecture)
            file_extensions: Extensões de arquivo para indexar
        """
        if not dir_path.exists():
            print(f"❌ Diretório não encontrado: {dir_path}")
            return
        
        indexed_count = 0
        total_chunks = 0
        for file_path in dir_path.rglob("*"):
            if file_path.suffix in file_extensions and file_path.is_file():
                try:
                    chunks_added = self.index_file(file_path, category)
                    total_chunks += chunks_added
                    indexed_count += 1
                except Exception as e:
                    print(f"⚠️ Erro ao indexar {file_path.name}: {e}")
        
        print(f"✅ Indexados {indexed_count} arquivos de {category}")
        return {"total_files": indexed_count, "total_chunks": total_chunks}
    
    def index_file(self, file_path: Path, category: str) -> int:
        """
        Indexa um arquivo individual
        
        Args:
            file_path: Caminho do arquivo
            category: Categoria do documento
        """
        content = file_path.read_text(encoding="utf-8")
        
        # Chunking simples (500 caracteres com overlap de 50)
        chunks = self._chunk_text(content, chunk_size=500, overlap=50)
        
        doc_id_base = f"{category}_{file_path.stem}"
        
        for idx, chunk in enumerate(chunks):
            doc_id = f"{doc_id_base}_chunk{idx}"
            
            metadata = {
                "category": category,
                "filename": file_path.name,
                "chunk_index": idx,
                "total_chunks": len(chunks),
                "indexed_at": datetime.now().isoformat()
            }
            
            self.collection.add(
                ids=[doc_id],
                documents=[chunk],
                metadatas=[metadata]
            )
        return len(chunks)
    
    def query(self, question: str, top_k: int = 5, category_filter: Optional[str] = None) -> List[Dict]:
        """
        Consulta semântica na base de conhecimento
        
        Args:
            question: Pergunta em linguagem natural
            top_k: Número de resultados
            category_filter: Filtrar por categoria (products, governance, etc.)
        
        Returns:
            Lista de documentos relevantes
        """
        where_filter = {"category": category_filter} if category_filter else None
        
        results = self.collection.query(
            query_texts=[question],
            n_results=top_k,
            where=where_filter
        )
        
        # Formata resultados
        formatted_results = []
        if results and results['documents']:
            for idx in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][idx],
                    "metadata": results['metadatas'][0][idx],
                    "distance": results['distances'][0][idx] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_context_for_agent(self, question: str, max_tokens: int = 2000) -> str:
        """
        Retorna contexto formatado para injection em prompt de agente
        
        Args:
            question: Pergunta do agente
            max_tokens: Limite de tokens de contexto
        
        Returns:
            Contexto formatado em markdown
        """
        results = self.query(question, top_k=5)
        
        if not results:
            return "⚠️ Nenhum documento relevante encontrado."
        
        context_parts = ["## 📚 Contexto de Archivus\n"]
        
        for idx, result in enumerate(results, 1):
            meta = result['metadata']
            context_parts.append(
                f"### Fonte {idx}: {meta['filename']} ({meta['category']})\n"
                f"{result['content']}\n"
            )
        
        full_context = "\n".join(context_parts)
        
        # Trunca se necessário (aproximado)
        if len(full_context) > max_tokens * 4:  # ~4 chars/token
            full_context = full_context[:max_tokens * 4] + "\n\n[...truncado]"
        
        return full_context
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Divide texto em chunks com overlap
        
        Args:
            text: Texto completo
            chunk_size: Tamanho do chunk em caracteres
            overlap: Overlap entre chunks
        
        Returns:
            Lista de chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Tenta terminar em quebra de linha ou espaço
            if end < len(text):
                last_newline = chunk.rfind('\n')
                last_space = chunk.rfind(' ')
                if last_newline > chunk_size * 0.7:
                    end = start + last_newline
                elif last_space > chunk_size * 0.7:
                    end = start + last_space
            
            chunks.append(text[start:end].strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Remove vazios
    
    def stats(self) -> Dict:
        """Retorna estatísticas do índice"""
        return {
            "total_documents": self.collection.count(),
            "db_path": str(self.db_path),
            "embedding_model": self.embedding_model
        }

    def _load_env_vars(self) -> None:
        """Carrega variáveis definidas em arquivos .env sem depender de python-dotenv."""
        candidate_paths = [
            Path(__file__).with_name(".env"),
            Path(__file__).resolve().parent.parent / ".env",
            Path(__file__).resolve().parent.parent.parent / ".env",
            Path.cwd() / ".env",
        ]

        for env_path in candidate_paths:
            if not env_path or not env_path.exists():
                continue
            try:
                for raw_line in env_path.read_text(encoding="utf-8").splitlines():
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    cleaned_key = key.strip()
                    if not cleaned_key:
                        continue
                    cleaned_value = value.strip().strip("'").strip('"')
                    os.environ.setdefault(cleaned_key, cleaned_value)
            except Exception as exc:
                print(f"⚠️ Não foi possível carregar variáveis de {env_path}: {exc}")


def main():
    """Exemplo de uso"""
    
    # Inicializa Archivus
    archivus = ArchivusAgent(db_path="./vector_store/chromadb")
    
    # Indexa documentação (exemplo)
    repo_root = Path(__file__).resolve().parents[2]
    
    # Indexa produtos
    products_path = repo_root / "docs" / "products"
    if products_path.exists():
        archivus.index_directory(products_path, category="products")
    
    # Indexa filosofia/arquitetura
    arch_path = repo_root / "docs" / "AVILA_PHILOSOPHY_AND_ARCHITECTURE.md"
    if arch_path.exists():
        archivus.index_file(arch_path, category="architecture")
    
    # Estatísticas
    print("\n📊 Estatísticas:")
    print(json.dumps(archivus.stats(), indent=2))
    
    # Consulta de exemplo
    print("\n🔍 Consulta: Como coletar GPS com compliance LGPD?")
    context = archivus.get_context_for_agent(
        "Como coletar dados de GPS com compliance LGPD?"
    )
    print(context)


if __name__ == "__main__":
    main()
