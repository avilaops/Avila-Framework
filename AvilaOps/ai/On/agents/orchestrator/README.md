# Orchestrator Agent

## Contexto
Agente maestro da suíte **On**, responsável por orquestrar interações entre humanos e agentes especializados. Atua como camada de inteligência semântica e roteamento dinâmico.

## Objetivo
Garantir que cada tarefa/conversa seja analisada, classificada e direcionada ao recurso mais adequado, mantendo fluxo contínuo e eficiente.

## Capacidades Principais
- **Análise semântica avançada**: extração de entidades, sentimentos, urgência e contexto.
- **Classificação inteligente**: categorização automática de conversas/tarefas.
- **Roteamento dinâmico**: direcionamento para agentes/humanos com balanceamento de carga.
- **Orquestração de workflows**: coordenação de múltiplos agentes, gestão de dependências e feedback loops.
- **Bridge humano-IA**: escalonamento seguro para supervisão quando necessário.

## Configuração
- Arquivo: `config.yaml`
- Modelo principal: GPT-4o
- Embeddings: `text-embedding-3-large`
- Turno padrão: 60 min
- Status: Ativo (telemetria habilitada)

## Integrações e Fluxos
- **Input**: Conversas, documentos, tasks e prompts capturados pelo bus.
- **Processamento**: análise semântica → classificação → roteamento → instruções de follow-up.
- **Output**: Decisões de roteamento, análise contextual e recomendações para Atlas/Helix/Atlas.
- Publica eventos `orchestrator/dispatch`, `orchestrator/alert`.

## Responsável
- Atlas Squad — Estratégia/Corporativo (com suporte MindLayer)

## Última atualização
- 2025-11-11