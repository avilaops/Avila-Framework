#!/usr/bin/env python3
"""
SISTEMA DE GESTÃO DE CONHECIMENTO - OBSIDIAN VAULT
===================================================

Orquestrador inteligente que:
1. Analisa o vault Obsidian
2. Remove duplicatas
3. Categoriza conteúdo
4. Gera clusters hierárquicos
5. Cria grafo de conhecimento
6. Produz prompts contextuais atualizados

Autor: Sistema Automatizado
Data: 2025-11-10
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import yaml
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Carregar variáveis de ambiente
load_dotenv()

# Importar módulos do sistema
from modules.orchestrator import KnowledgeOrchestrator
from modules.utils import setup_logging, create_directory_structure


class KnowledgeManager:
    """Gerenciador principal do sistema"""

    def __init__(self, config_path: str = None):
        """
        Inicializa o gerenciador

        Args:
            config_path: Caminho para o arquivo de configuração
        """
        # Carregar configuração
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Expandir variáveis de ambiente
        self._expand_env_vars()

        # Setup logging
        self.logger = setup_logging(self.config)

        # Criar estrutura de diretórios
        self.vault_root = Path(self.config['paths']['vault_root'])
        create_directory_structure(self.vault_root, self.config)

        # Inicializar orquestrador
        self.orchestrator = KnowledgeOrchestrator(self.config, self.logger)

        self.logger.info("=== Sistema de Gestão de Conhecimento Iniciado ===")

    def _expand_env_vars(self):
        """Expande variáveis de ambiente na configuração"""
        def expand(obj):
            if isinstance(obj, dict):
                return {k: expand(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [expand(item) for item in obj]
            elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)
            return obj

        self.config = expand(self.config)

    def run_full_pipeline(self):
        """Executa o pipeline completo de análise"""
        self.logger.info("\n" + "="*60)
        self.logger.info("INICIANDO PROCESSAMENTO COMPLETO")
        self.logger.info("="*60 + "\n")

        try:
            # 1. Coletar arquivos
            self.logger.info("📁 [1/7] Coletando arquivos do vault...")
            files = self.orchestrator.collect_files()
            self.logger.info(f"   ✓ {len(files)} arquivos encontrados\n")

            # 2. Processar conteúdo
            self.logger.info("📄 [2/7] Processando conteúdo dos arquivos...")
            documents = self.orchestrator.process_files(files)
            self.logger.info(f"   ✓ {len(documents)} documentos processados\n")

            # 3. Detectar duplicatas
            self.logger.info("🔍 [3/7] Detectando duplicatas...")
            duplicates = self.orchestrator.detect_duplicates(documents)
            self.logger.info(f"   ✓ {len(duplicates)} duplicatas encontradas\n")

            # 4. Categorizar
            self.logger.info("🏷️  [4/7] Categorizando documentos...")
            categorized = self.orchestrator.categorize_documents(documents)
            self.logger.info(f"   ✓ Documentos categorizados\n")

            # 5. Criar clusters
            self.logger.info("🗂️  [5/7] Gerando clusters hierárquicos...")
            clusters = self.orchestrator.create_clusters(categorized)
            self.logger.info(f"   ✓ {len(clusters)} clusters criados\n")

            # 6. Gerar grafo
            self.logger.info("🕸️  [6/7] Construindo grafo de conhecimento...")
            graph = self.orchestrator.build_knowledge_graph(categorized, clusters)
            self.logger.info(f"   ✓ Grafo gerado com {graph['nodes']} nós\n")

            # 7. Gerar prompts contextuais
            self.logger.info("✨ [7/7] Gerando prompts contextuais...")
            prompts = self.orchestrator.generate_context_prompts(categorized, clusters)
            self.logger.info(f"   ✓ {len(prompts)} prompts gerados\n")

            # Gerar dashboard final
            self.logger.info("📊 Criando dashboard principal...")
            self.orchestrator.create_dashboard(duplicates, clusters, graph, prompts)
            self.logger.info("   ✓ Dashboard atualizado\n")

            self.logger.info("="*60)
            self.logger.info("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            self.logger.info("="*60)

            # Resumo
            self._print_summary(files, documents, duplicates, clusters, prompts)

        except Exception as e:
            self.logger.error(f"❌ Erro durante processamento: {e}", exc_info=True)
            raise

    def _print_summary(self, files, documents, duplicates, clusters, prompts):
        """Imprime resumo do processamento"""
        print("\n" + "="*60)
        print("📈 RESUMO DO PROCESSAMENTO")
        print("="*60)
        print(f"Arquivos analisados:     {len(files)}")
        print(f"Documentos processados:  {len(documents)}")
        print(f"Duplicatas encontradas:  {len(duplicates)}")
        print(f"Clusters criados:        {len(clusters)}")
        print(f"Prompts gerados:         {len(prompts)}")
        print("="*60)
        print(f"\n📂 Outputs salvos em: {self.vault_root / self.config['paths']['output_dir']}")
        print("\nAcesse o dashboard em: _system/dashboard.md")
        print("="*60 + "\n")


def main():
    """Função principal"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║   SISTEMA DE GESTÃO DE CONHECIMENTO - OBSIDIAN VAULT     ║
║                                                           ║
║   Análise Inteligente • Remoção de Duplicatas            ║
║   Categorização Automática • Grafos de Conhecimento      ║
║   Prompts Contextuais Dinâmicos                          ║
╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        # Inicializar gerenciador
        manager = KnowledgeManager()

        # Executar pipeline completo
        manager.run_full_pipeline()

    except KeyboardInterrupt:
        print("\n⚠️  Processamento interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
