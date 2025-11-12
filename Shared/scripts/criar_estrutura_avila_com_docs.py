#!/usr/bin/env python3
import os
from pathlib import Path

BASE_DIR = Path(input("Digite o caminho onde deseja criar a estrutura da Ávila (ex.: C:\\Users\\Você\\Documents\\Avila): ").strip())

ESTRUTURA = {
    "AvilaInc": [
        "docs", "legal", "finance",
        "marketing/brand", "marketing/campaigns", "marketing/website", "marketing/social_media",
        "governance_framework/_modelos", "governance_framework/_anexos", "governance_framework/filosofia",
        "governance_framework/parametros", "governance_framework/tecnicas", "governance_framework/procedimentos",
        "governance_framework/funcoes", "governance_framework/revisao", "governance_framework/versoes", "governance_framework/capturas"
    ],
    "AvilaOps": [
        "infra/azure", "infra/aws", "infra/hetzner", "infra/docker", "infra/kubernetes",
        "devops/pipelines", "devops/monitoring", "devops/security", "devops/backups",
        "ai/rag", "ai/fine_tuning", "ai/prompts", "ai/datasets", "ai/notebooks",
        "data/ingestion", "data/processing", "data/warehouse", "data/dashboards",
        "products/opsflow", "products/pulse", "products/coredesk", "products/mindlayer", "products/insight",
        "docs/api", "docs/architecture", "docs/security_policies", "docs/styleguides",
        "governance", "research"
    ],
    "Shared": [
        "templates", "assets", "scripts", "backups"
    ]
}

README_MODELO = {
    "AvilaInc": """# Ávila Inc
Matriz institucional e estratégica. 
Abriga a governança, finanças, jurídico, marketing e documentação corporativa.""",

    "AvilaOps": """# Ávila Ops
Núcleo técnico e operacional. 
Contém infraestrutura, DevOps, IA, produtos e pesquisa aplicada.""",

    "Shared": """# Shared
Recursos compartilhados entre Ávila Inc e Ávila Ops.
Contém templates, assets, scripts e backups gerais."""
}

PROCEDIMENTOS_GERAIS = """# Procedimentos Técnicos e de Boas Práticas

## Padrão geral
- Trabalhar com versionamento (Git).
- Documentar decisões técnicas e operacionais no Obsidian.
- Cada modificação relevante deve possuir log de commit explicativo.

## Conduta e cultura
- Transparência: todos os processos são documentados.
- Revisão semanal: cada setor reporta aprendizados.
- Colaboração: dúvidas ou melhorias devem ser registradas como sugestão formal.

## Padrão de código
- Seguir convenções PEP8 (Python) e ESLint (JS/TS).
- Configurações e senhas nunca são comitadas em repositórios.
- Utilizar arquivos `.env` e exemplos `env.example`.

## Estrutura por setor
- **Infraestrutura:** gerencia ambientes, redes e segurança cloud.
- **DevOps:** cuida de pipelines, deploys, monitoramento e automações.
- **IA:** cria agentes, embeddings e integrações cognitivas.
- **Dados:** coleta, transforma e analisa informações de negócio.
- **Produtos:** mantém os sistemas finais, interfaces e APIs.
- **Governança:** supervisiona processos e conformidade.
"""

def criar_estrutura(base: Path, estrutura: dict):
    base.mkdir(parents=True, exist_ok=True)

    for raiz, subpastas in estrutura.items():
        raiz_dir = base / raiz
        raiz_dir.mkdir(parents=True, exist_ok=True)

        # Cria README principal de cada área (Inc, Ops, Shared)
        readme_path = raiz_dir / "README.md"
        if not readme_path.exists():
            readme_path.write_text(README_MODELO[raiz])

        for subpasta in subpastas:
            caminho = raiz_dir / subpasta
            caminho.mkdir(parents=True, exist_ok=True)

            # README automático em cada subpasta
            readme_sub = caminho / "README.md"
            if not readme_sub.exists():
                readme_sub.write_text(f"# {subpasta.capitalize()}\n\nEsta pasta pertence à área **{raiz}**.\n\nFunção: manter arquivos e documentos relativos a `{subpasta}`.\n")

    # cria README geral na raiz
    readme_geral = base / "README.md"
    readme_geral.write_text("# Estrutura Corporativa Ávila\n\nEste repositório contém a organização completa da Ávila Inc e Ávila Ops.\n")
    
    # cria arquivo de boas práticas globais
    boas_praticas = base / "PROCEDIMENTOS_GERAIS.md"
    boas_praticas.write_text(PROCEDIMENTOS_GERAIS)

    # cria .gitignore global
    gitignore = base / ".gitignore"
    gitignore.write_text("""# Padrão geral
__pycache__/
*.pyc
*.pyo
*.env
.env
node_modules/
logs/
backups/
.idea/
.vscode/
.DS_Store
""")

    print("\n✅ Estrutura da Ávila criada com arquivos e orientações iniciais.")

if __name__ == "__main__":
    criar_estrutura(BASE_DIR, ESTRUTURA)
