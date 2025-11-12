"""
Vector Database - Sistema de Busca Semântica com Embeddings
Responsável por armazenar e buscar informações usando similaridade vetorial
"""

import json
import pickle
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib
import sqlite3
from contextlib import contextmanager

from analyzer import SemanticAnalyzer

@dataclass
class VectorDocument:
    """Documento armazenado no banco vetorial"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    category: str
    source: str

@dataclass
class SearchResult:
    """Resultado de busca vetorial"""
    document: VectorDocument
    similarity_score: float
    rank: int
    matched_terms: List[str]

class VectorDatabase:
    """Database vetorial para busca semântica"""
    
    def __init__(self, db_path: Optional[Path] = None, cache_size: int = 1000):
        self.db_path = db_path or Path(__file__).parent / "vector_db.sqlite"
        self.cache_size = cache_size
        
        # Componentes
        self.semantic_analyzer = SemanticAnalyzer()
        
        # Cache em memória para performance
        self._vector_cache: Dict[str, np.ndarray] = {}
        self._metadata_cache: Dict[str, Dict[str, Any]] = {}
        
        # Inicialização
        self._init_database()
        self._load_cache()
    
    def _init_database(self):
        """Inicializa o banco de dados SQLite"""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    embedding BLOB,
                    created_at TEXT,
                    updated_at TEXT,
                    tags TEXT,
                    category TEXT,
                    source TEXT
                );
                
                CREATE TABLE IF NOT EXISTS collections (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    document_count INTEGER DEFAULT 0,
                    created_at TEXT
                );
                
                CREATE TABLE IF NOT EXISTS document_collections (
                    document_id TEXT,
                    collection_id TEXT,
                    PRIMARY KEY (document_id, collection_id),
                    FOREIGN KEY (document_id) REFERENCES documents (id),
                    FOREIGN KEY (collection_id) REFERENCES collections (id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_documents_category ON documents (category);
                CREATE INDEX IF NOT EXISTS idx_documents_source ON documents (source);
                CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents (created_at);
            """)
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexão com banco"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add_document(self, content: str, metadata: Dict[str, Any] = None, 
                    tags: List[str] = None, category: str = "general", 
                    source: str = "manual", doc_id: Optional[str] = None) -> str:
        """Adiciona documento ao banco vetorial"""
        
        # Gera ID se não fornecido
        if not doc_id:
            content_hash = hashlib.md5(content.encode()).hexdigest()
            doc_id = f"doc_{content_hash[:12]}"
        
        # Gera embedding
        embedding = self.semantic_analyzer.get_embedding(content)
        if not embedding:
            raise ValueError("Não foi possível gerar embedding para o documento")
        
        # Cria documento
        doc = VectorDocument(
            id=doc_id,
            content=content,
            metadata=metadata or {},
            embedding=embedding,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            tags=tags or [],
            category=category,
            source=source
        )
        
        # Salva no banco
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO documents 
                (id, content, metadata, embedding, created_at, updated_at, tags, category, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc.id,
                doc.content,
                json.dumps(doc.metadata),
                pickle.dumps(embedding),
                doc.created_at.isoformat(),
                doc.updated_at.isoformat(),
                json.dumps(doc.tags),
                doc.category,
                doc.source
            ))
        
        # Atualiza cache
        self._update_cache(doc)
        
        return doc_id
    
    def search(self, query: str, limit: int = 10, category: Optional[str] = None,
               tags: List[str] = None, min_similarity: float = 0.3) -> List[SearchResult]:
        """Busca documentos por similaridade semântica"""
        
        # Gera embedding da query
        query_embedding = self.semantic_analyzer.get_embedding(query)
        if not query_embedding:
            return []
        
        query_vector = np.array(query_embedding)
        
        # Busca documentos no banco
        filters = []
        params = []
        
        if category:
            filters.append("category = ?")
            params.append(category)
        
        if tags:
            # Busca documentos que contenham pelo menos uma das tags
            tag_conditions = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f'%"{tag}"%')
            filters.append(f"({' OR '.join(tag_conditions)})")
        
        where_clause = " AND ".join(filters) if filters else "1=1"
        
        with self._get_connection() as conn:
            cursor = conn.execute(f"""
                SELECT id, content, metadata, embedding, created_at, updated_at, tags, category, source
                FROM documents 
                WHERE {where_clause}
            """, params)
            
            results = []
            for row in cursor.fetchall():
                doc_id, content, metadata_json, embedding_blob, created_at, updated_at, tags_json, cat, src = row
                
                # Deserializa dados
                try:
                    embedding = pickle.loads(embedding_blob)
                    doc_vector = np.array(embedding)
                    
                    # Calcula similaridade
                    similarity = self._cosine_similarity(query_vector, doc_vector)
                    
                    if similarity >= min_similarity:
                        doc = VectorDocument(
                            id=doc_id,
                            content=content,
                            metadata=json.loads(metadata_json),
                            embedding=embedding,
                            created_at=datetime.fromisoformat(created_at),
                            updated_at=datetime.fromisoformat(updated_at),
                            tags=json.loads(tags_json),
                            category=cat,
                            source=src
                        )
                        
                        # Identifica termos coincidentes
                        matched_terms = self._find_matched_terms(query, content)
                        
                        result = SearchResult(
                            document=doc,
                            similarity_score=similarity,
                            rank=0,  # Será atualizado após ordenação
                            matched_terms=matched_terms
                        )
                        results.append(result)
                
                except Exception as e:
                    print(f"Erro ao processar documento {doc_id}: {e}")
                    continue
        
        # Ordena por similaridade e atualiza ranks
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        for i, result in enumerate(results):
            result.rank = i + 1
        
        return results[:limit]
    
    def get_document(self, doc_id: str) -> Optional[VectorDocument]:
        """Obtém documento por ID"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, content, metadata, embedding, created_at, updated_at, tags, category, source
                FROM documents 
                WHERE id = ?
            """, (doc_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            doc_id, content, metadata_json, embedding_blob, created_at, updated_at, tags_json, category, source = row
            
            return VectorDocument(
                id=doc_id,
                content=content,
                metadata=json.loads(metadata_json),
                embedding=pickle.loads(embedding_blob),
                created_at=datetime.fromisoformat(created_at),
                updated_at=datetime.fromisoformat(updated_at),
                tags=json.loads(tags_json),
                category=category,
                source=source
            )
    
    def update_document(self, doc_id: str, content: Optional[str] = None,
                       metadata: Optional[Dict[str, Any]] = None,
                       tags: Optional[List[str]] = None) -> bool:
        """Atualiza documento existente"""
        
        doc = self.get_document(doc_id)
        if not doc:
            return False
        
        # Atualiza campos fornecidos
        if content is not None:
            doc.content = content
            # Regenera embedding se conteúdo mudou
            doc.embedding = self.semantic_analyzer.get_embedding(content)
        
        if metadata is not None:
            doc.metadata.update(metadata)
        
        if tags is not None:
            doc.tags = tags
        
        doc.updated_at = datetime.now()
        
        # Salva no banco
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE documents 
                SET content = ?, metadata = ?, embedding = ?, updated_at = ?, tags = ?
                WHERE id = ?
            """, (
                doc.content,
                json.dumps(doc.metadata),
                pickle.dumps(doc.embedding),
                doc.updated_at.isoformat(),
                json.dumps(doc.tags),
                doc_id
            ))
        
        # Atualiza cache
        self._update_cache(doc)
        
        return True
    
    def delete_document(self, doc_id: str) -> bool:
        """Remove documento do banco"""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            
            if cursor.rowcount > 0:
                # Remove do cache
                self._vector_cache.pop(doc_id, None)
                self._metadata_cache.pop(doc_id, None)
                return True
        
        return False
    
    def create_collection(self, collection_id: str, name: str, description: str = "") -> bool:
        """Cria nova coleção de documentos"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO collections (id, name, description, document_count, created_at)
                    VALUES (?, ?, ?, 0, ?)
                """, (collection_id, name, description, datetime.now().isoformat()))
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_to_collection(self, doc_id: str, collection_id: str) -> bool:
        """Adiciona documento a uma coleção"""
        try:
            with self._get_connection() as conn:
                # Adiciona à tabela de relacionamento
                conn.execute("""
                    INSERT OR IGNORE INTO document_collections (document_id, collection_id)
                    VALUES (?, ?)
                """, (doc_id, collection_id))
                
                # Atualiza contador da coleção
                conn.execute("""
                    UPDATE collections 
                    SET document_count = (
                        SELECT COUNT(*) FROM document_collections 
                        WHERE collection_id = ?
                    )
                    WHERE id = ?
                """, (collection_id, collection_id))
            
            return True
        except Exception:
            return False
    
    def get_collection_documents(self, collection_id: str) -> List[VectorDocument]:
        """Obtém todos os documentos de uma coleção"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT d.id, d.content, d.metadata, d.embedding, d.created_at, 
                       d.updated_at, d.tags, d.category, d.source
                FROM documents d
                JOIN document_collections dc ON d.id = dc.document_id
                WHERE dc.collection_id = ?
            """, (collection_id,))
            
            documents = []
            for row in cursor.fetchall():
                doc_id, content, metadata_json, embedding_blob, created_at, updated_at, tags_json, category, source = row
                
                doc = VectorDocument(
                    id=doc_id,
                    content=content,
                    metadata=json.loads(metadata_json),
                    embedding=pickle.loads(embedding_blob),
                    created_at=datetime.fromisoformat(created_at),
                    updated_at=datetime.fromisoformat(updated_at),
                    tags=json.loads(tags_json),
                    category=category,
                    source=source
                )
                documents.append(doc)
        
        return documents
    
    def find_similar_documents(self, doc_id: str, limit: int = 5) -> List[SearchResult]:
        """Encontra documentos similares a um documento existente"""
        doc = self.get_document(doc_id)
        if not doc:
            return []
        
        return self.search(doc.content, limit=limit + 1)  # +1 porque excluiremos o próprio doc
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtém estatísticas do banco vetorial"""
        with self._get_connection() as conn:
            # Total de documentos
            total_docs = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            
            # Documentos por categoria
            category_counts = dict(conn.execute("""
                SELECT category, COUNT(*) FROM documents GROUP BY category
            """).fetchall())
            
            # Documentos por fonte
            source_counts = dict(conn.execute("""
                SELECT source, COUNT(*) FROM documents GROUP BY source
            """).fetchall())
            
            # Total de coleções
            total_collections = conn.execute("SELECT COUNT(*) FROM collections").fetchone()[0]
            
            # Documentos mais recentes
            recent_docs = conn.execute("""
                SELECT id, content, created_at FROM documents 
                ORDER BY created_at DESC LIMIT 5
            """).fetchall()
        
        return {
            'total_documents': total_docs,
            'total_collections': total_collections,
            'documents_by_category': category_counts,
            'documents_by_source': source_counts,
            'recent_documents': [
                {'id': doc_id, 'preview': content[:100], 'created_at': created_at}
                for doc_id, content, created_at in recent_docs
            ],
            'cache_size': len(self._vector_cache)
        }
    
    def bulk_add_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """Adiciona múltiplos documentos em lote"""
        doc_ids = []
        
        for doc_data in documents:
            try:
                doc_id = self.add_document(
                    content=doc_data['content'],
                    metadata=doc_data.get('metadata', {}),
                    tags=doc_data.get('tags', []),
                    category=doc_data.get('category', 'general'),
                    source=doc_data.get('source', 'bulk_import'),
                    doc_id=doc_data.get('id')
                )
                doc_ids.append(doc_id)
            except Exception as e:
                print(f"Erro ao adicionar documento: {e}")
                continue
        
        return doc_ids
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcula similaridade do cosseno entre dois vetores"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _find_matched_terms(self, query: str, content: str) -> List[str]:
        """Encontra termos em comum entre query e conteúdo"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        # Remove palavras muito curtas e stopwords
        stopwords = {'de', 'da', 'do', 'que', 'e', 'o', 'a', 'em', 'para', 'com'}
        
        matched = []
        for word in query_words.intersection(content_words):
            if len(word) > 2 and word not in stopwords:
                matched.append(word)
        
        return matched[:5]  # Máximo 5 termos
    
    def _update_cache(self, doc: VectorDocument):
        """Atualiza cache em memória"""
        # Remove item mais antigo se cache está cheio
        if len(self._vector_cache) >= self.cache_size:
            oldest_key = next(iter(self._vector_cache))
            self._vector_cache.pop(oldest_key)
            self._metadata_cache.pop(oldest_key, None)
        
        self._vector_cache[doc.id] = np.array(doc.embedding)
        self._metadata_cache[doc.id] = {
            'content_preview': doc.content[:100],
            'category': doc.category,
            'tags': doc.tags,
            'created_at': doc.created_at.isoformat()
        }
    
    def _load_cache(self):
        """Carrega documentos mais acessados no cache"""
        with self._get_connection() as conn:
            # Carrega os documentos mais recentes
            cursor = conn.execute("""
                SELECT id, embedding, content, category, tags, created_at
                FROM documents 
                ORDER BY updated_at DESC 
                LIMIT ?
            """, (min(self.cache_size, 100),))
            
            for row in cursor.fetchall():
                doc_id, embedding_blob, content, category, tags_json, created_at = row
                
                try:
                    embedding = pickle.loads(embedding_blob)
                    self._vector_cache[doc_id] = np.array(embedding)
                    self._metadata_cache[doc_id] = {
                        'content_preview': content[:100],
                        'category': category,
                        'tags': json.loads(tags_json),
                        'created_at': created_at
                    }
                except Exception:
                    continue


# Função utilitária para popular banco com dados do projeto
def populate_with_on_project_data(vector_db: VectorDatabase, project_root: Path):
    """Popula banco vetorial com dados do projeto On"""
    
    documents_to_add = []
    
    # Adiciona READMEs dos agentes
    agents_dir = project_root / "agents"
    if agents_dir.exists():
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                readme_path = agent_dir / "README.md"
                if readme_path.exists():
                    content = readme_path.read_text(encoding='utf-8')
                    documents_to_add.append({
                        'id': f"agent_readme_{agent_dir.name}",
                        'content': content,
                        'metadata': {'agent_name': agent_dir.name, 'type': 'agent_documentation'},
                        'tags': ['agent', 'documentation', agent_dir.name],
                        'category': 'agent_docs',
                        'source': 'project_files'
                    })
    
    # Adiciona documentos do core
    core_files = [
        'on_core.py', 'on_bus.py', 'on_message.py', 'on_scheduler.py', 
        'on_storage.py', 'on_telemetry.py'
    ]
    
    core_dir = project_root / "core"
    for file_name in core_files:
        file_path = core_dir / file_name
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            # Extrai docstring principal
            lines = content.split('\n')
            docstring_lines = []
            in_docstring = False
            for line in lines:
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    if in_docstring:
                        break
                    in_docstring = True
                    continue
                if in_docstring:
                    docstring_lines.append(line)
            
            docstring = '\n'.join(docstring_lines) if docstring_lines else content[:500]
            
            documents_to_add.append({
                'id': f"core_{file_name.replace('.py', '')}",
                'content': docstring,
                'metadata': {'file_name': file_name, 'type': 'core_module'},
                'tags': ['core', 'module', file_name.replace('.py', '')],
                'category': 'core_docs',
                'source': 'project_files'
            })
    
    # Adiciona conhecimento base sobre o sistema
    system_knowledge = [
        {
            'content': "Sistema On é uma plataforma de agentes autônomos especializada em diferentes áreas de negócio. Os agentes trabalham de forma colaborativa usando inteligência artificial para automatizar tarefas corporativas.",
            'tags': ['sistema', 'overview', 'agentes'],
            'category': 'knowledge_base'
        },
        {
            'content': "Atlas é o agente especializado em estratégia e conhecimento corporativo. Responsável por sustentar a base operacional e fornecer insights estratégicos para a empresa.",
            'tags': ['atlas', 'estrategia', 'corporativo'],
            'category': 'agent_knowledge'
        },
        {
            'content': "Helix é o agente técnico especializado em engenharia e DevOps. Responsável pela automação técnica e manutenção da infraestrutura do sistema.",
            'tags': ['helix', 'tecnico', 'devops'],
            'category': 'agent_knowledge'
        }
    ]
    
    for i, knowledge in enumerate(system_knowledge):
        documents_to_add.append({
            'id': f"knowledge_{i}",
            'content': knowledge['content'],
            'metadata': {'type': 'knowledge_base'},
            'tags': knowledge['tags'],
            'category': knowledge['category'],
            'source': 'system_knowledge'
        })
    
    # Adiciona todos os documentos
    doc_ids = vector_db.bulk_add_documents(documents_to_add)
    print(f"Adicionados {len(doc_ids)} documentos ao banco vetorial")
    
    return doc_ids


# Exemplo de uso
if __name__ == "__main__":
    vector_db = VectorDatabase()
    
    # Exemplo: adiciona documentos de teste
    test_docs = [
        {
            'content': "O agente Atlas é responsável pela estratégia corporativa e análise de dados. Ele mantém a base de conhecimento da empresa e fornece insights estratégicos.",
            'tags': ['atlas', 'estrategia', 'dados'],
            'category': 'agent_info'
        },
        {
            'content': "O sistema de telemetria coleta métricas de performance dos agentes usando OpenTelemetry. As métricas são enviadas para Prometheus e visualizadas no Grafana.",
            'tags': ['telemetria', 'metricas', 'prometheus'],
            'category': 'technical_info'
        },
        {
            'content': "Para resolver problemas de performance na API, primeiro verificar os logs, depois analisar as métricas de resposta no Grafana e identificar gargalos.",
            'tags': ['performance', 'api', 'troubleshooting'],
            'category': 'procedures'
        }
    ]
    
    # Adiciona documentos
    doc_ids = vector_db.bulk_add_documents(test_docs)
    print(f"Documentos adicionados: {doc_ids}")
    
    # Busca semântica
    results = vector_db.search("Como resolver problemas de performance?", limit=3)
    
    print("\n=== RESULTADOS DA BUSCA ===")
    for result in results:
        print(f"\nRank {result.rank} (similaridade: {result.similarity_score:.2f})")
        print(f"Conteúdo: {result.document.content}")
        print(f"Categoria: {result.document.category}")
        print(f"Tags: {result.document.tags}")
        print(f"Termos coincidentes: {result.matched_terms}")
    
    # Estatísticas
    stats = vector_db.get_statistics()
    print(f"\n=== ESTATÍSTICAS ===")
    print(f"Total de documentos: {stats['total_documents']}")
    print(f"Documentos por categoria: {stats['documents_by_category']}")
    print(f"Cache size: {stats['cache_size']}")