import os
from pathlib import Path
import yaml

# Diretório base
BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / "agents"

# Dicionário com todos os agentes
agents = {
    "atlas": {
        "area": "Estratégia / Corporativo",
        "significado": "Sustenta a base da operação",
    },
    "helix": {
        "area": "Engenharia / DevOps",
        "significado": "DNA técnico e automação",
    },
    "sigma": {
        "area": "Financeiro / Controladoria",
        "significado": "Análise e precisão matemática",
    },
    "vox": {
        "area": "Comercial / CRM",
        "significado": "Voz da empresa",
    },
    "lumen": {
        "area": "Pesquisa e IA aplicada",
        "significado": "Clareza, insight",
    },
    "forge": {
        "area": "Produção / Indústria",
        "significado": "Forja, criação e manufatura",
    },
    "lex": {
        "area": "Jurídico / Compliance",
        "significado": "Lei e padronização",
    },
    "echo": {
        "area": "Comunicação / Branding",
        "significado": "Replica a mensagem da marca",
    },
}

# Criação das pastas e arquivos
for nome, info in agents.items():
    agent_path = AGENTS_DIR / nome
    agent_path.mkdir(parents=True, exist_ok=True)

    # Criar config.yaml
    config_data = {
        "agent_name": nome.capitalize(),
        "area": info["area"],
        "significado": info["significado"],
        "status": "ativo",
        "model": "gpt-4o",
        "memory_path": f"../../data/{nome}_memory.json",
        "description": f"Agente especializado em {info['area'].lower()} ({info['significado'].lower()}).",
        "version": "1.0.0",
        "permissions": {
            "read": ["../../data/knowledge_base"],
            "write": ["../../logs"],
            "sync": True
        }
    }

    with open(agent_path / "config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)

    # Criar README.md
    readme_content = f"""# {nome.capitalize()} Agent

**Área:** {info['area']}  
**Significado:** {info['significado']}

## Função
Agente da suíte **On** especializado em {info['area'].lower()}.
Responsável por aplicar inteligência autônoma para {info['significado'].lower()}.

## Configuração
Arquivo: `config.yaml`  
Modelo: GPT-4o  
Status: Ativo
"""

    (agent_path / "README.md").write_text(readme_content, encoding="utf-8")

print(f"✅ {len(agents)} agentes configurados em {AGENTS_DIR}")
