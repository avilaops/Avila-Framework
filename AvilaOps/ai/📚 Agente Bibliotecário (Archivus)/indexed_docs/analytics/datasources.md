# Data Sources (Analytics)

Canonical sources for commercial analytics and joins (geolocation × interest):

- events_utm: parsed UTM parameters from all inbound links (website, email, social)
- content_meta: front-matter from `marketing/templates/**` (title, channels, interests)
- newsletter_clicks: link-level clicks with utm.* expanded
- social_clicks: per-post clicks with utm.* expanded
- whatsapp_tags: conversation labels (intent) from WhatsApp Business
- crm_stages: pipeline stage per lead/account (lead, qualified, proposal, won, lost)
- geo_resolutions: GPS/CEP → geohash/municipio/UF mapping with accuracy and provider

Join keys & notes:
- Prefer (`utm.campaign`, `utm.id`, `utm.term`) for campaign attribution
- For user-level journeys, pseudonymize `user_id` with salted hash; avoid PII
- Aggregate to cohorts k≥20 before reporting; fallback to higher-level geography if needed

Retention & compliance:
- Default 90 days for raw events; aggregates can persist longer
- Segregate BR/PT datasets; enforce access control and audit logs
