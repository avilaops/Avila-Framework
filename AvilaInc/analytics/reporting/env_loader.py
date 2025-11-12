"""
Helper para carregar variáveis de ambiente do arquivo .env
"""
from pathlib import Path


def load_env(env_file: Path = None) -> None:
    """Carrega variáveis de ambiente do arquivo .env se existir."""
    if env_file is None:
        env_file = Path(__file__).resolve().parents[2] / ".env"
    
    if not env_file.exists():
        return
    
    import os
    
    with env_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                # Remove aspas se presentes
                if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    value = value[1:-1]
                
                os.environ[key] = value
