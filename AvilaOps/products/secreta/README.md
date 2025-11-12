# Secreta

## Contexto
**Secreta** é a plataforma gamificada/metaverso da Ávila, construída como monorepo PNPM com múltiplos apps (API, web) e pacotes compartilhados.

## Objetivo
Centralizar código-fonte, documentação e automações do ecossistema Secreta, garantindo governança e integração contínua com os demais produtos Ávila.

## Estrutura Atual
- `apps/api` — backend Node/Express (TypeScript).
- `apps/web` — frontend Next.js.
- `packages/` — bibliotecas compartilhadas (UI, domínio, utilitários).
- `docs/` — guias técnicos, playbooks e materiais de comunicação.
- `pnpm-workspace.yaml` — definição dos workspaces.
- `INSTRUCOES.txt` / `SETUP.txt` — orientações iniciais de ambiente.

## Rotinas Essenciais
- Utilizar `pnpm` para instalação/execução (`pnpm install`, `pnpm dev`).
- Rodar linters/testes antes de PR (`pnpm lint`, `pnpm test`).
- Sincronizar deploys com `devops/pipelines` e monitoramento em `devops/monitoring`.
- Documentar APIs em `docs/api` e integrações em `docs/architecture`.

## Responsável
- Forge Squad — Produção/Indústria (com apoio Helix)

## Última atualização
- 2025-11-11
