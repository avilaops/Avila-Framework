# ÁvilaOps — Núcleo Técnico

## Contexto
ÁvilaOps é o braço operacional da Ávila Inc., responsável por Engenharia, DevOps, IA aplicada, infraestrutura corporativa, produtos digitais e pesquisa. Todas as iniciativas seguem a filosofia **Estrutura, Clareza, Execução**, com versionamento Git, documentação em Markdown e integração contínua entre VS Code, Visual Studio 2022, PowerShell e OneDrive.

## Objetivo
Fornecer um hub unificado para squads técnicos e agentes autônomos (Atlas, Helix, Lumen, Forge, Echo, Lex, Sigma, Vox, Archivus), garantindo governança, observabilidade e entregas reutilizáveis para todo o ecossistema Ávila.

## Estrutura Oficial
- `ai/` — pipelines de IA, agentes On, datasets e prompts.
- `data/` — malha analítica (ingestão, processamento, dashboards, warehouse).
- `devops/` — automações de backup, pipelines, segurança e monitoramento.
- `docs/` — bases de conhecimento (API, arquitetura, styleguides, políticas).
- `governance/` — diretrizes corporativas, arquitetura e procedimentos.
- `infra/` — runbooks de AWS, Azure, Docker, Hetzner e Kubernetes.
- `products/` — portfólio de produtos (CoreDesk, Insight, MindLayer, OpsFlow, Pulse, Secreta etc.).
- `Agente Bibliotecario (Archivus)/` — curadoria, integridade e auditorias.

## Operação
- Utilizar `.vscode/avila.code-workspace` e os snippets `avila-*` para novos artefatos.
- Registrar decisões arquiteturais em `docs/architecture` e governança em `governance/`.
- Orquestrar agentes via `ai/On/core/on_core.py` e monitorar pelo stack de observabilidade (`ai/On/observability`).
- Salvar logs de sessões do Copilot em `Docs/Relatorios/Conversas/` via script corporativo.

## Responsável
- Nícolas Ávila (Diretoria Técnica ÁvilaOps)

## Última atualização
- 2025-11-11