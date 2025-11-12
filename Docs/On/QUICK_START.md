# 🚀 ÁVILA - GUIA DE SETUP RÁPIDO

## Começar AGORA (30 minutos)

**Data:** 2025-11-10

---

## ✅ PRÉ-REQUISITOS

```powershell
# Verificar instalações necessárias
python --version  # Deve ser 3.11+
git --version
az --version  # Azure CLI
```

Se algo faltar:
```powershell
# Instalar Python
winget install Python.Python.3.11

# Instalar Azure CLI
winget install Microsoft.AzureCLI

# Instalar Git
winget install Git.Git
```

---

## 📁 PASSO 1: Criar Estrutura de Diretórios (2min)

```powershell
# Criar ecossistema Ávila
$avilaRoot = "C:\Users\nicol\OneDrive\Avila"

# Estrutura completa
$dirs = @(
    "$avilaRoot\data\raw"
    "$avilaRoot\data\processed"
    "$avilaRoot\data\embeddings"
    "$avilaRoot\models\trained"
    "$avilaRoot\models\artifacts"
    "$avilaRoot\outputs\reports"
    "$avilaRoot\outputs\dashboards"
    "$avilaRoot\outputs\insights"
    "$avilaRoot\logs"
    "$avilaRoot\config"
    "$avilaRoot\scripts"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force
    Write-Host "✓ Criado: $dir" -ForegroundColor Green
}
```

---

## 🐍 PASSO 2: Configurar Python Environment (5min)

```powershell
# Navegar para scripts
cd "C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\scripts"

# Criar virtual environment
python -m venv venv

# Ativar
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements-orchestrator.txt

# Isso vai levar ~5min (muitas libs)
# ☕ Aproveite para um café!
```

**Se der erro de execução de scripts:**
```powershell
# Executar como Admin
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🔑 PASSO 3: Configurar Variáveis de Ambiente (3min)

```powershell
# Criar arquivo .env
cd C:\Users\nicol\OneDrive\Avila

@"
# OpenAI
OPENAI_API_KEY=sk-proj-SUBSTITUA-AQUI

# Azure (opcional no início)
AZURE_SUBSCRIPTION_ID=
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=

# Caminhos
OBSIDIAN_VAULT_PATH=C:\Users\nicol\OneDrive\Documentos\Obsidian Vault
AVILA_DATA_PATH=C:\Users\nicol\OneDrive\Avila\data
AVILA_OUTPUTS_PATH=C:\Users\nicol\OneDrive\Avila\outputs

# Configurações
LOG_LEVEL=INFO
ENABLE_TELEMETRY=true
"@ | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "✓ Arquivo .env criado" -ForegroundColor Green
Write-Host "⚠️  EDITE .env e adicione sua OPENAI_API_KEY!" -ForegroundColor Yellow
```

**Obter OpenAI API Key:**
1. Acesse: https://platform.openai.com/api-keys
2. Login/Cadastro
3. "Create new secret key"
4. Copie e cole no `.env`

---

## 🧪 PASSO 4: Testar Instalação (5min)

Criar arquivo de teste:

```powershell
# Criar test_setup.py
cd C:\Users\nicol\OneDrive\Avila\scripts

@"
#!/usr/bin/env python3
"""Teste de setup do ambiente Ávila"""

import sys
print("="*60)
print("TESTE DE AMBIENTE ÁVILA")
print("="*60)

# 1. Python version
print(f"\n1. Python: {sys.version}")
assert sys.version_info >= (3, 11), "❌ Python 3.11+ necessário"
print("   ✓ Versão OK")

# 2. Dependências críticas
critical_libs = [
    'pandas', 'numpy', 'sklearn', 'openai',
    'networkx', 'yaml', 'dotenv'
]

print("\n2. Dependências:")
for lib in critical_libs:
    try:
        __import__(lib)
        print(f"   ✓ {lib}")
    except ImportError:
        print(f"   ❌ {lib} - FALTANDO!")
        sys.exit(1)

# 3. OpenAI API
print("\n3. OpenAI API:")
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
if api_key and api_key.startswith('sk-'):
    print(f"   ✓ API Key configurada ({api_key[:10]}...)")

    # Testar chamada
    import openai
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': 'Say hi'}],
            max_tokens=10
        )
        print(f"   ✓ API funcional: {response.choices[0].message.content}")
    except Exception as e:
        print(f"   ⚠️  Erro na API: {e}")
else:
    print("   ❌ OPENAI_API_KEY não configurada!")

# 4. Paths
print("\n4. Caminhos:")
paths = {
    'Obsidian Vault': os.getenv('OBSIDIAN_VAULT_PATH'),
    'Ávila Data': os.getenv('AVILA_DATA_PATH'),
    'Ávila Outputs': os.getenv('AVILA_OUTPUTS_PATH')
}

for name, path in paths.items():
    if path and os.path.exists(path):
        print(f"   ✓ {name}: {path}")
    else:
        print(f"   ❌ {name}: NÃO ENCONTRADO")

print("\n" + "="*60)
print("TESTE COMPLETO!")
print("="*60)
"@ | Out-File -FilePath "test_setup.py" -Encoding UTF8

# Executar teste
python test_setup.py
```

**Resultado esperado:**
```
============================================================
TESTE DE AMBIENTE ÁVILA
============================================================

1. Python: 3.11.x
   ✓ Versão OK

2. Dependências:
   ✓ pandas
   ✓ numpy
   ✓ sklearn
   ✓ openai
   ✓ networkx
   ✓ yaml
   ✓ dotenv

3. OpenAI API:
   ✓ API Key configurada (sk-proj-XX...)
   ✓ API funcional: Hi there!

4. Caminhos:
   ✓ Obsidian Vault: C:\Users\nicol\...
   ✓ Ávila Data: C:\Users\nicol\OneDrive\Avila\data
   ✓ Ávila Outputs: C:\Users\nicol\OneDrive\Avila\outputs

============================================================
TESTE COMPLETO!
============================================================
```

---

## 🎯 PASSO 5: Primeira Execução - Pipeline Básico (10min)

Criar script minimalista que processa 10 documentos:

```powershell
cd C:\Users\nicol\OneDrive\Avila\scripts

@"
#!/usr/bin/env python3
"""
Pipeline MVP - Processa subset de documentos Obsidian
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

# Configuração
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

VAULT_PATH = Path(os.getenv('OBSIDIAN_VAULT_PATH'))
OUTPUT_PATH = Path(os.getenv('AVILA_OUTPUTS_PATH'))

def collect_sample_docs(n=10):
    '''Coleta primeiros N arquivos .md'''
    docs = []
    for md_file in VAULT_PATH.rglob('*.md'):
        # Ignorar pastas de sistema
        if any(x in str(md_file) for x in ['.obsidian', '_system', 'scripts']):
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            docs.append({
                'path': str(md_file),
                'title': md_file.stem,
                'content': content[:1000],  # Primeiros 1000 chars
                'size': len(content)
            })

            if len(docs) >= n:
                break
        except Exception as e:
            print(f"Erro lendo {md_file}: {e}")

    return docs

def generate_embedding(text):
    '''Gera embedding OpenAI'''
    response = client.embeddings.create(
        input=text,
        model='text-embedding-3-small'
    )
    return response.data[0].embedding

def categorize_document(content):
    '''Categoriza documento com GPT-3.5'''
    categories = ['Trabalho', 'Aprendizado', 'Ferramentas', 'Ideias', 'Referência']

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{
            'role': 'user',
            'content': f'''Categorize este documento em UMA categoria:
{', '.join(categories)}

Documento: {content[:300]}

Responda apenas com o nome da categoria.'''
        }],
        max_tokens=10,
        temperature=0
    )

    category = response.choices[0].message.content.strip()
    return category if category in categories else 'Uncategorized'

def cosine_similarity(v1, v2):
    '''Calcula similaridade cosseno'''
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main():
    print("🚀 ÁVILA MVP - Pipeline Básico\n")
    print("="*60)

    # 1. Coletar documentos
    print("\n📁 [1/4] Coletando documentos...")
    docs = collect_sample_docs(n=10)
    print(f"   ✓ {len(docs)} documentos coletados")

    # 2. Gerar embeddings
    print("\n🧬 [2/4] Gerando embeddings...")
    for i, doc in enumerate(docs):
        print(f"   Processando {i+1}/{len(docs)}: {doc['title'][:40]}...")
        doc['embedding'] = generate_embedding(doc['content'])
    print("   ✓ Embeddings gerados")

    # 3. Categorizar
    print("\n🏷️  [3/4] Categorizando documentos...")
    for doc in docs:
        doc['category'] = categorize_document(doc['content'])
        print(f"   {doc['title'][:30]:<30} → {doc['category']}")

    # 4. Detectar duplicatas
    print("\n🔍 [4/4] Detectando duplicatas...")
    duplicates = []
    for i in range(len(docs)):
        for j in range(i+1, len(docs)):
            sim = cosine_similarity(docs[i]['embedding'], docs[j]['embedding'])
            if sim > 0.85:
                duplicates.append({
                    'doc1': docs[i]['title'],
                    'doc2': docs[j]['title'],
                    'similarity': sim
                })
                print(f"   ⚠️  {docs[i]['title'][:20]} ≈ {docs[j]['title'][:20]} ({sim:.2%})")

    if not duplicates:
        print("   ✓ Nenhuma duplicata encontrada")

    # 5. Salvar resultados
    print("\n💾 Salvando resultados...")

    # Remover embeddings (muito grandes para JSON)
    for doc in docs:
        doc.pop('embedding')

    output = {
        'processed_at': str(Path.ctime(Path.cwd())),
        'total_docs': len(docs),
        'documents': docs,
        'duplicates': duplicates,
        'categories_count': {cat: sum(1 for d in docs if d['category']==cat)
                            for cat in set(d['category'] for d in docs)}
    }

    output_file = OUTPUT_PATH / 'reports' / 'mvp_results.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"   ✓ Resultados salvos em: {output_file}")

    # 6. Resumo
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    print(f"Documentos processados:  {len(docs)}")
    print(f"Duplicatas encontradas:  {len(duplicates)}")
    print("\nCategorias:")
    for cat, count in output['categories_count'].items():
        print(f"  {cat:<20} {count:>3}")
    print("="*60)
    print("\n✅ Pipeline MVP concluído com sucesso!")
    print(f"\n📄 Veja resultados completos em:\n   {output_file}")

if __name__ == '__main__':
    main()
"@ | Out-File -FilePath "mvp_pipeline.py" -Encoding UTF8

# Executar!
python mvp_pipeline.py
```

**Output esperado:**
```
🚀 ÁVILA MVP - Pipeline Básico

============================================================

📁 [1/4] Coletando documentos...
   ✓ 10 documentos coletados

🧬 [2/4] Gerando embeddings...
   Processando 1/10: Atlas...
   Processando 2/10: Configuração de ambientes IDE...
   ...
   ✓ Embeddings gerados

🏷️  [3/4] Categorizando documentos...
   Atlas                          → Aprendizado
   Configuração de ambientes IDE  → Ferramentas
   ...

🔍 [4/4] Detectando duplicatas...
   ✓ Nenhuma duplicata encontrada

💾 Salvando resultados...
   ✓ Resultados salvos em: C:\...\mvp_results.json

============================================================
📊 RESUMO
============================================================
Documentos processados:  10
Duplicatas encontradas:  0

Categorias:
  Aprendizado          3
  Ferramentas          4
  Trabalho             2
  Ideias               1
============================================================

✅ Pipeline MVP concluído com sucesso!
```

---

## 🎉 PASSO 6: Verificar Resultados (2min)

```powershell
# Abrir resultados
code C:\Users\nicol\OneDrive\Avila\outputs\reports\mvp_results.json
```

Você verá algo como:
```json
{
  "processed_at": "2025-11-10 15:30:00",
  "total_docs": 10,
  "documents": [
    {
      "path": "C:\\Users\\nicol\\...",
      "title": "Atlas",
      "content": "...",
      "size": 1523,
      "category": "Aprendizado"
    },
    ...
  ],
  "duplicates": [],
  "categories_count": {
    "Aprendizado": 3,
    "Ferramentas": 4,
    "Trabalho": 2,
    "Ideias": 1
  }
}
```

---

## 📈 PASSO 7: Próximos Passos

Agora que o MVP funciona, você pode:

### **Opção A: Processar Vault Completo**
```powershell
# Editar mvp_pipeline.py
# Mudar linha: docs = collect_sample_docs(n=10)
# Para:        docs = collect_sample_docs(n=1000)  # ou sem limite

python mvp_pipeline.py
```

### **Opção B: Executar Orchestrator Completo**
```powershell
# Copiar config.yaml para Ávila
Copy-Item "C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\scripts\config.yaml" `
          "C:\Users\nicol\OneDrive\Avila\config\"

# Atualizar paths no config.yaml
code C:\Users\nicol\OneDrive\Avila\config\config.yaml

# Executar orchestrator
cd C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\scripts
python avila_orchestrator.py
```

### **Opção C: Setup ActivityWatch Integration**
```powershell
# Instalar ActivityWatch (se ainda não tiver)
winget install ActivityWatch.ActivityWatch

# Localizar banco de dados
# Tipicamente em: C:\Users\nicol\AppData\Local\activitywatch\aw-server\

# Criar script de extração (próximo sprint)
```

### **Opção D: Azure CLI Integration**
```powershell
# Login Azure
az login

# Testar query
az monitor metrics list --resource <resource-id>

# Criar script de coleta (próximo sprint)
```

---

## 📚 RECURSOS

### **Documentação Criada:**
1. `AVILA_ORCHESTRATION_MASTER.md` - Visão geral da arquitetura
2. `IMPLEMENTATION_ROADMAP.md` - Roadmap detalhado (13 sprints)
3. `MATHEMATICAL_FOUNDATIONS.md` - Matemática por trás dos modelos
4. `PHILOSOPHY_AND_SECTORS.md` - Filosofia e sequência de setores
5. Este arquivo (`QUICK_START.md`)

### **Scripts Criados:**
1. `avila_orchestrator.py` - Orchestrador principal
2. `mvp_pipeline.py` - Pipeline minimalista
3. `test_setup.py` - Teste de ambiente
4. `requirements-orchestrator.txt` - Dependências

### **Onde Buscar Ajuda:**
- **GitHub Copilot:** Pergunte sobre qualquer parte do código
- **OpenAI Docs:** https://platform.openai.com/docs
- **Azure Docs:** https://learn.microsoft.com/azure
- **LangChain:** https://python.langchain.com/docs

---

## 🐛 TROUBLESHOOTING

### **Erro: `ModuleNotFoundError`**
```powershell
# Certifique-se que está no venv
.\venv\Scripts\Activate.ps1

# Reinstalar dependências
pip install -r requirements-orchestrator.txt
```

### **Erro: OpenAI API rate limit**
```python
# Adicionar retry logic
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(min=1, max=60))
def generate_embedding(text):
    # código original
```

### **Erro: Memória insuficiente (embeddings grandes)**
```python
# Processar em batches menores
BATCH_SIZE = 50  # ao invés de processar tudo de uma vez

for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i:i+BATCH_SIZE]
    process_batch(batch)
```

### **Erro: Azure CLI não autenticado**
```powershell
az login --tenant <seu-tenant-id>
az account set --subscription <seu-subscription-id>
```

---

## ✅ CHECKLIST FINAL

Antes de prosseguir para o Roadmap completo, confirme:

- [ ] Python 3.11+ instalado
- [ ] Virtual environment criado e ativado
- [ ] Dependências instaladas (`pip list` mostra tudo)
- [ ] `.env` configurado com OPENAI_API_KEY
- [ ] `test_setup.py` passa sem erros
- [ ] `mvp_pipeline.py` processa 10 documentos com sucesso
- [ ] Resultados salvos em `Avila/outputs/reports/`
- [ ] Documentação lida (pelo menos ORCHESTRATION_MASTER)

**Tudo OK? 🎉**

Próximo passo: Implementar **Sprint 1** do Roadmap!

```powershell
code "C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\On\IMPLEMENTATION_ROADMAP.md"
```

---

## 🚀 COMANDOS RÁPIDOS (Copiar & Colar)

```powershell
# Setup completo em 1 comando (executar linha por linha)
cd C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\scripts
.\venv\Scripts\Activate.ps1
python test_setup.py
python mvp_pipeline.py
code C:\Users\nicol\OneDrive\Avila\outputs\reports\mvp_results.json
```

---

**💡 Dica:** Adicione alias no PowerShell para ativar venv rapidamente:

```powershell
# Adicionar ao perfil do PowerShell
code $PROFILE

# Adicionar esta linha:
function avila { cd C:\Users\nicol\OneDrive\Documentos\Obsidian Vault\scripts; .\venv\Scripts\Activate.ps1 }

# Agora você pode simplesmente digitar:
avila
```

---

**Boa orquestração! 🎼**
