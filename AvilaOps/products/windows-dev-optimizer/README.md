# Windows Dev Optimizer

Plataforma AvilaOps para otimização de ambientes Windows voltados a desenvolvimento. O projeto combina módulos Python para higiene de sistema, integração com a plataforma ON (multi‑agente) e agora possui modo desktop com WebView embarcado.

## Visão Geral

- **Backend:** FastAPI + HTMX em `framework/app`, servindo dashboards dinâmicos e endpoints REST.
- **Integração ON:** `framework/core/on_integration.py` conecta o otimizador ao event bus dos agentes (Atlas, Helix, etc.).
- **Serviços de Suporte:** telemetria privacy-first, autenticação anônima e gerenciamento de sessões em `framework/services`.
- **Launcher Desktop:** `desktop_main.py` inicializa FastAPI internamente e exibe a UI em uma janela nativa via pywebview.
- **Scripts de Distribuição:** `build/` contém automações para ZIP instalável e pacote Inno Setup.

## Estrutura Atual
```
windows-dev-optimizer/
	app.py                  # Modo servidor padrão (FastAPI)
	desktop_main.py         # Launcher desktop com WebView
	start_windows_dev_optimizer.ps1
	framework/
		app/                # FastAPI + HTMX
		core/
		services/
		templates/
	modules/                # Edge, Bloatware, Developer setup etc.
	templates/              # Views raiz e parciais HTMX
	build/                  # Scripts de empacotamento
	exports/
	config/
	requirements.txt
	requirements_framework.txt
	README.md
```

## Como Executar (Dev)
1. Abra PowerShell e navegue até a pasta do produto.
2. (Opcional) gere ambiente virtual: `python -m venv .venv` e `\.venv\Scripts\Activate.ps1`.
3. Instale dependências: `pip install -r requirements_framework.txt`.
4. Rode o modo desktop: `python desktop_main.py` ou `./start_windows_dev_optimizer.ps1` (usa desktop por padrão).
5. Para rodar só o servidor HTTP: `./start_windows_dev_optimizer.ps1 -NoBrowser` e acesse `http://127.0.0.1:8000`.

## Empacotamento
- `build/create_installer.ps1`: gera ZIP com `install.ps1` que cria venv, instala dependências e atalho.
- `build/prepare_inno_assets.ps1`: prepara `build/inno_dist/` para compilar via Inno Setup (`windows_dev_optimizer.iss`).
- Opcional: usar PyInstaller para gerar executável único (ajuste caminhos e assine com certificado Avila).

## Funcionalidades Principais
- **Edge Analyzer:** métricas e limpeza controlada do Microsoft Edge.
- **Program Analyzer:** inventário de software e recomendações baseadas em uso.
- **Bloatware Remover:** catálogo de remoções seguras com checkpoints automáticos.
- **Developer Optimizer:** ajustes de performance, WSL2, toolchain e políticas de segurança.
- **ON Integration:** roteamento inteligente e colaboração entre agentes (Atlas, Helix, Sigma etc.).

## Logs e Telemetria
- Logs operacionais armazenados em `logs/` com rotação.
- Telemetria anonimizada (local-only) em SQLite criptografado (`framework/services/telemetry_service.py`).
- Relatórios exportados para `reports/` e `exports/`.

## Responsáveis
- OpsFlow Squad — Productivity & Workstations
- Contato: productivity@avila.inc

## Última atualização
- 2025-11-11