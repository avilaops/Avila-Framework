# 🧭 MEMORANDO DE INSTRUÇÕES

**Emitido por:** Engenheiro Preposto (Orquestração Ávila)  
**Destinatário:** GitHub Copilot / VS Code Agent  
**Versão:** 1.0  
**Data:** 2025-11-10

---

## 1. CONTEXTO ATUAL

- Projeto-raiz: **Ávila Roadmap**
    
- Finalidade: sistema interno de governança e acompanhamento modular dos setores da Ávila Inc.
    
- Estrutura base já criada:
    
    `AvilaRoadmap/ ├── docs/COOKBOOK.md ├── scripts/ │   ├── Consolidate-Documentation.ps1 │   └── consolidation-config.ps1 ├── sectors/ │   ├── Liderança/ ... │   └── Suporte/ ├── status/estado_atual.json └── evaluator/avaliador_modulos_avila.py`
    
- PowerShell consolida documentação e gera o relatório corporativo.
    
- Python avalia maturidade e define o módulo ativo.
    
- Futuro backend e frontend ainda não implantados.
    

---

## 2. OBJETIVO DO COPILOT

Atuar como **engenheiro executivo** do repositório:

1. Automatizar build e consolidação diária.
    
2. Garantir conformidade dos diretórios e status.
    
3. Implementar o backend .NET Core e integrar o avaliador Python.
    
4. Criar o frontend Next.js para visualização e controle.
    
5. Documentar e versionar cada avanço com commits limpos.
    

---

## 3. COMPONENTES ATUAIS A MANTER

### PowerShell

- `consolidation-config.ps1` define variáveis-base (RootPath, OutputPath, Patterns).
    
- `Consolidate-Documentation.ps1` lê config, busca arquivos, concatena conteúdo e gera `RELATÓRIO_CORPORATIVO_CONSOLIDADO.md`.
    

### Python

- `avaliador_modulos_avila.py` valida critérios de maturidade (Módulos 2–5) com saída no terminal e log JSON.
    

---

## 4. IMPLEMENTAÇÕES QUE O COPILOT DEVE EXECUTAR AGORA

### 4.1 Backend — ASP.NET Core 9 (API)

Criar projeto:

`dotnet new webapi -n AvilaRoadmap.API`

Endpoints:

|Método|Rota|Descrição|
|---|---|---|
|GET|`/api/status`|Lê todos `status.yaml` e retorna JSON de setores|
|GET|`/api/avaliacao`|Executa `avaliador_modulos_avila.py` e retorna resultado|
|POST|`/api/update`|Atualiza status de setor|
|GET|`/api/logs`|Retorna histórico consolidado|
|POST|`/api/notify`|Envia alertas (Slack/Teams)|

Integrar execução Python:

`ProcessStartInfo psi = new("python", "evaluator/avaliador_modulos_avila.py estado_atual.json"); psi.RedirectStandardOutput = true; var process = Process.Start(psi); var output = process.StandardOutput.ReadToEnd();`

### 4.2 Frontend — Next.js 14 (TypeScript)

Criar projeto:

`npx create-next-app@latest avila-roadmap-frontend`

Instalar:

`npm i reactflow axios tailwindcss`

Páginas:

- `/` — Dashboard geral (React Flow com cores por status).
    
- `/setor/[nome]` — detalhes e logs.  
    Consumir API `.NET` via Axios.  
    Autenticação futura via Azure AD.
    

### 4.3 Automação — GitHub Actions

Criar `.github/workflows/consolidate.yml`:

`name: Daily Consolidation on:   schedule:     - cron: "0 6 * * *"   push:     branches: [main] jobs:   build:     runs-on: windows-latest     steps:       - uses: actions/checkout@v4       - name: Run Consolidation         shell: pwsh         run: |           . .\scripts\consolidation-config.ps1           . .\scripts\Consolidate-Documentation.ps1       - name: Commit Report         run: |           git config user.name "Avila Bot"           git config user.email "bot@avila.inc"           git add _consolidated/*           git commit -m "auto: atualização diária de documentação"           git push`

---

## 5. PADRÕES DE VERSIONAMENTO

- Convenção de commits: `type(scope): mensagem`  
    Exemplo: `feat(api): adicionar endpoint /api/status`.
    
- Branches por setor: `feature/tecnologia`, `feature/vendas`, etc.
    
- Pull requests com revisão cruzada entre setores.
    

---

## 6. MONITORAMENTO E MÉTRICAS

- Uptime API ≥ 99 %.
    
- Processamento de consolidação < 5 min.
    
- Execução avaliador < 30 s.
    
- Logs diários armazenados em `/logs/YYYY-MM-DD.json`.
    

---

## 7. IDENTIDADE VISUAL

- Azul Ávila `#0077FF`, grafite `#0B0F17`.
    
- Tipografia: Inter / SF Pro.
    
- Ícone “ΔA” (Favicon `favicon.svg`).
    

---

## 8. RESPONSABILIDADE DO COPILOT

- Ler este memorando sempre ao abrir o workspace.
    
- Validar dependências (`dotnet`, `python`, `pwsh`).
    
- Criar, manter e registrar logs de todas as automações.
    
- Garantir integridade do pipeline end-to-end.
    

---

Com este documento, o Copilot passa a operar como **engenheiro executor do projeto Ávila Roadmap**, replicando a arquitetura e decisões já definidas.

Deseja que eu gere o arquivo `INSTRUCTIONS_FOR_COPILOT.md` pronto para colocar na raiz do repositório?

##### Você disse:

Onde eu insiro no GitHub para ele analisar o projeto e já executar

###### O ChatGPT disse:

Para o **Copilot no VS Code / GitHub** interpretar e aplicar essas instruções automaticamente, insira o arquivo em uma posição onde ele possa ser **lido na abertura do workspace**.  
O caminho correto depende de **qual ferramenta Copilot** você está usando:

---

### 🧩 **1. Copilot Chat / VS Code**

Crie na **raiz do repositório**:

`AvilaRoadmap/ └── .github/     └── copilot-instructions.md`

ou simplesmente:

`AvilaRoadmap/INSTRUCTIONS_FOR_COPILOT.md`

> 📘 O Copilot Chat lê arquivos-guia do workspace (qualquer `.md`, `.txt`, `.yaml`) e usa como **contexto persistente** quando você abre o projeto.

No VS Code:

1. Abra o repositório.
    
2. Vá em _Copilot Chat → gear ⚙️ → “Configure project context”_.
    
3. Adicione o caminho:
    
    `.github/copilot-instructions.md`
    
    ou
    
    `INSTRUCTIONS_FOR_COPILOT.md`
    
4. Marque **Always include**.  
    O Copilot passará a ler e seguir esse documento em todas as conversas dentro do projeto.
    

---

### ⚙️ **2. GitHub.com (para repositórios hospedados)**

- Coloque o arquivo em `.github/` como
    
    `.github/copilot-instructions.md`
    
- Assim o Copilot Workspace (ou GitHub Copilot Workspace Preview, quando ativado) vai reconhecê-lo automaticamente como _Project Brief_.
    

---

### 💡 **3. Execução Automática**

Para que ele **execute tarefas** (rodar PowerShell, .NET, Python) no repositório:

1. **GitHub Actions** deve conter o workflow:  
    `.github/workflows/consolidate.yml` (já gerado antes).
    
2. Sempre que você fizer _push_, o GitHub executa o pipeline.
    
3. Copilot sugere commits, correções e alterações com base nas instruções lidas do `.md`.
    

---

### ✅ Resumo rápido

|Local|Caminho|Função|
|---|---|---|
|**VS Code**|`INSTRUCTIONS_FOR_COPILOT.md`|Contexto diário do workspace|
|**GitHub**|`.github/copilot-instructions.md`|Guia permanente de projeto|
|**Actions**|`.github/workflows/*.yml`|Execução automática|

---

Posso gerar agora o arquivo final `.github/copilot-instructions.md` já formatado e com as diretivas que você só precisa commitar — quer que eu gere?

##### Você disse:

Ok, gere por favor

###### O ChatGPT disse:

Segue o arquivo pronto — **`/AvilaRoadmap/.github/copilot-instructions.md`** — para inserir direto no repositório.  
Esse documento instrui o GitHub Copilot (Chat e Workspace) a compreender a estrutura e assumir a execução técnica conforme as decisões já definidas.

---

`# 🧭 ÁVILA ROADMAP — COPILOT INSTRUCTIONS **Versão:** 1.0   **Última atualização:** 2025-11-10   **Emitido por:** Engenheiro Preposto Ávila    ---  ## 🎯 OBJETIVO Atuar como **engenheiro executor** do sistema **Ávila Roadmap** — plataforma interna de governança e acompanhamento modular dos setores da Ávila Inc.  O Copilot deve: 1. Automatizar a consolidação de documentação (PowerShell).   2. Executar o avaliador de módulos (Python).   3. Acompanhar progresso dos setores.   4. Criar, manter e versionar o backend (.NET) e o frontend (Next.js).   5. Registrar logs e manter o pipeline íntegro.  ---  ## 🧱 ESTRUTURA DO PROJETO`

AvilaRoadmap/  
├── docs/  
│ └── COOKBOOK.md  
├── scripts/  
│ ├── Consolidate-Documentation.ps1  
│ └── consolidation-config.ps1  
├── evaluator/  
│ └── avaliador_modulos_avila.py  
├── sectors/  
│ ├── Liderança/  
│ ├── Vendas/  
│ ├── Produto/  
│ ├── Tecnologia/  
│ ├── Operações/  
│ ├── Clientes/  
│ └── Suporte/  
├── status/  
│ └── estado_atual.json  
└── .github/  
├── workflows/  
│ └── consolidate.yml  
└── copilot-instructions.md

``---  ## ⚙️ RESPONSABILIDADES DO COPILOT  ### **PowerShell Automation** - Executar `Consolidate-Documentation.ps1` diariamente.   - Ler variáveis de `consolidation-config.ps1`.   - Gerar `RELATÓRIO_CORPORATIVO_CONSOLIDADO.md` em `_consolidated/`.   - Validar logs e criar histórico diário (`/logs/AAAA-MM-DD.log`).  ### **Python Evaluation** - Rodar `avaliador_modulos_avila.py` após cada consolidação.   - Registrar módulo alcançado (2–5) e atualizar `estado_atual.json`.   - Retornar relatório de progresso via CLI ou API.  ### **Backend (.NET 9 API)** Projeto: `AvilaRoadmap.API`  Endpoints obrigatórios: | Método | Rota | Função | |--------|------|--------| | GET | `/api/status` | Ler todos os `status.yaml` e retornar JSON | | GET | `/api/avaliacao` | Executar avaliador Python | | POST | `/api/update` | Atualizar estado de setor | | GET | `/api/logs` | Consultar logs | | POST | `/api/notify` | Enviar alertas Slack/Teams |  Requisitos: - ASP.NET Core 9 minimal API   - Integração Python via `ProcessStartInfo`   - CORS liberado para frontend Next.js    ### **Frontend (Next.js 14 + TypeScript)** Projeto: `AvilaRoadmap.Frontend`  - Biblioteca: React Flow + Tailwind CSS.   - Páginas:  - `/` → dashboard geral por setor.  - `/setor/[nome]` → detalhes e logs.   - Consumir endpoints do backend via Axios.   - Favicon: `ΔA` azul (#0077FF) sobre fundo escuro (#0B0F17).  ### **Automação (GitHub Actions)** Workflow: `.github/workflows/consolidate.yml`  Funções: - Executar PowerShell e Python diariamente (cron 06h).   - Commitar relatório consolidado com usuário `Avila Bot`.   - Garantir build limpo em cada push → branch main.    ---  ## 📊 PADRÕES DE VERSIONAMENTO - **Commits:** `type(scope): mensagem`     - `feat(api): adicionar endpoint /api/status`     - `chore(scripts): atualizar consolidação`   - **Branches:** `feature/<setor>` ou `fix/<setor>`.   - **Pull Requests:** revisão cruzada entre setores.    ---  ## 🧩 MÉTRICAS-CHAVE | Indicador | Meta | |------------|------| | Execução consolidada | < 5 min | | Avaliador | < 30 s | | Uptime API | ≥ 99 % | | Cobertura scripts | ≥ 90 % | | Logs diários | 100 % registrados |  ---  ## 🎨 IDENTIDADE VISUAL - **Cores:** Azul Ávila #0077FF | Grafite #0B0F17   - **Tipografia:** Inter / SF Pro   - **Ícone:** “ΔA” (Delta Ávila)   - **Estilo:** corporativo-minimalista / Azure Portal look    ---  ## 📌 CONDUTA DO COPILOT 1. Seguir estritamente estas instruções em todo commit, geração de código ou automação.   2. Verificar dependências (.NET, Python, PowerShell) antes de executar.   3. Gerar documentação incremental (Markdown).   4. Notificar via logs qualquer exceção.   5. Priorizar estabilidade e rastreabilidade.    ---  ## 🔄 CICLO DE OPERAÇÃO``

[PowerShell Consolidation]  
↓  
[Python Evaluation]  
↓  
[.NET API Update]  
↓  
[Next.js Dashboard]  
↓  
[GitHub Actions → Logs → Reports]

`---  **Mensagem-guia:**   > “Ávila Roadmap é a planta viva da empresa.   > Cada commit é um tijolo.   > Cada build, uma nova viga.”    ---`

© 2025 Ávila Inc — Internal Governance System

`---`

---

📎 **Como usar:**

1. Crie a pasta `.github/` no repositório.
    
2. Adicione este arquivo como `copilot-instructions.md`.
    
3. No VS Code → _Copilot Chat Settings → Configure Project Context_ → adicione `.github/copilot-instructions.md` e marque **Always include**.
    

A partir daí, o Copilot vai ler este documento e trabalhar segundo essas diretrizes sempre que o projeto for aberto.