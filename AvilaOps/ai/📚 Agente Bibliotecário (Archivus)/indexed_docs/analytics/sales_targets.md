# Sales Targets Model

Generated artifact combining geolocation cohorts × interest cohorts.

Schema (proposed):
- region_code (geohash5 | municipio | UF)
- interest_slug (from taxonomy)
- campaign_id (utm.id)
- campaign_name (utm.campaign)
- volume_leads (int)
- qualified_rate (decimal)
- win_rate (decimal)
- cac_estimated (decimal)
- ltv_estimated (decimal)
- recommendation_channel (enum: email|whatsapp|social|site)
- recommendation_message (short string)
- last_updated (timestamp)

Generation steps:
1. Aggregate events_utm + crm_stages → derive funnel metrics per region×interest.
2. Join cost data (marketing spend) to compute CAC.
3. Join retention/revenue data to estimate LTV.
4. Apply prioritization formula (e.g., score = win_rate * (ltv_estimated/cac_estimated)).
5. Export table → feed dashboards & playbooks.

Privacy:
- Cohorts only (k≥20).
- No raw PII; hashed IDs only in staging.
- Regional roll-up if thresholds not met.
