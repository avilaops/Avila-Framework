#!/usr/bin/env python3
"""
ÁVILA AI ORCHESTRATOR - Sistema de Orquestração Inteligente
===========================================================

Maestro principal que coordena todos os pipelines de dados,
modelos de ML e agentes de IA do ecossistema Ávila.

Responsabilidades:
1. Coordenar coleta de dados de múltiplas fontes
2. Orquestrar pipelines ETL e ML
3. Gerenciar estado dos agentes de IA
4. Monitorar saúde do sistema
5. Gerar insights e relatórios

Autor: Ávila Tech
Data: 2025-11-10
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import yaml

# Analytics & ML
import pandas as pd
import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.preprocessing import StandardScaler

# AI & Embeddings
import openai
from sentence_transformers import SentenceTransformer

# Graph & Vector DB
import networkx as nx

# Utilities
from collections import defaultdict
import hashlib


@dataclass
class DataSource:
    """Representa uma fonte de dados no ecossistema"""
    name: str
    type: str  # 'obsidian', 'activitywatch', 'azure', 'copilot', 'terminal'
    path: Path
    polling_interval: int  # segundos
    last_sync: Optional[datetime] = None
    status: str = "idle"  # idle, syncing, error
    records_processed: int = 0

    def __hash__(self):
        return hash(self.name)


@dataclass
class Pipeline:
    """Representa um pipeline de processamento"""
    name: str
    sources: List[DataSource]
    schedule: str  # cron expression
    enabled: bool = True
    last_run: Optional[datetime] = None
    status: str = "idle"
    metrics: Dict[str, Any] = field(default_factory=dict)


class AvilaOrchestrator:
    """
    Orquestrador principal do sistema Ávila

    Implementa padrão Event-Driven Architecture com:
    - Event Loop assíncrono
    - Message Queue (em memória → Redis futuro)
    - Worker Pool para processamento paralelo
    """

    def __init__(self, config_path: str = "config.yaml"):
        """Inicializa o orquestrador"""

        # Carregar configuração
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Setup logging
        self.logger = self._setup_logging()

        # Inicializar componentes
        self.sources: Dict[str, DataSource] = {}
        self.pipelines: Dict[str, Pipeline] = {}
        self.event_queue = asyncio.Queue()
        self.knowledge_graph = nx.DiGraph()

        # State tracking
        self.state = {
            'orchestrator_started': datetime.now(),
            'total_events_processed': 0,
            'total_documents_indexed': 0,
            'total_insights_generated': 0,
            'active_agents': []
        }

        # AI Models (lazy loading)
        self._embedding_model = None
        self._openai_client = None

        self.logger.info("🎼 Ávila Orchestrator inicializado")

    def _setup_logging(self) -> logging.Logger:
        """Configura sistema de logging"""
        logger = logging.getLogger('AvilaOrchestrator')
        logger.setLevel(logging.INFO)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console.setFormatter(formatter)
        logger.addHandler(console)

        # File handler
        log_file = Path(self.config['logging']['file'])
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    @property
    def embedding_model(self):
        """Lazy loading do modelo de embeddings"""
        if self._embedding_model is None:
            self.logger.info("Carregando modelo de embeddings...")
            self._embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.logger.info("✓ Modelo carregado")
        return self._embedding_model

    @property
    def openai_client(self):
        """Lazy loading do cliente OpenAI"""
        if self._openai_client is None:
            import os
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            self._openai_client = openai.OpenAI(api_key=api_key)
            self.logger.info("✓ Cliente OpenAI inicializado")
        return self._openai_client

    def register_source(self, source: DataSource):
        """Registra uma nova fonte de dados"""
        self.sources[source.name] = source
        self.logger.info(f"📡 Fonte registrada: {source.name} ({source.type})")

    def register_pipeline(self, pipeline: Pipeline):
        """Registra um novo pipeline"""
        self.pipelines[pipeline.name] = pipeline
        self.logger.info(f"⚙️  Pipeline registrado: {pipeline.name}")

    async def start(self):
        """Inicia o orquestrador (main event loop)"""
        self.logger.info("\n" + "="*60)
        self.logger.info("🚀 ÁVILA ORCHESTRATOR STARTING")
        self.logger.info("="*60)

        # Iniciar workers
        workers = [
            asyncio.create_task(self._event_processor()),
            asyncio.create_task(self._health_monitor()),
            asyncio.create_task(self._scheduler())
        ]

        # Adicionar source pollers
        for source in self.sources.values():
            workers.append(
                asyncio.create_task(self._source_poller(source))
            )

        # Aguardar todos os workers
        await asyncio.gather(*workers)

    async def _event_processor(self):
        """Processa eventos da fila (consumer)"""
        self.logger.info("🔄 Event processor iniciado")

        while True:
            try:
                event = await self.event_queue.get()

                # Processar evento
                await self._handle_event(event)

                # Marcar como concluído
                self.event_queue.task_done()
                self.state['total_events_processed'] += 1

            except Exception as e:
                self.logger.error(f"Erro processando evento: {e}", exc_info=True)

            await asyncio.sleep(0.1)  # Prevent tight loop

    async def _handle_event(self, event: Dict[str, Any]):
        """Processa um evento específico"""
        event_type = event['type']

        handlers = {
            'file_created': self._handle_file_created,
            'file_modified': self._handle_file_modified,
            'activity_logged': self._handle_activity_logged,
            'azure_metric': self._handle_azure_metric,
            'copilot_interaction': self._handle_copilot_interaction,
        }

        handler = handlers.get(event_type)
        if handler:
            await handler(event['data'])
        else:
            self.logger.warning(f"Handler não encontrado para: {event_type}")

    async def _handle_file_created(self, data: Dict):
        """Handler: novo arquivo no Obsidian"""
        file_path = Path(data['path'])

        self.logger.info(f"📄 Novo arquivo: {file_path.name}")

        # Ler conteúdo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Gerar embedding
        embedding = self.embedding_model.encode(content)

        # Extrair metadata
        metadata = self._extract_metadata(content, file_path)

        # Adicionar ao knowledge graph
        node_id = self._add_to_knowledge_graph(file_path, metadata, embedding)

        # Detectar duplicatas
        duplicates = self._find_duplicates(embedding, threshold=0.85)
        if duplicates:
            self.logger.warning(f"⚠️  Possível duplicata detectada: {duplicates}")

        # Auto-categorização
        category = await self._categorize_document(content)
        self.logger.info(f"🏷️  Categoria: {category}")

        self.state['total_documents_indexed'] += 1

    async def _handle_file_modified(self, data: Dict):
        """Handler: arquivo modificado"""
        self.logger.debug(f"✏️  Arquivo modificado: {data['path']}")
        # Re-processar embedding, atualizar grafo, etc.

    async def _handle_activity_logged(self, data: Dict):
        """Handler: nova atividade do ActivityWatch"""
        # Análise de produtividade, detecção de padrões
        pass

    async def _handle_azure_metric(self, data: Dict):
        """Handler: métrica do Azure"""
        # Monitoramento de custos, performance, alertas
        pass

    async def _handle_copilot_interaction(self, data: Dict):
        """Handler: interação com Copilot"""
        # Análise de prompts, extração de conhecimento
        pass

    async def _source_poller(self, source: DataSource):
        """Polling de uma fonte de dados (producer)"""
        self.logger.info(f"👁️  Poller iniciado: {source.name}")

        while True:
            try:
                # Verificar se há novos dados
                new_data = await self._poll_source(source)

                # Gerar eventos
                for item in new_data:
                    event = {
                        'type': self._get_event_type(source.type, item),
                        'source': source.name,
                        'timestamp': datetime.now(),
                        'data': item
                    }
                    await self.event_queue.put(event)

                source.last_sync = datetime.now()
                source.records_processed += len(new_data)

            except Exception as e:
                self.logger.error(f"Erro polling {source.name}: {e}")
                source.status = "error"

            await asyncio.sleep(source.polling_interval)

    async def _poll_source(self, source: DataSource) -> List[Dict]:
        """Verifica se há novos dados na fonte"""
        new_data = []

        if source.type == 'obsidian':
            # Verificar novos/modificados arquivos .md
            vault_path = Path(source.path)
            cutoff_time = source.last_sync or datetime.now() - timedelta(days=1)

            for md_file in vault_path.rglob('*.md'):
                if md_file.stat().st_mtime > cutoff_time.timestamp():
                    new_data.append({
                        'path': str(md_file),
                        'modified': datetime.fromtimestamp(md_file.stat().st_mtime)
                    })

        elif source.type == 'activitywatch':
            # Query SQLite para novos registros
            pass

        elif source.type == 'azure':
            # Azure CLI / SDK para métricas
            pass

        return new_data

    def _get_event_type(self, source_type: str, item: Dict) -> str:
        """Determina o tipo de evento baseado na fonte"""
        mappings = {
            'obsidian': 'file_modified',  # ou file_created
            'activitywatch': 'activity_logged',
            'azure': 'azure_metric',
            'copilot': 'copilot_interaction'
        }
        return mappings.get(source_type, 'unknown')

    async def _health_monitor(self):
        """Monitor de saúde do sistema"""
        self.logger.info("💓 Health monitor iniciado")

        while True:
            # Verificar saúde de cada componente
            health = {
                'timestamp': datetime.now(),
                'sources': {name: src.status for name, src in self.sources.items()},
                'pipelines': {name: pipe.status for name, pipe in self.pipelines.items()},
                'event_queue_size': self.event_queue.qsize(),
                'uptime': (datetime.now() - self.state['orchestrator_started']).total_seconds()
            }

            # Log se houver problemas
            if any(status == 'error' for status in health['sources'].values()):
                self.logger.error(f"⚠️  Fontes com erro: {health['sources']}")

            await asyncio.sleep(60)  # Check a cada minuto

    async def _scheduler(self):
        """Scheduler para pipelines agendados"""
        self.logger.info("⏰ Scheduler iniciado")

        while True:
            now = datetime.now()

            for pipeline in self.pipelines.values():
                if not pipeline.enabled:
                    continue

                # Verificar se deve executar (simplificado)
                # TODO: implementar parsing de cron expression
                should_run = self._should_run_pipeline(pipeline, now)

                if should_run:
                    self.logger.info(f"▶️  Executando pipeline: {pipeline.name}")
                    await self._run_pipeline(pipeline)

            await asyncio.sleep(30)  # Check a cada 30s

    def _should_run_pipeline(self, pipeline: Pipeline, now: datetime) -> bool:
        """Verifica se pipeline deve executar agora"""
        # Simplificado: executar se nunca rodou ou passou do intervalo
        if pipeline.last_run is None:
            return True

        # Exemplo: rodar a cada hora
        interval = timedelta(hours=1)
        return (now - pipeline.last_run) > interval

    async def _run_pipeline(self, pipeline: Pipeline):
        """Executa um pipeline completo"""
        pipeline.status = "running"
        start_time = datetime.now()

        try:
            # Coletar dados de todas as fontes
            all_data = []
            for source in pipeline.sources:
                data = await self._poll_source(source)
                all_data.extend(data)

            # Processar dados (exemplo: clustering)
            if pipeline.name == "knowledge_clustering":
                await self._pipeline_clustering(all_data)

            # Atualizar métricas
            pipeline.metrics['last_duration'] = (datetime.now() - start_time).total_seconds()
            pipeline.metrics['records_processed'] = len(all_data)
            pipeline.last_run = datetime.now()
            pipeline.status = "idle"

            self.logger.info(f"✓ Pipeline concluído: {pipeline.name} ({len(all_data)} registros)")

        except Exception as e:
            self.logger.error(f"❌ Erro no pipeline {pipeline.name}: {e}")
            pipeline.status = "error"

    async def _pipeline_clustering(self, documents: List[Dict]):
        """Pipeline: clustering hierárquico de documentos"""
        if not documents:
            return

        self.logger.info(f"🗂️  Clustering {len(documents)} documentos...")

        # Gerar embeddings
        embeddings = []
        for doc in documents:
            content = doc.get('content', '')
            emb = self.embedding_model.encode(content)
            embeddings.append(emb)

        # Normalizar
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings)

        # HDBSCAN clustering
        clusterer = HDBSCAN(min_cluster_size=3, metric='euclidean')
        labels = clusterer.fit_predict(embeddings_scaled)

        # Agrupar por cluster
        clusters = defaultdict(list)
        for doc, label in zip(documents, labels):
            if label != -1:  # -1 = outliers
                clusters[int(label)].append(doc)

        self.logger.info(f"✓ {len(clusters)} clusters encontrados")

        # Gerar insights por cluster
        for cluster_id, docs in clusters.items():
            insight = await self._generate_cluster_insight(docs)
            self.logger.info(f"  Cluster {cluster_id}: {insight}")

    async def _generate_cluster_insight(self, documents: List[Dict]) -> str:
        """Gera insight sobre um cluster usando LLM"""
        # Extrair títulos/trechos
        samples = [doc.get('path', 'unknown')[:100] for doc in documents[:5]]

        prompt = f"""
        Analise este cluster de {len(documents)} documentos relacionados.
        Exemplos: {', '.join(samples)}

        Responda em 1 frase: qual é o tema comum destes documentos?
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erro gerando insight: {e}"

    def _extract_metadata(self, content: str, file_path: Path) -> Dict:
        """Extrai metadata de um documento"""
        metadata = {
            'title': file_path.stem,
            'path': str(file_path),
            'size': len(content),
            'lines': content.count('\n'),
            'created': datetime.fromtimestamp(file_path.stat().st_ctime),
            'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
        }

        # Extrair tags frontmatter (YAML)
        if content.startswith('---'):
            try:
                end = content.index('---', 3)
                frontmatter = yaml.safe_load(content[3:end])
                metadata['tags'] = frontmatter.get('tags', [])
                metadata['category'] = frontmatter.get('category')
            except:
                pass

        return metadata

    def _add_to_knowledge_graph(self, file_path: Path, metadata: Dict, embedding: np.ndarray) -> str:
        """Adiciona documento ao grafo de conhecimento"""
        node_id = hashlib.md5(str(file_path).encode()).hexdigest()[:8]

        self.knowledge_graph.add_node(
            node_id,
            title=metadata['title'],
            path=str(file_path),
            category=metadata.get('category', 'Uncategorized'),
            embedding=embedding.tolist()
        )

        # Criar arestas com documentos similares
        for other_id in self.knowledge_graph.nodes():
            if other_id == node_id:
                continue

            other_emb = np.array(self.knowledge_graph.nodes[other_id]['embedding'])
            similarity = self._cosine_similarity(embedding, other_emb)

            if similarity > 0.65:  # threshold para relacionamento
                self.knowledge_graph.add_edge(
                    node_id, other_id, weight=float(similarity)
                )

        return node_id

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calcula similaridade cosseno entre dois vetores"""
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def _find_duplicates(self, embedding: np.ndarray, threshold: float = 0.85) -> List[str]:
        """Encontra documentos duplicados baseado em embedding"""
        duplicates = []

        for node_id in self.knowledge_graph.nodes():
            other_emb = np.array(self.knowledge_graph.nodes[node_id]['embedding'])
            similarity = self._cosine_similarity(embedding, other_emb)

            if similarity >= threshold:
                duplicates.append(node_id)

        return duplicates

    async def _categorize_document(self, content: str) -> str:
        """Categoriza documento usando LLM"""
        categories = self.config['categorization']['main_categories']

        prompt = f"""
        Categorize este documento em UMA das seguintes categorias:
        {', '.join(categories)}

        Documento (primeiras 500 chars):
        {content[:500]}

        Responda apenas com o nome da categoria.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            category = response.choices[0].message.content.strip()
            return category if category in categories else "Uncategorized"
        except Exception as e:
            self.logger.error(f"Erro categorizando: {e}")
            return "Uncategorized"

    def get_status(self) -> Dict:
        """Retorna status atual do orquestrador"""
        return {
            'state': self.state,
            'sources': {name: {
                'status': src.status,
                'last_sync': src.last_sync,
                'records': src.records_processed
            } for name, src in self.sources.items()},
            'pipelines': {name: {
                'status': pipe.status,
                'last_run': pipe.last_run,
                'metrics': pipe.metrics
            } for name, pipe in self.pipelines.items()},
            'knowledge_graph': {
                'nodes': self.knowledge_graph.number_of_nodes(),
                'edges': self.knowledge_graph.number_of_edges()
            }
        }

    async def shutdown(self):
        """Desliga o orquestrador gracefully"""
        self.logger.info("\n🛑 Shutting down Ávila Orchestrator...")

        # Salvar estado
        state_file = Path("_system/orchestrator_state.json")
        state_file.parent.mkdir(exist_ok=True)

        with open(state_file, 'w') as f:
            json.dump(self.get_status(), f, indent=2, default=str)

        self.logger.info("✓ Estado salvo")
        self.logger.info("👋 Orchestrator stopped")


async def main():
    """Função principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║            ÁVILA AI ORCHESTRATOR v1.0                        ║
║                                                              ║
║  Sistema de Orquestração Inteligente                        ║
║  Event-Driven • Multi-Source • AI-Powered                   ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Inicializar orquestrador
    orchestrator = AvilaOrchestrator(
        config_path="scripts/config.yaml"
    )

    # Registrar fontes
    obsidian_source = DataSource(
        name="obsidian_vault",
        type="obsidian",
        path=Path(orchestrator.config['paths']['vault_root']),
        polling_interval=60  # 1 minuto
    )
    orchestrator.register_source(obsidian_source)

    # Registrar pipelines
    clustering_pipeline = Pipeline(
        name="knowledge_clustering",
        sources=[obsidian_source],
        schedule="0 0 * * 0",  # Todo domingo à meia-noite
        enabled=True
    )
    orchestrator.register_pipeline(clustering_pipeline)

    try:
        # Iniciar orquestração
        await orchestrator.start()

    except KeyboardInterrupt:
        await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
