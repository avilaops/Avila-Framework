# UTM Conventions

Use these keys in front-matter (lowercase):
- utm.source: channel origin (e.g., email, facebook, linkedin, website)
- utm.medium: format (e.g., outreach, newsletter, social, cpc)
- utm.campaign: business goal or named campaign (e.g., aquisicao_consultoria, newsletter_mensal)
- utm.content: variant identifier (e.g., cold_intro_v1, post_fb_v1)
- utm.term: interest/keyword slug (maps to interest taxonomy)
- utm.id: unique campaign id (short slug or UUID)

Examples:
- email outreach: source=email, medium=outreach, campaign=aquisicao_consultoria, content=cold_intro_v1, term=reduzir_custos, id=acq_001
- linkedin post: source=linkedin, medium=social, campaign=aprendizado_impacto, content=post_li_v1, term=aumento_receita, id=ai_2025_11

Rules:
- snake_case only
- keep consistent per campaign; document in `marketing/campaigns/`
- add date tags via commit, not in utm values
- utm.term must match an interest slug in `docs/analytics/interest_taxonomy.md`
- use utm.id to tie assets across channels to a single campaign row in the analytics warehouse

Interest taxonomy mapping:
- Keep a single source of truth in `docs/analytics/interest_taxonomy.md`
- Examples of slugs: `reduzir_custos`, `aumento_receita`, `financas_operacionais`, `marketing_performance`
- If multiple interests apply, prioritize the primary one in `utm.term` and add the rest as tags in content front-matter (`interests: []`)

Data model expectations (for joins):
- `events_utm` extracts standard UTM params from all links
- `content_meta` provides front-matter fields (title, channels, interests)
- Join key: (`utm.campaign`, `utm.id`, `utm.term`) → generates interest cohorts used em heatmaps região×interesse

Validation checklist (pre-merge):
- [ ] utm.source/medium/campaign/content present
- [ ] utm.term matches taxonomy slug
- [ ] utm.id present and unique per campaign
- [ ] Commit message references campaign (e.g., `campaign: aquisicao_consultoria`) and links issue/PR