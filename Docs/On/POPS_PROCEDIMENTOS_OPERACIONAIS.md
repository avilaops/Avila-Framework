# 📋 POPs - PROCEDIMENTOS OPERACIONAIS PADRÃO ÁVILA

## Manual Operacional Completo para Todos os Setores

**Versão:** 1.0
**Data:** 2025-11-10
**Objetivo:** Garantir que qualquer pessoa saiba exatamente o que fazer em qualquer situação

---

## 🎯 POP #1: ATENDIMENTO AO CLIENTE

### Quando usar:
Cliente entra em contato por qualquer canal (chat, email, WhatsApp, redes sociais)

### O que fazer:

**PASSO 1: Saudação (primeiros 30 segundos)**
```
Canais escritos (chat/WhatsApp/email):
"Olá [nome]! Sou [seu nome] da Ávila. Como posso ajudar você hoje?"

Telefone:
"Ávila, bom dia/boa tarde! [seu nome] falando. Como posso ajudar?"
```

**PASSO 2: Identificar tipo de contato**
- [ ] Novo lead (nunca falou com a gente)
- [ ] Cliente atual (já comprou/contratou)
- [ ] Dúvida técnica
- [ ] Reclamação
- [ ] Pedido de orçamento

**PASSO 3: Respostas por tipo**

**Se for NOVO LEAD:**
1. Perguntar: "Qual sua principal necessidade hoje?"
2. Qualificar (BANT):
   - Budget: Tem orçamento? ("Qual faixa de investimento você considera?")
   - Authority: Quem decide? ("Você é quem toma a decisão ou precisa consultar alguém?")
   - Need: Qual dor? ("Qual problema principal quer resolver?")
   - Timeline: Quando? ("Para quando precisa dessa solução?")
3. Se qualificado (budget + urgência): **Agendar reunião com SDR**
4. Se não qualificado: **Enviar material educativo + nurturing**

**Se for CLIENTE ATUAL:**
1. Verificar no CRM: qual produto/serviço ele tem
2. Perguntar: "Como podemos melhorar sua experiência?"
3. Se for suporte técnico → **escalar para Suporte (POP #2)**
4. Se for upgrade/novo serviço → **escalar para Vendas**

**Se for DÚVIDA TÉCNICA:**
1. Tentar resolver em até 5 minutos (usar knowledge base)
2. Se não souber → **NÃO INVENTAR!** → "Ótima pergunta! Vou consultar nosso especialista e te retorno em até 2h. Pode ser?"
3. Registrar no sistema: ticket + prazo de retorno
4. Escalar para **Suporte Nível 2**

**Se for RECLAMAÇÃO:**
1. Empatia SEMPRE: "Sinto muito por isso. Vou resolver agora mesmo."
2. Ouvir sem interromper
3. Anotar tudo
4. Prometer prazo realista: "Vou resolver até [horário]. Posso te ligar de volta?"
5. Escalar para **Gestor de Atendimento** (se grave)
6. **SEMPRE** dar retorno no prazo prometido

**Se for ORÇAMENTO:**
1. Usar **Calculadora de Preços** (Módulo 6 - a criar)
2. Enviar proposta por email em até 24h
3. Agendar follow-up em 3 dias

**PASSO 4: Registro obrigatório**
- [ ] Nome completo do cliente
- [ ] Empresa (se B2B)
- [ ] Email + telefone
- [ ] Motivo do contato
- [ ] Ação tomada
- [ ] Próximo passo agendado

**PASSO 5: Encerramento**
```
"Mais alguma dúvida que eu possa ajudar agora?"
[Aguardar resposta]
"Perfeito! Qualquer coisa, estamos à disposição. Tenha um ótimo dia!"
```

**SLA (tempo máximo de resposta):**
- Chat/WhatsApp: 5 minutos
- Email: 2 horas (horário comercial)
- Redes sociais: 1 hora

---

## ⬆️ POP #2: ESCALONAMENTO DE PROBLEMAS

### Quando usar:
Você não sabe responder OU problema é grave OU cliente pede para falar com gestor

### Matriz de Escalonamento:

| Situação                             | Para quem escalar     | Prazo                 |
| ------------------------------------ | --------------------- | --------------------- |
| **Dúvida técnica simples**           | Knowledge base IA     | Imediato              |
| **Dúvida técnica complexa**          | Suporte Nível 2       | 2h                    |
| **Bug crítico (sistema fora do ar)** | CTO + DevOps          | **IMEDIATO** (ligar!) |
| **Cliente irritado**                 | Gestor de Atendimento | 30min                 |
| **Pedido de reembolso**              | Financeiro + Gestor   | 24h                   |
| **Dúvida de contrato/jurídico**      | Administrativo        | 48h                   |
| **Oportunidade grande (>R$50k)**     | Diretor Comercial     | 1h                    |
| **Imprensa/mídia**                   | CEO                   | **IMEDIATO**          |
| **Questão ética/vazamento**          | CEO + Compliance      | **IMEDIATO**          |

### Como escalar:

**PASSO 1:** Avisar o cliente
```
"[Nome], para te dar a melhor resposta possível, vou passar seu caso
para [cargo/setor]. Você terá retorno em até [prazo]. Tudo bem?"
```

**PASSO 2:** Enviar no Slack:
```
@[pessoa] - ESCALAÇÃO [PRIORIDADE]

Cliente: [nome + empresa]
Canal: [WhatsApp/Email/Chat]
Problema: [resumo em 1 linha]
Contexto: [o que já tentou/falou]
Prazo prometido: [data/hora]

Link do ticket: [url]
```

**PASSO 3:** Acompanhar
- [ ] Confirmar que a pessoa recebeu (em até 15min)
- [ ] Checar status antes do prazo
- [ ] Informar cliente sobre andamento

**PASSO 4:** Fechar loop
Depois que resolvido, perguntar ao cliente:
```
"Conseguimos resolver sua questão? Como foi o atendimento de 1 a 5?"
```

---

## 💼 POP #3: VENDAS & NEGOCIAÇÃO

### Quando usar:
Lead qualificado pede proposta comercial

### Processo de Vendas (7 passos):

**1. DESCOBERTA (15-30 min de reunião)**

Perguntas obrigatórias:
- "Qual o principal desafio que vocês enfrentam hoje?"
- "O que já tentaram fazer para resolver?"
- "Se pudesse resolver isso com uma varinha mágica, qual seria o resultado ideal?"
- "Qual o impacto financeiro desse problema?" (quantificar!)
- "Quando precisam que isso esteja funcionando?"
- "Quem mais precisa aprovar essa decisão?"
- "Qual orçamento destinaram para isso?"

**2. DIAGNÓSTICO**

Identificar qual solução Ávila encaixa:
- [ ] Consultoria IA (1x projeto)
- [ ] Plataforma SaaS (recorrente)
- [ ] Desenvolvimento customizado
- [ ] Treinamento/Capacitação
- [ ] Combo (consultoria + plataforma)

**3. APRESENTAÇÃO DA SOLUÇÃO**

Estrutura de apresentação (max 20 slides):
1. Problema identificado (palavras do cliente)
2. Impacto atual (com números)
3. Nossa solução (como resolve)
4. Casos similares (social proof)
5. ROI esperado (quanto economiza/ganha)
6. Timeline de implementação
7. Investimento e condições

**4. PROPOSTA COMERCIAL**

Enviar PDF profissional com:
- Resumo executivo
- Escopo detalhado
- Cronograma
- Investimento (3 opções: básico, padrão, premium)
- Termos e condições
- Próximos passos

**Prazo de validade:** 15 dias

**5. FOLLOW-UP**

- Dia 1: Confirmar recebimento
- Dia 3: "Conseguiu revisar? Alguma dúvida?"
- Dia 7: "Vamos marcar 15min para alinhar?"
- Dia 12: "Proposta vence em 3 dias. Posso ajudar em algo?"
- Dia 15: "Precisa de mais tempo? Posso estender até [data]"

**6. NEGOCIAÇÃO**

**Objeções comuns e respostas:**

| Objeção | Resposta |
|---------|----------|
| "Muito caro" | "Entendo. Vamos olhar o ROI: você economiza R$X/mês. Em Y meses já pagou. Faz sentido?" |
| "Preciso pensar" | "Claro! O que especificamente precisa avaliar? Posso ajudar com mais informações?" |
| "Vou consultar concorrente" | "Ótimo! Compare features e ROI lado a lado. Ficamos à disposição para esclarecer diferenças." |
| "Não tenho budget agora" | "Entendo. Para quando vocês planejam? Posso reservar essa condição especial até lá?" |
| "Seu concorrente faz mais barato" | "Interessante! O que exatamente eles oferecem? [comparar apples-to-apples]" |

**Descontos autorizados:**
- Sem aprovação: até 5%
- Gerente Comercial: até 15%
- Diretor Comercial: até 25%
- CEO: acima de 25% (casos excepcionais)

**7. FECHAMENTO**

Quando cliente diz "sim":
1. Comemorar! 🎉 (mas com profissionalismo)
2. Enviar contrato em até 2h
3. Agendar kickoff (primeira reunião do projeto)
4. Passar bastão para **Gestão de Projetos**
5. Registrar no CRM: deal won + valor + prazo

---

## 📞 POP #4: COMUNICAÇÃO INTERNA

### Canais oficiais:

| Canal | Para que usar | Prazo de resposta |
|-------|---------------|-------------------|
| **Slack** | Urgências, dúvidas rápidas, coordenação diária | 15 min |
| **Email** | Comunicações formais, aprovações, documentos | 4h |
| **Reuniões** | Alinhamentos, decisões complexas, brainstorms | Agendar c/ 24h |
| **Obsidian** | Documentação, conhecimento, POPs, processos | n/a |
| **Dashboard** | Métricas, KPIs, status de projetos | Atualização diária |

### Rituais obrigatórios:

**DIARIAMENTE:**
- **9h:** Stand-up (15 min, Slack)
  - O que fiz ontem?
  - O que farei hoje?
  - Algum bloqueio?

**SEMANALMENTE:**
- **Segunda 10h:** Planning da semana (30 min)
  - Prioridades top 3 por setor
  - Dependências entre times

- **Sexta 16h:** Retrospectiva (30 min)
  - O que funcionou?
  - O que melhorar?
  - Wins da semana

**MENSALMENTE:**
- **Primeira segunda do mês:** All-hands (1h)
  - Resultados mês anterior
  - Metas mês atual
  - Reconhecimentos

### Etiqueta de comunicação:

✅ **FAZER:**
- Ser direto e claro
- Usar @menção quando precisa de resposta urgente
- Threads (não poluir canal principal)
- Emojis de reação (👍 ✅ ⚠️)
- Avisar se vai demorar: "Vi! Respondo em 1h"

❌ **NÃO FAZER:**
- Mensagens vagas ("precisamos conversar" sem contexto)
- Spam (enviar mesma mensagem em 5 canais)
- Discussões longas no chat (marcar reunião)
- Falar mal de cliente/colega (NUNCA)
- Deixar sem resposta (mínimo dar um "ok, vi")

---

## 🚨 POP #5: GESTÃO DE INCIDENTES

### Definição de incidente:
Qualquer evento que impacta ou pode impactar o serviço ao cliente

### Níveis de Severidade:

**P0 - CRÍTICO (Sistema fora do ar)**
- Afeta TODOS os clientes
- Perda de receita ativa
- **SLA:** Resolver em 1h
- **Ação:** Ligar CTO + CEO + DevOps imediatamente

**P1 - ALTO (Funcionalidade importante quebrada)**
- Afeta MUITOS clientes
- Workaround existe
- **SLA:** Resolver em 4h
- **Ação:** Escalar para Tech Lead

**P2 - MÉDIO (Bug não crítico)**
- Afeta POUCOS clientes
- Impacto limitado
- **SLA:** Resolver em 24h
- **Ação:** Criar ticket e priorizar

**P3 - BAIXO (Melhoria/cosmético)**
- Não afeta operação
- **SLA:** Incluir no próximo sprint
- **Ação:** Backlog

### Processo de Incidente:

**1. DETECÇÃO (0-5 min)**
- Alerta automático (monitoring)
- OU cliente reporta
- OU equipe detecta

**2. TRIAGEM (5-10 min)**
- Classificar severidade (P0/P1/P2/P3)
- Quem é o responsável? (on-call)
- Criar war room se P0/P1 (Slack channel)

**3. COMUNICAÇÃO (10-15 min)**
- Avisar clientes afetados
- Status page: "Estamos investigando problema X"
- Updates a cada 30min

**4. INVESTIGAÇÃO (paralelo)**
- Logs, métricas, traces
- Hipóteses → testes
- Documentar tudo no ticket

**5. RESOLUÇÃO**
- Aplicar fix
- Testar em staging
- Deploy em produção
- Validar (está resolvido mesmo?)

**6. PÓS-MORTEM (dentro de 48h)**
Documento obrigatório:
- O que aconteceu? (timeline)
- Por que aconteceu? (root cause)
- Como resolvemos?
- Como prevenir? (ações)
- Responsáveis + prazos

**Nunca culpar pessoas. Sempre melhorar processos.**

---

## 👤 POP #6: ONBOARDING (Novos Funcionários)

### DIA 1 (Boas-vindas)

**8h30 - Chegada**
- [ ] Recepção calorosa
- [ ] Tour pelo escritório (físico/virtual)
- [ ] Entregar: laptop, acessos, crachá, brindes

**9h - Café com CEO (30 min)**
- História da Ávila
- Missão, visão, valores
- Por que você foi escolhido

**9h30 - Setup técnico (1h)**
- [ ] Email @avila.com
- [ ] Slack
- [ ] GitHub/Azure DevOps
- [ ] CRM, ferramentas do setor
- [ ] VPN (se remoto)

**10h30 - Reunião com Gestor (1h)**
- Expectativas mútuas
- OKRs dos primeiros 90 dias
- Dúvidas

**12h - Almoço com time**

**14h - Treinamentos obrigatórios (3h)**
- [ ] Cultura Ávila (30 min)
- [ ] Segurança da informação (30 min)
- [ ] Ferramentas IA (1h)
- [ ] Processos do seu setor (1h)

**17h - Encerramento**
- Feedback do dia
- Plano para amanhã

### SEMANA 1 (Imersão)

- Shadowing (acompanhar colega experiente)
- Primeiras tarefas pequenas (não críticas)
- 1:1 diário com gestor (15 min)

### MÊS 1 (Produtividade)

- Assumir responsabilidades reais
- 1:1 semanal com gestor
- Check-in 30 dias: "Como está sendo? O que podemos melhorar?"

### MÊS 3 (Avaliação)

- Revisão de performance
- Confirmar fit cultural
- Planejar próximos 6 meses

---

## 📊 MÉTRICAS DE SUCESSO DOS POPs

Medir trimestralmente:

| POP | Métrica | Meta |
|-----|---------|------|
| **Atendimento** | Tempo médio de resposta | < 5 min |
| **Atendimento** | CSAT (satisfação) | > 4.5/5 |
| **Escalonamento** | Taxa de resolução 1º nível | > 70% |
| **Vendas** | Taxa de conversão (proposta → fechamento) | > 30% |
| **Vendas** | Ciclo de vendas médio | < 30 dias |
| **Incidentes** | MTTR (tempo p/ resolver) P0 | < 1h |
| **Incidentes** | MTTR P1 | < 4h |
| **Onboarding** | Satisfação novos funcionários | > 4.7/5 |
| **Onboarding** | Retenção após 3 meses | > 90% |

---

## 🔄 MANUTENÇÃO DESTE DOCUMENTO

**Responsável:** Gestor de Operações

**Revisão:** Trimestral (ou quando processo mudar)

**Como sugerir mudanças:**
1. Criar issue no GitHub: `POP - [nome] - [sugestão]`
2. Discussão com time afetado
3. Aprovação do gestor
4. Atualização do documento
5. Comunicar mudança (Slack + email)

---

**Versão atual:** 1.0
**Última atualização:** 2025-11-10
**Próxima revisão:** 2026-02-10

---

**Lembre-se: POPs são vivos. Se algo não funciona na prática, mude o POP!**

*A Ávila é uma empresa que aprende e evolui constantemente.* 🚀
