# Gerador do archivus_main.py com encoding correto
import sys
from pathlib import Path

target = Path(r"C:\Users\nicol\OneDrive\Avila\AvilaOps\Agente Bibliotecario (Archivus)\archivus_main.py")

code = '''# coding: utf-8
import os, shutil, hashlib, json, yaml, zipfile
from pathlib import Path
from datetime import datetime, timedelta

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SCRIPT_DIR / "config.yaml"
WORKSPACE_ROOT = Path(r"C:\\Users\\nicol\\OneDrive\\Avila")

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)

DOCS_PATH = WORKSPACE_ROOT / "Docs"
LOGS_PATH = WORKSPACE_ROOT / "Logs"
SCRIPTS_PATH = WORKSPACE_ROOT / "Scripts"
BACKUP_PATH = WORKSPACE_ROOT / "Shared" / "backups" / "archivus"
MANIFEST_FILE = SCRIPT_DIR / CONFIG['integrity']['manifest_file']

BACKUP_PATH.mkdir(parents=True, exist_ok=True)
(LOGS_PATH / "Daily").mkdir(parents=True, exist_ok=True)
(LOGS_PATH / "Archive").mkdir(parents=True, exist_ok=True)

class Archivus:
    def __init__(self):
    self.config = CONFIG
        self.log_file = LOGS_PATH / "Daily" / f"archivus_{datetime.now().strftime('%Y-%m-%d')}.log"
     self.report_data = {'timestamp': datetime.now().isoformat(), 'actions': [], 'metrics': {}, 'issues': []}
    
    def log(self, message, level="INFO"):
 timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
      with open(self.log_file, 'a', encoding='utf-8') as f:
       f.write(log_entry + "\\n")
    
    def validate_structure(self):
        self.log("Validacao de estrutura...")
        removed = []
        relatorios = DOCS_PATH / "Relatorios"
     if relatorios.exists():
            official = CONFIG['official_structure']['Docs']['Relatorios']
       for item in relatorios.iterdir():
   if item.is_dir() and item.name not in official:
   self.log(f"Removendo pasta: {item.name}", "WARN")
     shutil.rmtree(item)
        removed.append(str(item.relative_to(WORKSPACE_ROOT)))
        self.report_data['actions'].append({'action': 'validate', 'removed': len(removed)})
        self.log(f"Validacao concluida. Removidos: {len(removed)}")
        return removed
    
    def rotate_logs(self):
        self.log("Rotacao de logs...")
        count = 0
        cutoff = datetime.now() - timedelta(days=30)
   for log in (LOGS_PATH / "Daily").glob("*.log"):
         if datetime.fromtimestamp(log.stat().st_mtime) < cutoff:
                shutil.move(str(log), str(LOGS_PATH / "Archive" / log.name))
          count += 1
        self.report_data['actions'].append({'action': 'rotate_logs', 'count': count})
   self.log(f"Rotacao concluida: {count} logs")
 
    def backup_scripts(self):
        self.log("Backup de scripts...")
        ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup = BACKUP_PATH / f"scripts_backup_{ts}.zip"
        with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as z:
       for root, dirs, files in os.walk(SCRIPTS_PATH):
           for file in files:
       fp = Path(root) / file
          z.write(fp, fp.relative_to(WORKSPACE_ROOT))
     size = backup.stat().st_size / 1024 / 1024
    self.report_data['actions'].append({'action': 'backup', 'file': backup.name, 'size_mb': round(size, 2)})
 self.log(f"Backup criado: {backup.name}")
        backups = sorted(BACKUP_PATH.glob("scripts_backup_*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
        for old in backups[30:]:
   old.unlink()
    
    def calculate_hash(self, path):
        h = hashlib.sha256()
 with open(path, 'rb') as f:
          while chunk := f.read(8192):
h.update(chunk)
        return h.hexdigest()
    
    def generate_integrity_manifest(self):
      self.log("Gerando manifesto...")
   manifest = {'generated_at': datetime.now().isoformat(), 'files': {}}
      for fp in SCRIPTS_PATH.rglob("*.py"):
            rp = str(fp.relative_to(WORKSPACE_ROOT))
    manifest['files'][rp] = {
     'hash': self.calculate_hash(fp),
    'size': fp.stat().st_size,
           'modified': datetime.fromtimestamp(fp.stat().st_mtime).isoformat()
            }
 with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
      json.dump(manifest, f, indent=2)
        self.log(f"Manifesto: {len(manifest['files'])} arquivos")
        self.report_data['metrics']['manifest_files'] = len(manifest['files'])
    
  def verify_integrity(self):
      if not MANIFEST_FILE.exists():
            self.log("Criando manifesto inicial...", "WARN")
   self.generate_integrity_manifest()
    return
        self.log("Verificando integridade...")
        with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
         manifest = json.load(f)
        issues = []
      for rp, data in manifest['files'].items():
            fp = WORKSPACE_ROOT / rp
        if not fp.exists():
     issues.append(f"Removido: {rp}")
elif self.calculate_hash(fp) != data['hash']:
        issues.append(f"Modificado: {rp}")
        if issues:
            self.log(f"ALERTA: {len(issues)} divergencias!", "ERROR")
            self.report_data['issues'].extend(issues)
        else:
            self.log("Integridade OK")
      self.report_data['metrics']['integrity_issues'] = len(issues)
    
    def collect_metrics(self):
        self.log("Coletando metricas...")
        files = sum(1 for _ in WORKSPACE_ROOT.rglob("*") if _.is_file())
        size = sum(f.stat().st_size for f in WORKSPACE_ROOT.rglob("*") if f.is_file()) / 1024 / 1024
 conversas = len(list((DOCS_PATH / "Relatorios" / "Conversas").glob("*.md")))
     logs = len(list((LOGS_PATH / "Archive").glob("*.log")))
        self.report_data['metrics'].update({
  'total_files': files,
          'total_size_mb': round(size, 2),
            'conversas': conversas,
    'archived_logs': logs
   })
        self.log(f"Metricas: {files} arquivos, {size:.2f} MB")
    
    def generate_report(self):
        self.log("Gerando relatorio...")
        rp = DOCS_PATH / "Relatorios" / "Auditorias" / f"AUDITORIA_ARCHIVUS_{datetime.now().strftime('%Y-%m-%d')}.md"
     rp.parent.mkdir(parents=True, exist_ok=True)
        m = self.report_data['metrics']
        content = f"""# Relatorio Archivus

**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Metricas

| Metrica | Valor |
|---------|-------|
| Arquivos | {m.get('total_files', 0)} |
| Tamanho | {m.get('total_size_mb', 0)} MB |
| Conversas | {m.get('conversas', 0)} |
| Logs | {m.get('archived_logs', 0)} |

## Acoes

"""
        for a in self.report_data['actions']:
    content += f"- {a['action']}: {a}\\n"
   if self.report_data['issues']:
            content += "\\n## Problemas\\n\\n"
        for i in self.report_data['issues']:
              content += f"- {i}\\n"
        else:
  content += "\\n## Status: OK\\n"
   with open(rp, 'w', encoding='utf-8') as f:
     f.write(content)
        self.log(f"Relatorio: {rp.name}")
    
 def run_daily_tasks(self):
        self.log("=" * 50)
        self.log("ARCHIVUS - ROTINA DIARIA")
        self.log("=" * 50)
        try:
            self.validate_structure()
         self.rotate_logs()
    self.backup_scripts()
        self.verify_integrity()
          self.collect_metrics()
            self.generate_report()
            self.log("=" * 50)
 self.log("ROTINA CONCLUIDA COM SUCESSO")
 self.log("=" * 50)
  except Exception as e:
      self.log(f"ERRO: {e}", "ERROR")
            raise

if __name__ == "__main__":
    archivus = Archivus()
    archivus.run_daily_tasks()
'''

try:
    target.write_text(code, encoding='utf-8')
    print(f"Arquivo criado com sucesso: {target}")
    print("Teste: python archivus_main.py")
except Exception as e:
    print(f"Erro: {e}")
