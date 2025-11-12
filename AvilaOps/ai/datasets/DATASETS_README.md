# Datasets - AvilaOps AI

Dados estruturados para treinamento, análise e operação dos agentes AI.

## 📂 Estrutura

```
datasets/
├── on/                          # Produto ON (onboarding & operações)
│   ├── onboarding_events.json   # Eventos de uso (DAU/MAU/TTV)
│   ├── support_tickets.json     # Tickets + tempo resolução
│   └── retention_cohorts.csv    # Análise retenção 30/60/90d
├── geolocation/                 # Produto Geolocation
│   ├── gps_samples.json         # Amostras GPS com consent
│   ├── interest_taxonomy.json   # Taxonomia de interesses
│   └── sales_targets.csv        # Região×interesse → conversão
└── shared/                      # Dados compartilhados
    ├── crm_interactions.json    # Interações CRM
    └── marketing_utm_clicks.json # Cliques UTM
```

## 🔐 Privacidade & Compliance

### Dados Sensíveis
- **GPS**: Pseudonimizados (`user_hash` em vez de `user_id`)
- **Consentimento**: Rastreado via `consent_id` + `retention_until`
- **Retenção**: Padrão 90 dias (configurável)
- **k-anonimato**: Agregações devem ter k≥20

### Responsável
- **Lex** (validação compliance)
- **Lumen** (analytics)
- **Helix** (engenharia de dados)

## 📊 Formatos Suportados

- **JSON**: Eventos, logs, taxonomias
- **CSV**: Tabelas agregadas, coortes
- **Parquet**: Big data (futuro)

## 🔄 Atualização

- **Frequência**: Semanal (automatizado via Helix)
- **Versionamento**: Git LFS para datasets grandes
- **Validação**: Schema validation antes de commit

## 📖 Dicionário de Dados

Ver README em cada subpasta (`on/`, `geolocation/`, `shared/`)
