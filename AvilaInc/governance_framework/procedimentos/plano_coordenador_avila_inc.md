# Plano de Coordenacao - Avila Inc

## Missao para os proximos 90 dias
- Fechar o ciclo ponta a ponta do cliente: aquisicao -> atendimento -> proposta -> contrato -> faturamento -> recebimento -> pos-venda.
- Orquestrar marketing e conteudo sincronizados com GitHub e site oficial.
- Padronizar atendimento WhatsApp com SLA e governanca de catalogo, etiquetas e escalonamento.
- Instrumentar metricas financeiras e operacionais de forma semanal e mensal.
- Preparar a operacao Portugal: entidade legal, recebimentos em EUR, precificacao, impostos e compliance local.

## Roadmap 30-60-90 (responsavel: Coordenador)

### Dias 1-30 | Setup e governanca
- WhatsApp Business App configurado com etiquetas, respostas rapidas, horario, fila e regras de escalonamento. Definir caminho para migracao futura para Cloud API.
- CRM leve com pipeline padronizado: Lead -> Qualificacao -> Proposta -> Fechamento -> Implantacao -> Suporte. Integracao inicial via encaminhamento manual de conversas do WhatsApp.
- Conteudo: publicar calendario editorial mensal (semana a semana) e guideline de marca. Fontes obrigatorias: releases do GitHub, cases e lancamentos.
- Site: automatizar deploy via GitHub Actions e criar seccao News/Updates gerada a partir de tags de release.
- Financeiro: instituir plano de contas, centros de custo e rotina semanal de DRE gerencial. Criar checklist de faturamento e cobranca.
- Juridico: preparar templates padrao (MSA, NDA, Ordem de Servico) com numeracao, versionamento e assinatura eletronica.
- Portugal: montar lista de prerequisitos, cronograma de abertura, matriz de precos BR x PT e estrategia de recebimento EUR (IBAN/SEPA via Wise).

### Dias 31-60 | Integracoes e metricas
- Integracao de bancos (Wise, Inter, Nubank): captura diaria de extratos e saldos para datastore unico.
- Funil de marketing com UTMs padronizadas, eventos do site e relatorio semanal de CAC, conversao e LTV preliminar.
- Playbooks de atendimento: scripts por cenario, SLA, metricas (FRT, TMA, CSAT) e checklist de fechamento.
- Conteudo multiplataforma: fluxos no repo marketing/ gerando site e Facebook via unico Pull Request.
- Portugal: tabela tributaria de referencia, estimativa de margem por servico e politica de precos em EUR.

### Dias 61-90 | Escala e automacao
- Migrar WhatsApp para Cloud API com catalogo e webhooks alimentando o CRM.
- Automacao de cobranca: emissao de faturas, links de pagamento, reconciliacao automatica e notificacoes.
- Painel executivo unificado (financeiro, vendas, marketing, atendimento) com atualizacao semanal.
- Operacao Portugal ativa: conta bancaria EUR funcional, rotas de recebimento validadas e emissao fiscal conforme regras locais.

## Stack minima e fluxos
- **Repositores GitHub**
  - `site-avila-inc`: conteudo e deploy automatico.
  - `marketing/`: posts, imagens, calendario. Merge em `main` dispara geracao de pagina e agenda social.
  - `playbooks/`: atendimento, vendas, contratos, financas e operacao.
- **Data store**
  - PostgreSQL (ou SQLite piloto) com tabelas: `leads`, `deals`, `messages`, `posts`, `invoices`, `payments`, `bank_tx`, `contracts`.
- **Conectores**
  - Bancos: routines diarias (API/CSV) de Wise, Inter, Nubank -> `bank_tx`.
  - WhatsApp: fase manual via export/forward; fase Cloud API com webhooks -> `messages`.
  - GitHub: releases e commits etiquetados -> posts, changelog, pagina News.
- **Orquestracao**
  - GitHub Actions para deploy do site, geracao de conteudo e jobs de coleta.
  - Cron jobs (GitHub Actions ou scheduler) para ingestao de bancos e consolidacao de metricas.

## Operacao WhatsApp
- **Padrao inicial (App Business)**
  - Etiquetas: Novo, Qualificado, Proposta, Fechado, Suporte.
  - Respostas rapidas e mensagem de ausencia.
  - Catalogo com servicos principais.
  - Encaminhamento manual dos leads para o CRM com campo de origem.
- **Padrao Cloud API**
  - Numero unico oficial, webhooks para CRM, templates aprovados para follow-up e cobranca.
  - Opt-in de notificacoes, catalogo sincronizado e filas por time.
  - Escalonamento automatico (atendimento -> coordenador -> diretoria quando necessario).

## Calendario de conteudo e sincronizacao
- Fonte principal: arquivos Markdown no repo `marketing/` com front-matter (`title`, `channels`, `date`, `tags`, `cta`, `image`).
- Regra base: 3 posts por semana. Pilares: caso pratico, update de produto, bastidores/filosofia.
- CI/CD: merge em `main` gera pagina estatica do site, post para Facebook com UTM e registro em `posts` para relatorios.
- Vincular releases do GitHub a comunicados e notas de atualizacao.

## KPIs executivos (semanais/mensais)
- **Marketing**: sessoes do site, leads, conversao site->lead, CAC preliminar, CTR posts.
- **Vendas**: novos leads, leads qualificados, taxa de ganho, ticket medio, ciclo de vendas.
- **Atendimento**: FRT, TMA, CSAT, resolucao primeiro contato, backlog.
- **Financeiro**: MRR/ARR, margem bruta, inadimplencia, geracao/queima de caixa, DSO.
- **Produto/Entrega**: velocity, lead time de PR, defeitos por entrega, NPS pos go-live.

## Financeiro e bancos
- Rotina diaria de importacao (CSV/API) para `bank_tx` com campos normalizados: data, descricao, valor, contrapartida, banco.
- Conciliacao: `payments` vincula `invoices` a `bank_tx` por valor, data, descricao, com fila de discrepancias.
- Cobranca: links e formas por pais.
  - Brasil: Pix, boleto, cartao local.
  - Portugal/EU: IBAN/SEPA, opcional Stripe.
- Metricas: fluxo de caixa D+90, aging de recebiveis, forecast mensal.

## Contratos e compliance
- Templates padrao: NDA, MSA, Ordem de Servico com front-matter para variaveis.
- Workflow: numeracao unica, status (Rascunho, Revisao, Enviado, Assinado, Expirado), vinculo a deal e fatura.
- Assinatura eletronica com arquivamento do PDF assinado, hash e metadados no storage seguro.

## Brasil <-> Portugal
- Tabela de precos EUR com politica de arredondamento e margem target.
- Recebimento PT/EU: conta Wise com IBAN ou banco local, priorizando SEPA e cartoes.
- Centros de custo segregados BR e PT, relatorios fiscais distintos.
- Engajar contador local para tributos quando a entidade portuguesa estiver ativa.

## Entregas da primeira semana
1. Calendario editorial do mes publicado no repo `marketing/`.
2. Etiquetas e scripts padronizados no WhatsApp Business e treinamento do time.
3. Pipeline do site com canal News gerado via Pull Request integrado.
4. Planilha inicial de conciliacao com extratos Wise/Inter/Nubank populando `bank_tx`.
5. Templates contratuais com numeracao unificada em `playbooks/` ou pasta juridica.
6. Painel semanal com 10 KPIs priorizados.
