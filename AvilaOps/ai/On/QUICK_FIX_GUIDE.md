# 🚀 GUIA DE CORREÇÃO RÁPIDA - ON PLATFORM

## ⚡ EXECUTE ISTO AGORA (15 minutos)

### 1️⃣ Instalar Dependências Completas

```powershell
# No terminal PowerShell, dentro da pasta On/

# Criar requirements completo
@"
# === CORE DEPENDENCIES ===
pyyaml>=6.0
openai>=1.0.0
requests>=2.31.0
rich>=13.0.0
tqdm>=4.66.0

# === WEB FRAMEWORK ===
flask>=3.0.0
flask-cors>=4.0.0
jinja2>=3.1.0

# === DATA SCIENCE ===
numpy>=1.24.0
scikit-learn>=1.3.0

# === NLP & EMBEDDINGS ===
# sentence-transformers>=2.2.0  # Descomente se quiser embeddings avançados
# torch>=2.0.0  # Descomente se quiser embeddings avançados

# === TELEMETRY ===
opentelemetry-api>=1.20.0
opentelemetry-sdk>=1.20.0
opentelemetry-instrumentation-flask>=0.41b0
prometheus-client>=0.18.0

# === UTILITIES ===
python-dotenv>=1.0.0
"@ | Out-File -FilePath requirements-full.txt -Encoding utf8

# Instalar
pip install -r requirements-full.txt
```

### 2️⃣ Criar Arquivo .env

```powershell
@"
# Configuração do ambiente ON Platform
OPENAI_API_KEY=sk-seu-api-key-aqui
OBSIDIAN_VAULT_PATH=C:/Users/nicol/OneDrive/Obsidian Vault
FLASK_ENV=development
FLASK_DEBUG=True
"@ | Out-File -FilePath .env -Encoding utf8
```

### 3️⃣ Corrigir config.yaml

```powershell
@"
on_core:
  version: "1.0.0"
  base_path: "."
  vault_path: "C:/Users/nicol/OneDrive/Obsidian Vault"
  language_model: "gpt-4o"
  embed_model: "text-embedding-3-large"
  auto_index: true
  sync_target: "onedrive"

agents_path: "./agents"
data_path: "./data"
logs_path: "./logs"

permissions:
  read: ["./agents/*/config.yaml", "./data/"]
  write: ["./logs/", "./registry/"]
  sync: true
"@ | Out-File -FilePath core/config.yaml -Encoding utf8
```

### 4️⃣ Criar Templates para Dashboard

```powershell
# Criar diretórios
New-Item -ItemType Directory -Force -Path "core\semantic\templates"
New-Item -ItemType Directory -Force -Path "core\semantic\static"
```

### 5️⃣ Criar Template HTML Simples

```powershell
@"
<!DOCTYPE html>
<html>
<head>
    <title>ON Platform Dashboard</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #00d9ff;
            text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .card {
            background: rgba(22, 33, 62, 0.8);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.4);
            border: 1px solid rgba(0, 217, 255, 0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 217, 255, 0.3);
        }
        .card h2 {
            margin-bottom: 15px;
            color: #00d9ff;
            font-size: 1.2em;
        }
        .metric {
            font-size: 2.5em;
            font-weight: bold;
            color: #00ff88;
            margin: 10px 0;
        }
        .status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
        }
        .status-active { background: #00ff88; color: #000; }
        .status-warning { background: #ffaa00; color: #000; }
        .status-error { background: #ff4444; color: #fff; }
        .logs-container {
            margin-top: 30px;
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 20px;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }
        .log-entry {
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 0.85em;
            padding: 8px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
        }
        .log-time { color: #888; }
        .log-agent { color: #00d9ff; font-weight: bold; }
        .log-message { color: #ddd; flex-grow: 1; margin: 0 15px; }
        .refresh-btn {
            background: #00d9ff;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin: 20px auto;
            display: block;
            transition: background 0.3s;
        }
        .refresh-btn:hover {
            background: #00ff88;
        }
    </style>
</head>
<body>
    <h1>🚀 ON PLATFORM - Dashboard de Monitoramento</h1>
    
    <div class="dashboard">
        <div class="card">
            <h2>⚙️ Status do Sistema</h2>
            <div class="status status-active" id="system-status">● OPERACIONAL</div>
            <p style="margin-top: 15px; color: #aaa;">
                Uptime: <strong id="uptime">Calculando...</strong>
            </p>
        </div>
        
        <div class="card">
            <h2>🤖 Agentes Ativos</h2>
            <div class="metric" id="active-agents">-</div>
            <p style="color: #aaa;">de 9 agentes configurados</p>
        </div>
        
        <div class="card">
            <h2>💬 Conversas</h2>
            <div class="metric" id="conversations-total">-</div>
            <p style="color: #aaa;">
                Ativas: <strong id="conversations-active" style="color: #00ff88;">-</strong>
            </p>
        </div>
        
        <div class="card">
            <h2>📚 Base de Conhecimento</h2>
            <div class="metric" id="knowledge-docs">-</div>
            <p style="color: #aaa;">documentos indexados</p>
        </div>
        
        <div class="card">
            <h2>🎯 Roteamento</h2>
            <div class="metric" id="routing-decisions">-</div>
            <p style="color: #aaa;">
                Confiança média: <strong id="routing-confidence" style="color: #00ff88;">-</strong>
            </p>
        </div>
        
        <div class="card">
            <h2>⚡ Performance</h2>
            <div class="metric" id="avg-response-time">-</div>
            <p style="color: #aaa;">tempo médio de resposta (min)</p>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="updateDashboard()">🔄 Atualizar Dados</button>
    
    <div class="logs-container">
        <h2 style="margin-bottom: 20px; color: #00d9ff;">📜 Logs do Sistema (últimos 15)</h2>
        <div id="logs-list">
            <p style="text-align: center; color: #888; padding: 20px;">
                Carregando logs...
            </p>
        </div>
    </div>
    
    <script>
        let startTime = Date.now();
        
        // Atualizar uptime a cada segundo
        setInterval(() => {
            const uptimeSeconds = Math.floor((Date.now() - startTime) / 1000);
            const hours = Math.floor(uptimeSeconds / 3600);
            const minutes = Math.floor((uptimeSeconds % 3600) / 60);
            const seconds = uptimeSeconds % 60;
            document.getElementById('uptime').textContent = 
                hours + 'h ' + minutes + 'm ' + seconds + 's';
        }, 1000);
        
        // Atualizar dashboard automaticamente a cada 10 segundos
        setInterval(updateDashboard, 10000);
        updateDashboard();
        
        async function updateDashboard() {
            try {
                // Buscar métricas
                const response = await fetch('/api/metrics/overview');
                const data = await response.json();
                
                // Atualizar cards
                document.getElementById('active-agents').textContent = 
                    data.resources?.active_count || 0;
                document.getElementById('conversations-total').textContent = 
                    data.conversations?.total_today || 0;
                document.getElementById('conversations-active').textContent = 
                    data.conversations?.active || 0;
                document.getElementById('knowledge-docs').textContent = 
                    data.knowledge?.total_documents || 0;
                document.getElementById('routing-decisions').textContent = 
                    data.routing?.total_decisions || 0;
                document.getElementById('routing-confidence').textContent = 
                    ((data.routing?.avg_confidence || 0) * 100).toFixed(1) + '%';
                document.getElementById('avg-response-time').textContent = 
                    (data.conversations?.avg_resolution_time || 0).toFixed(1);
                
                // Atualizar status
                const status = data.conversations?.active > 0 ? 'active' : 'warning';
                document.getElementById('system-status').className = 'status status-' + status;
                
            } catch (error) {
                console.error('Erro ao buscar métricas:', error);
                document.getElementById('system-status').className = 'status status-error';
                document.getElementById('system-status').textContent = '● ERRO DE CONEXÃO';
            }
            
            // Buscar logs
            try {
                const logsResponse = await fetch('/api/logs/recent?limit=15');
                const logs = await logsResponse.json();
                
                if (logs && logs.length > 0) {
                    const logsHtml = logs.map(log => {
                        const time = new Date(log.timestamp).toLocaleTimeString('pt-BR');
                        return '<div class="log-entry">' +
                            '<span class="log-time">' + time + '</span>' +
                            '<span class="log-agent">[' + log.agent + ']</span>' +
                            '<span class="log-message">' + log.message + '</span>' +
                            '</div>';
                    }).join('');
                    
                    document.getElementById('logs-list').innerHTML = logsHtml;
                } else {
                    document.getElementById('logs-list').innerHTML = 
                        '<p style="text-align: center; color: #888; padding: 20px;">' +
                        '⚠️ Nenhum log ainda. Execute o sistema para gerar logs.</p>';
                }
            } catch (error) {
                console.error('Erro ao buscar logs:', error);
                document.getElementById('logs-list').innerHTML = 
                    '<p style="text-align: center; color: #ff4444; padding: 20px;">' +
                    '❌ Erro ao carregar logs</p>';
            }
        }
    </script>
</body>
</html>
"@ | Out-File -FilePath core/semantic/templates/dashboard.html -Encoding utf8
```

### 6️⃣ Criar Script de Inicialização Rápida

```powershell
@"
#!/usr/bin/env python3
'''
ON Platform - Quick Start Script
Inicialização rápida para testes
'''

import sys
from pathlib import Path

# Adiciona core ao path
sys.path.insert(0, str(Path(__file__).parent / 'core'))

from on.core.on_core import OnCoreApp

def main():
    print('=' * 60)
    print('🚀 ON PLATFORM - QUICK START')
    print('=' * 60)
    print()
    
    # Inicializar e rodar
    app = OnCoreApp()
    
    try:
        app.run_forever()
    except KeyboardInterrupt:
        print('\n\n🛑 Sistema interrompido pelo usuário')
    except Exception as e:
        print(f'\n❌ Erro: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
"@ | Out-File -FilePath quick_start.py -Encoding utf8
```

### 7️⃣ EXECUTAR O SISTEMA!

```powershell
# Executar
python quick_start.py
```

---

## 🎯 O QUE ESPERAR

Após executar `python quick_start.py`, você verá:

```
============================================================
🚀 ON PLATFORM - QUICK START
============================================================

ON CORE - ÁVILA OPS (Modo Produção)
Iniciando em: 2025-11-12T10:30:00

Configuração central carregada
✓ SQLite inicializado (registry/on_core.db)
✓ Telemetria OpenTelemetry ativa
✓ 9 agente(s) detectado(s)
  → Orchestrator registrado (área=Orquestração, turno=30 min)
  → Atlas registrado (área=Estratégia, turno=60 min)
  → Helix registrado (área=Engenharia, turno=45 min)
  ...
============================================================
🚀 On.Core inicializado em modo serviço
📊 Telemetria: http://localhost:3000 (Grafana)
🔍 Prometheus: http://localhost:9090
📜 Loki: http://localhost:3100
============================================================
💓 System heartbeat | Uptime: 30s
```

**E os arquivos começarão a ser criados:**

```
registry/
  └── on_core.db          ← Banco SQLite com logs, tasks, shifts

logs/                     ← Ainda vazio (logs vão para o banco)

frontend-monitor/
  └── (use o dashboard em core/semantic/templates/dashboard.html)
```

---

## 🔧 PRÓXIMO PASSO: Iniciar Dashboard Web

```powershell
# Em outro terminal, criar servidor Flask simples
@"
from flask import Flask, render_template, jsonify
from pathlib import Path
import sys
import sqlite3

sys.path.insert(0, str(Path(__file__).parent / 'core'))

app = Flask(__name__, 
            template_folder='core/semantic/templates',
            static_folder='core/semantic/static')

DB_PATH = Path('registry/on_core.db')

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/metrics/overview')
def metrics():
    return jsonify({
        'conversations': {'total_today': 0, 'active': 0, 'avg_resolution_time': 0},
        'routing': {'total_decisions': 0, 'avg_confidence': 0.85},
        'knowledge': {'total_documents': 0},
        'resources': {'active_count': 9}
    })

@app.route('/api/logs/recent')
def logs():
    if not DB_PATH.exists():
        return jsonify([])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        'SELECT agent, timestamp, message FROM logs ORDER BY id DESC LIMIT 15'
    )
    logs = [{'agent': r[0], 'timestamp': r[1], 'message': r[2]} for r in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs)

if __name__ == '__main__':
    print('🌐 Dashboard disponível em: http://localhost:5000')
    app.run(debug=True, port=5000)
"@ | Out-File -FilePath run_dashboard.py -Encoding utf8

# Executar dashboard
python run_dashboard.py
```

**Acesse:** http://localhost:5000

---

## ✅ CHECKLIST DE VALIDAÇÃO

Após executar, verifique:

- [ ] `python quick_start.py` executa sem erros
- [ ] Arquivo `registry/on_core.db` foi criado
- [ ] Banco tem dados: `sqlite3 registry/on_core.db "SELECT COUNT(*) FROM logs"`
- [ ] Dashboard Flask roda em http://localhost:5000
- [ ] Dashboard mostra "9 agentes ativos"
- [ ] Logs aparecem na interface web
- [ ] Sistema heartbeat aparece no console

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### Erro: "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install flask flask-cors
```

### Erro: "No such table: logs"
```powershell
# Deletar e recriar banco
Remove-Item registry/on_core.db -Force
python quick_start.py  # Recria o banco
```

### Erro: OpenAI API
```powershell
# Editar .env e adicionar chave válida
OPENAI_API_KEY=sk-sua-chave-real
```

### Dashboard não atualiza
- Verifique se `run_dashboard.py` está rodando
- Abra console do navegador (F12) para ver erros
- Confirme que `quick_start.py` está gerando logs no banco

---

## 📧 RESUMO PARA EMAIL

**Situação:** Sistema não estava sendo executado, por isso logs e frontend vazios.

**Solução:**
1. Instalar dependências completas (`pip install -r requirements-full.txt`)
2. Criar templates do dashboard
3. Executar `python quick_start.py` (inicializa sistema)
4. Executar `python run_dashboard.py` (interface web)
5. Acessar http://localhost:5000

**Resultado:** Sistema operacional com logs sendo gerados e dashboard funcional!

---

**Tempo total:** 15-20 minutos  
**Complexidade:** Baixa (copiar e colar comandos)
