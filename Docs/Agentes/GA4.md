Ordem direta. Implante GA4 em toda a Ávila seguindo estas tarefas sequenciais. Sem debate.

0) Decisões
	1.	IDs por ambiente: G-PULSE-DEV, G-PULSE-STG, G-PULSE-PRD.
	2.	Identificador corporativo único: account_id (UUID ou slug). Proibido PII.

1) Admin GA4
	1.	Criar 3 propriedades (dev/stg/prod).
	2.	Ligar BigQuery Export nas 3.
	3.	Admin → Custom definitions → criar dimensions:
	•	account_id, persona, vertical, plan, env, utm_source, utm_medium, utm_campaign, utm_content, utm_term.
	4.	Admin → Conversions → marcar: submit_form, book_demo, start_pilot.
	5.	Ativar Consent Mode v2.

2) Padrão de eventos (usar exatamente estes nomes)

Base:
view_page, view_lp, start_form, submit_form, book_demo, download_asset, start_trial, start_pilot, login, logout, view_dashboard, error.

Parâmetros obrigatórios em todos:
env, account_id, persona, vertical, plan, utm_source, utm_medium, utm_campaign, utm_content, utm_term.

3) Web (Next.js/Azure Static Web Apps)
	1.	Incluir gtag no layout e desabilitar send_page_view.
	2.	Persistir UTM em cookie de sessão.
	3.	Helper global sendEvent(name, params).

Arquivos:
	•	/web/lib/ga.ts
	•	Chamar sendEvent('view_page', {...}) no carregamento; CTA dispara start_form; pós-submit dispara submit_form.

4) Backend (Node/.NET/Rust) via Measurement Protocol v2
	1.	Guardar GA4_MEASUREMENT_ID e GA4_API_SECRET no Key Vault/Azure App Config.
	2.	Criar função gaServerEvent(clientId, name, params) e usar em:
	•	Envio de e-mail: view_report_email.
	•	Geração de PDF/link: download_asset.
	•	Início de piloto: start_pilot.

5) E-mail e links
	1.	Todo link sai com UTM: ?utm_source=email&utm_medium=drip&utm_campaign=weekly_pulse.
	2.	Templates do Ávila Pulse já com UTM.
	3.	Registrar abertura clicando em link de confirmação no HTML do e-mail.

6) GTM (opcional)
	1.	DataLayer mínimo: { event, env, account_id, persona, vertical, plan }.
	2.	Tags GA4 Event lendo do DataLayer.
	3.	Disparadores por CSS/JS.

7) Segurança e Compliance
	1.	Proibido enviar e-mail, nome, telefone em eventos.
	2.	Consent Mode v2 antes de qualquer coleta.
	3.	Revisão de parâmetros por Security antes do deploy.

8) Observabilidade
	1.	Staging: ligar DebugView.
	2.	Alerta diário: volume de eventos < 60% da média 7d → abrir ticket no Helix.
	3.	Exportar para BQ e criar views para: funil, CAC, payback, origem por UTM.

9) Checklist de PR
	•	IDs de medição corretos por ambiente.
	•	Helper sendEvent presente.
	•	Eventos base implementados.
	•	Conversions marcadas.
	•	Custom dimensions criadas.
	•	BigQuery export ativo.
	•	Consent Mode v2 ativo.
	•	Alerta de volume configurado.

10) Divisão por times
	•	Web: itens 3 e parte do 5.
	•	Backend/Helix: itens 4 e parte do 5.
	•	Marketing/Vox: UTMs, campanhas, GTM.
	•	Data/Lumen: BQ, views, painéis, alertas.
	•	Security/Lex: revisão de parâmetros e consent.