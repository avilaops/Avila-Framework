# Geolocation — trilha de estudo

## Objetivo
Avaliar viabilidade técnica e econômica de geolocalização para uso em operações e marketing, com privacidade-first.

## KPIs
- Cobertura (%), acurácia de geocoding, latência p95
- Custo por 1k consultas, custo total mensal
- Risco de privacidade (score) e cumprimento de consentimento

## Dados & Limites
- Objetivo: capturar a máxima granularidade de dados necessária para os estudos (incluindo GPS preciso) sempre que houver base legal adequada.
- Base legal e consentimento: GPS preciso permitido com consentimento explícito e registrável OU outra base legal aplicável (execução de contrato/legítimo interesse com LIA). Manter registro de consentimento/finalidade.
- Minimização por finalidade: coletar apenas campos necessários (ex.: latitude, longitude, acurácia, timestamp, fonte). Sem tracking em background sem aviso claro.
- Retenção: definir janelas por caso de uso (padrão 90 dias; estender somente com justificativa e DPA/contrato). Políticas de eliminação automática obrigatórias.
- Segurança e acesso: pseudonimização no ingestion, criptografia em trânsito e repouso, segregação BR/PT, acesso mínimo com logs e auditoria.
- Direitos do titular: opt-out e exclusão sob solicitação; atendimento em até 24h úteis.
- Avaliação de impacto: realizar DPIA quando houver uso em larga escala de localização precisa; aprovação do encarregado/DPO antes de produção.

## Experimentos (exemplos)
- Comparar provedores (API A vs API B) por acurácia e custo
- Cache local-first para reduzir latência e custo
- Coarsening de localização para minimizar risco e manter utilidade

## Decisões
- Registrar decisões com data, responsáveis e motivação (DRE de impacto quando aplicável)

## Enriquecimento & Cruzamentos (Interesses → Ação Comercial)

Objetivo: cruzar localização (GPS/CEP/município) com "dados de interesse" para orientar estratégia comercial (priorização de regiões, mensagens, canais, ofertas).

Fontes de interesse (ver `docs/analytics/datasources.md`):
- UTMs e páginas visitadas (conteúdo/tema → interesse)
- Cliques de newsletter e social
- Tags/etiquetas do WhatsApp Business (intenção)
- Estágio no CRM (lead qualificado, proposta, etc.)

Como cruzar (resumo operacional):
1) Padronizar geodados (lat/long, geohash, CEP) e eventos de interesse (taxonomia em `docs/analytics/interest_taxonomy.md`).
2) Pseudonimizar identificadores (user_id/account_id → hash com salt rotativo).
3) Agregar por coortes mínimas (k≥20) em geohash5/CEP3 para relatórios; se <k, subir granularidade (geohash4/município).
4) Gerar tabela `sales_targets` com pares região×interesse contendo: volume, conversão estimada, CAC estimado, recomendação de canal/mensagem.

KPIs comerciais resultantes:
- Heatmap região×interesse (volume e conversão)
- CAC/LTV por coorte de interesse e região
- Taxa de qualificação e win-rate por mensagem/canal

Privacidade & Compliance:
- Sem PII em relatórios; somente coortes agregadas (k-anonimato)
- Consentimento/legítimo interesse documentado para uso de localização precisa
- Segregação BR/PT e retenção conforme política vigente
