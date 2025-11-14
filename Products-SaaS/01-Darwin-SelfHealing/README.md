# 🧬 Darwin - Self-Healing Python Library

> **Sua aplicação que aprende com os próprios erros e se auto-corrige**

[![PyPI version](https://badge.fury.io/py/darwin-healing.svg)](https://badge.fury.io/py/darwin-healing)
[![Downloads](https://pepy.tech/badge/darwin-healing)](https://pepy.tech/project/darwin-healing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 **O Problema**

Você já passou por isso?

```python
# Erro: ModuleNotFoundError: No module named 'requests'
# Você: pip install requests
# 5 minutos depois...

# Erro: Port 8000 already in use
# Você: kill -9 $(lsof -t -i:8000)
# 10 minutos depois...

# Erro: Permission denied: '/var/log/app.log'
# Você: sudo chmod 777 /var/log/app.log
# Mais 15 minutos perdidos...
```

**30+ minutos perdidos por dia** corrigindo os mesmos erros.

**Darwin resolve isso automaticamente.**

---

## ✨ **A Solução**

```python
from darwin import SelfHealing

# Ativa self-healing na sua app
app = SelfHealing()

@app.heal
def minha_funcao():
    import requests  # Darwin instala automaticamente se não existir
    response = requests.get('https://api.exemplo.com')
    return response.json()

# Se der erro, Darwin:
# 1. Detecta o problema (ex: ModuleNotFoundError)
# 2. Aplica a correção (pip install requests)
# 3. Tenta novamente
# 4. Salva o aprendizado para próxima vez
```

**Resultado:** Sua app se auto-corrige enquanto você toma café ☕

---

## 🚀 **Instalação**

```bash
pip install darwin-healing
```

---

## 📖 **Como Usar**

### 1. **Básico - Decorador**

```python
from darwin import heal

@heal
def processar_dados():
    # Seu código aqui
    # Darwin cuida dos erros automaticamente
    pass
```

### 2. **Avançado - Context Manager**

```python
from darwin import SelfHealing

with SelfHealing() as healer:
    # Todo código aqui é auto-corrigido
    servidor.start()
    processar_requests()
```

### 3. **Expert - Configuração Customizada**

```python
from darwin import Darwin

darwin = Darwin(
    auto_install_packages=True,
    auto_fix_ports=True,
    auto_fix_permissions=False,  # Desabilitar correção de permissões
    learning_mode=True,           # Salvar aprendizados
    notification=True             # Notificar correções
)

@darwin.heal
def minha_app():
    # Configurações personalizadas aplicadas
    pass
```

---

## 🧠 **O Que Darwin Corrige Automaticamente**

### ✅ **Padrões Inclusos (12)**

| Erro                    | Correção Automática          |
| ----------------------- | ---------------------------- |
| `ModuleNotFoundError`   | `pip install <module>`       |
| `Port already in use`   | Troca porta ou mata processo |
| `Permission denied`     | `chmod` ou solicita sudo     |
| `Connection timeout`    | Retry com backoff            |
| `File not found`        | Cria arquivo/diretório       |
| `Disk space full`       | Limpa arquivos temporários   |
| `Memory error`          | Libera memória não usada     |
| `Import error`          | Instala dependências         |
| `Database locked`       | Retry com wait               |
| `SSL certificate error` | Atualiza certificados        |
| `DNS resolution failed` | Tenta DNS alternativo        |
| `Rate limit exceeded`   | Aplica throttling            |

### 🎁 **Darwin Pro - 50+ Padrões** (R$ 97/mês)

- Correções avançadas de AWS/Azure
- Auto-scaling baseado em métricas
- Rollback automático em falhas
- Integração Slack/Discord/Teams
- Analytics de falhas
- Suporte prioritário

---

## 📊 **Benefícios**

### 💰 **Economia de Tempo**

```
Antes do Darwin:
- 30 min/dia corrigindo erros
- 2.5h/semana
- 10h/mês
- 120h/ano (15 dias úteis)

Com Darwin:
- 0 min/dia
- Economia: R$ 20.000-50.000/ano
  (baseado em salário dev R$ 10k-25k/mês)
```

### 🧠 **Aprendizado Contínuo**

Darwin salva **todos os erros e correções**:

```json
{
  "error": "ModuleNotFoundError: requests",
  "solution": "pip install requests",
  "success": true,
  "timestamp": "2025-11-13T15:30:00",
  "occurrences": 3
}
```

Na 2ª vez que o erro aparecer, Darwin já sabe o que fazer.

### 🔒 **100% Privado**

- Roda localmente (sem enviar dados para cloud)
- Open-source (código auditável)
- Zero dependências de API externa

---

## 🎯 **Casos de Uso**

### 1. **Desenvolvimento Local**

```python
@heal
def dev_server():
    # Nunca mais se preocupe com portas em uso
    # ou módulos faltando
    app.run(debug=True)
```

### 2. **CI/CD Pipelines**

```yaml
# .github/workflows/test.yml
- name: Run tests with Darwin
  run: |
    pip install darwin-healing
    darwin run pytest tests/
    # Darwin corrige falhas no pipeline automaticamente
```

### 3. **Produção (com cuidado)**

```python
# Apenas correções seguras em produção
darwin = Darwin(
    safe_mode=True,  # Só correções não-destrutivas
    notify_only=True # Apenas notifica, não corrige
)
```

---

## 📈 **Comparação**

| Solução             | Tempo p/ Corrigir | Custo              | Aprendizado |
| ------------------- | ----------------- | ------------------ | ----------- |
| **Manual**          | 30 min/erro       | R$ 0               | ❌ Não       |
| **Stack Overflow**  | 15 min/erro       | R$ 0               | ❌ Não       |
| **Copilot/ChatGPT** | 5 min/erro        | US$ 20/mês         | ⚠️ Limitado  |
| **Darwin**          | 0 min             | R$ 0 (open-source) | ✅ Sim       |
| **Darwin Pro**      | 0 min             | R$ 97/mês          | ✅ Avançado  |

---

## 🛠️ **Arquitetura**

```
┌─────────────────────────────────────┐
│   Sua Aplicação Python              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Darwin Decorator/Context Manager  │
│   - Intercepta exceções             │
│   - Analisa padrão de erro          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Pattern Matcher                   │
│   - 12 padrões built-in             │
│   - Custom patterns (Pro)           │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Auto-Fix Engine                   │
│   - Executa correção                │
│   - Retry original function         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Learning Storage (JSON)           │
│   - Salva erro + solução            │
│   - Incrementa contador             │
└─────────────────────────────────────┘
```

---

## 🔧 **Configuração**

### `darwin.yaml`

```yaml
darwin:
  # Correções automáticas
  auto_install_packages: true
  auto_fix_ports: true
  auto_fix_permissions: false

  # Aprendizado
  learning_mode: true
  storage_path: "./darwin_knowledge/"

  # Notificações
  notifications:
    enabled: true
    channels:
      - console
      - file
      - slack  # Requer Darwin Pro

  # Segurança
  safe_mode: false
  allowed_commands:
    - pip
    - npm
    - chmod

  # Performance
  max_retries: 3
  retry_delay: 1.0
```

---

## 📚 **Documentação**

- [Guia de Início Rápido](./docs/quickstart.md)
- [API Reference](./docs/api.md)
- [Padrões de Erro](./docs/patterns.md)
- [Configuração Avançada](./docs/advanced.md)
- [FAQ](./docs/faq.md)

---

## 🤝 **Contribuir**

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-correcao`)
3. Commit (`git commit -m 'Adiciona correção para XYZ'`)
4. Push (`git push origin feature/nova-correcao`)
5. Abra um Pull Request

---

## 📜 **Licença**

MIT License - use livremente!

**Darwin Pro** é licença comercial (R$ 97/mês).

---

## 💬 **Suporte**

- **GitHub Issues:** [github.com/avila/darwin/issues](https://github.com/avila/darwin/issues)
- **Discord:** [discord.gg/darwin](https://discord.gg/darwin)
- **Email:** support@darwin-healing.com
- **Docs:** [docs.darwin-healing.com](https://docs.darwin-healing.com)

---

## 🌟 **Roadmap**

### Q1 2026
- [x] Release open-source (v1.0)
- [x] 12 padrões de correção
- [ ] PyPI package
- [ ] Documentação completa

### Q2 2026
- [ ] Darwin Pro (50+ padrões)
- [ ] Dashboard web de analytics
- [ ] Integração Slack/Discord
- [ ] API para custom patterns

### Q3 2026
- [ ] Darwin Cloud (SaaS)
- [ ] Team collaboration
- [ ] Enterprise features
- [ ] Certificação de segurança

---

## 🏆 **Criado por**

**Ávila Inc** - Construindo o futuro da automação inteligente

- 🌐 [avila.inc](https://avila.inc)
- 📧 nicolas@avila.inc
- 🐦 [@avilaframework](https://twitter.com/avilaframework)

---

**⭐ Se Darwin te salvou tempo, dê uma estrela no GitHub!**

```bash
# Teste agora
pip install darwin-healing
python -c "from darwin import heal; print('🧬 Darwin instalado!')"
```

---

_"Pare de corrigir erros manualmente. Deixe Darwin evoluir sua aplicação."_ 🧬
