#!/usr/bin/env python3
"""
Script para indexar toda documentação Ávila no Archivus RAG
Sincroniza: Setup/, Docs/, AvilaInc/, AvilaOps/ → ChromaDB
"""

import sys
from pathlib import Path

# Adicionar caminho do Archivus
archivus_path = Path(__file__).parent / "📚 Agente Bibliotecário (Archivus)"
sys.path.insert(0, str(archivus_path))

from archivus_agent import ArchivusAgent

def main():
    print("=" * 60)
    print("🔄 SINCRONIZAÇÃO ARCHIVUS - DOCUMENTAÇÃO COMPLETA ÁVILA")
    print("=" * 60)
    
    # Inicializar Archivus
    archivus = ArchivusAgent()
    
    # Diretórios para indexar
    data_dir = archivus_path / "data"
    
    directories = [
        (data_dir / "setup", "Configuração e Setup do ambiente", "setup"),
        (data_dir, "Documentação principal", "archivus-data"),
        (Path(__file__).resolve().parents[1] / "docs" / "products", "Portfólio de Produtos", "products"),
    ]
    
    total_files = 0
    total_chunks = 0
    
    for directory, description, category in directories:
        if not directory.exists():
            print(f"⚠️  Pulando {directory} (não existe)")
            continue
            
        print(f"\n📂 Indexando: {description}")
        print(f"   Caminho: {directory}")
        
        result = archivus.index_directory(directory, category)
        
        files_count = result.get('total_files', 0)
        chunks_count = result.get('total_chunks', 0)
        
        total_files += files_count
        total_chunks += chunks_count
        
        print(f"   ✅ {files_count} arquivos, {chunks_count} chunks")
    
    print("\n" + "=" * 60)
    print(f"✅ INDEXAÇÃO CONCLUÍDA")
    print(f"   📄 Total de arquivos: {total_files}")
    print(f"   🧩 Total de chunks: {total_chunks}")
    print("=" * 60)
    
    # Teste de query
    print("\n🔍 Teste de busca: 'configuração GitHub Copilot'")
    results = archivus.query("configuração GitHub Copilot", top_k=3)
    
    print(f"\n📊 Resultados encontrados: {len(results)}")
    for i, item in enumerate(results, 1):
        meta = item.get('metadata', {})
        source = meta.get('filename', 'desconhecido')
        distance = item.get('distance')
        relevance = 1 - distance if distance is not None else None
        relevance_str = f"{relevance:.2%}" if relevance is not None else "n/d"
        preview = item.get('content', '')[:150]
        print(f"\n{i}. {source}")
        print(f"   Relevância: {relevance_str}")
        print(f"   Trecho: {preview}...")

if __name__ == "__main__":
    main()
