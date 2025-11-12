# Archivus — Agente Bibliotecário

## Contexto
Archivus é o agente de curadoria responsável por garantir integridade, governança e padronização de arquivos nos repositórios Ávila Inc./ÁvilaOps.

## Objetivo
Monitorar estruturas oficiais (`Docs/`, `Logs/`, `Scripts/`, `Shared/`), executar rotinas automáticas (diária, semanal, mensal) e gerar relatórios de conformidade.

## Escopo Monitorado
```
C:\Users\nicol\OneDrive\Avila\
  Docs\Relatorios\{Conversas, Analises, Auditorias, ...}
  Logs\{Daily, Alerts, Archive}
  Scripts\{Backup, Maintenance, Verify}
  Shared\backups\archivus
```

Itens fora do padrão são sinalizados e removidos conforme rotina diária.

## Rotinas Automáticas
- **Diária (02:00)**: valida estrutura, rotaciona logs (>30 dias), coleta métricas e gera relatório em `Docs/Relatorios/Auditorias`.
- **Semanal (Dom 03:00)**: backup completo de `Scripts/`, verificação SHA256 e atualização de `integrity_manifest.json`.
- **Mensal (Dia 1 04:00)**: arquivamento profundo, limpeza de temporários e rotação de backups antigos.

## Operação Manual
- Executar rotina: `python archivus_main.py`
- Agendar Task Scheduler: script PowerShell em `READM[E]` (ver exemplos).
- Consultar logs: `C:\Users\nicol\OneDrive\Avila\Logs\Daily\archivus_<data>.log`

## Integrações
- **Atlas**: recebe relatórios diários e alertas de divergência.
- **Helix**: notificado sobre falha de backup ou alteração de scripts.
- **Sigma**: integrações financeiras futuras (backlog).

## Artefatos Gerados
- `integrity_manifest.json` — manifesto de arquivos críticos com hash, tamanho e data.
- `AUDITORIA_ARCHIVUS_<data>.md` — relatório diário com métricas, ações e achados.

## Responsável
- Atlas Squad + Archivus Ops Team

## Última atualização
- 2025-11-11
