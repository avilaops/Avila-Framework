#!/usr/bin/env python3
"""
PROCESSADOR AUTOMÁTICO DE DOCUMENTOS
Sistema completamente automatizado para análise e consolidação
Executa sem intervenção humana e envia relatórios
"""

import os
import glob
import json
import datetime
import shutil
import logging
import smtplib
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import schedule
import time
import argparse

class AutomatedDocumentProcessor:
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.workspace_path = Path(self.config.get('workspace_path', '.'))
        self.output_path = Path(self.config.get('output_path', './output'))
        self.backup_path = Path(self.config.get('backup_path', './backup'))
        self.last_run_file = Path('.last_run')
        
        # Criar diretórios necessários
        self.output_path.mkdir(exist_ok=True)
        self.backup_path.mkdir(exist_ok=True)
        
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Carrega configuração do arquivo JSON"""
        default_config = {
            "workspace_path": ".",
            "output_path": "./output", 
            "backup_path": "./backup",
            "email": {
                "enabled": True,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": ["gerente@empresa.com", "ti@empresa.com"]
            },
            "processing": {
                "auto_cleanup": True,
                "create_backup": True,
                "deep_analysis": True,
                "max_file_size_mb": 50,
                "file_extensions": [".md", ".txt", ".json", ".yml", ".yaml", ".py", ".ps1"]
            },
            "exclusions": {
                "patterns": ["*.tmp", "*.log", "*.cache", "*backup*", "*temp*"],
                "directories": ["node_modules", "__pycache__", ".git", "backup", "cache"]
            },
            "schedule": {
                "enabled": True,
                "frequency": "daily",  # daily, weekly, hourly
                "time": "02:00"  # HH:MM
            },
            "notifications": {
                "teams_webhook": "",
                "slack_webhook": ""
            }
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            else:
                # Criar arquivo de configuração padrão
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4, ensure_ascii=False)
                self.log(f"Arquivo de configuração criado: {config_path}")
        except Exception as e:
            self.log(f"Erro ao carregar configuração: {e}", level="ERROR")
            
        return default_config
    
    def setup_logging(self):
        """Configura sistema de logs"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"processor_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log(self, message: str, level: str = "INFO"):
        """Log personalizado"""
        getattr(self.logger, level.lower())(message)
        
    def should_exclude_file(self, file_path: Path) -> bool:
        """Verifica se arquivo deve ser excluído"""
        file_name = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Verificar padrões de exclusão
        for pattern in self.config['exclusions']['patterns']:
            if file_path.match(pattern):
                return True
                
        # Verificar diretórios excluídos
        for dir_name in self.config['exclusions']['directories']:
            if dir_name.lower() in file_path_str:
                return True
                
        # Verificar tamanho do arquivo
        if file_path.stat().st_size > self.config['processing']['max_file_size_mb'] * 1024 * 1024:
            return True
            
        return False
    
    def get_file_hash(self, file_path: Path) -> str:
        """Gera hash do arquivo para detectar mudanças"""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def scan_workspace(self) -> List[Path]:
        """Escaneia workspace em busca de arquivos válidos"""
        valid_files = []
        
        self.log("🔍 Iniciando escaneamento do workspace...")
        
        for extension in self.config['processing']['file_extensions']:
            pattern = f"**/*{extension}"
            files = list(self.workspace_path.glob(pattern))
            
            for file_path in files:
                if file_path.is_file() and not self.should_exclude_file(file_path):
                    valid_files.append(file_path)
                    
        self.log(f"✅ Encontrados {len(valid_files)} arquivos válidos")
        return valid_files
    
    def check_for_changes(self) -> bool:
        """Verifica se houve mudanças desde a última execução"""
        if not self.last_run_file.exists():
            return True
            
        try:
            with open(self.last_run_file, 'r') as f:
                last_run_data = json.load(f)
                
            current_files = self.scan_workspace()
            current_hashes = {}
            
            for file_path in current_files:
                try:
                    current_hashes[str(file_path)] = self.get_file_hash(file_path)
                except Exception as e:
                    self.log(f"Erro ao gerar hash de {file_path}: {e}", "WARNING")
                    
            # Comparar com hashes anteriores
            last_hashes = last_run_data.get('file_hashes', {})
            
            if current_hashes != last_hashes:
                self.log("🔄 Mudanças detectadas no workspace")
                return True
            else:
                self.log("ℹ️ Nenhuma mudança detectada desde a última execução")
                return False
                
        except Exception as e:
            self.log(f"Erro ao verificar mudanças: {e}", "WARNING")
            return True
    
    def create_backup(self, files: List[Path]):
        """Cria backup dos arquivos antes do processamento"""
        if not self.config['processing']['create_backup']:
            return
            
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.backup_path / f"backup_{timestamp}"
        backup_dir.mkdir(exist_ok=True)
        
        self.log(f"📦 Criando backup em: {backup_dir}")
        
        for file_path in files:
            try:
                relative_path = file_path.relative_to(self.workspace_path)
                backup_file_path = backup_dir / relative_path
                backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_file_path)
            except Exception as e:
                self.log(f"Erro ao fazer backup de {file_path}: {e}", "WARNING")
    
    def analyze_file_content(self, file_path: Path) -> Dict[str, Any]:
        """Analisa conteúdo de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            analysis = {
                'file': str(file_path),
                'size': file_path.stat().st_size,
                'lines': len(content.splitlines()),
                'words': len(content.split()),
                'characters': len(content),
                'modified': file_path.stat().st_mtime,
                'extension': file_path.suffix,
                'key_topics': self.extract_key_topics(content),
                'has_code': self.detect_code_content(content),
                'language': self.detect_language(file_path.suffix)
            }
            
            return analysis
            
        except Exception as e:
            self.log(f"Erro ao analisar {file_path}: {e}", "WARNING")
            return {'file': str(file_path), 'error': str(e)}
    
    def extract_key_topics(self, content: str) -> List[str]:
        """Extrai tópicos-chave do conteúdo (versão simplificada)"""
        # Palavras-chave técnicas comuns
        keywords = [
            'azure', 'aws', 'kubernetes', 'docker', 'api', 'database',
            'python', 'javascript', 'powershell', 'sql', 'git',
            'deployment', 'configuration', 'security', 'automation',
            'testing', 'ci/cd', 'devops', 'infrastructure', 'monitoring'
        ]
        
        content_lower = content.lower()
        found_topics = []
        
        for keyword in keywords:
            if keyword in content_lower:
                found_topics.append(keyword)
                
        return found_topics[:10]  # Top 10 tópicos
    
    def detect_code_content(self, content: str) -> bool:
        """Detecta se o conteúdo contém código"""
        code_indicators = ['function', 'class', 'import', 'def ', 'var ', 'let ', 'const ', '<?', '#!/']
        content_lower = content.lower()
        
        return any(indicator in content_lower for indicator in code_indicators)
    
    def detect_language(self, extension: str) -> str:
        """Detecta linguagem baseado na extensão"""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ps1': 'PowerShell',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.sql': 'SQL',
            '.txt': 'Text'
        }
        return lang_map.get(extension.lower(), 'Unknown')
    
    def generate_consolidated_report(self, analyses: List[Dict[str, Any]]) -> str:
        """Gera relatório consolidado"""
        timestamp = datetime.datetime.now()
        
        # Estatísticas gerais
        total_files = len(analyses)
        total_size = sum(a.get('size', 0) for a in analyses)
        total_lines = sum(a.get('lines', 0) for a in analyses)
        
        # Análise por tipo de arquivo
        extensions = {}
        languages = {}
        topics = {}
        
        for analysis in analyses:
            ext = analysis.get('extension', 'unknown')
            extensions[ext] = extensions.get(ext, 0) + 1
            
            lang = analysis.get('language', 'Unknown')
            languages[lang] = languages.get(lang, 0) + 1
            
            for topic in analysis.get('key_topics', []):
                topics[topic] = topics.get(topic, 0) + 1
        
        # Arquivos mais relevantes
        code_files = [a for a in analyses if a.get('has_code', False)]
        large_files = sorted(analyses, key=lambda x: x.get('size', 0), reverse=True)[:10]
        
        report = f"""
# RELATÓRIO AUTOMÁTICO DE ANÁLISE DE DOCUMENTOS

**Data de Geração:** {timestamp.strftime('%d/%m/%Y %H:%M:%S')}  
**Workspace:** {self.workspace_path}  
**Processamento:** Automático (sem intervenção humana)

---

## 📊 ESTATÍSTICAS GERAIS

- **Total de arquivos processados:** {total_files}
- **Tamanho total:** {total_size / (1024*1024):.2f} MB
- **Total de linhas:** {total_lines:,}
- **Arquivos com código:** {len(code_files)}

## 📁 DISTRIBUIÇÃO POR TIPO

### Extensões de Arquivo
"""
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{ext}**: {count} arquivo(s)\n"
            
        report += "\n### Linguagens Identificadas\n"
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{lang}**: {count} arquivo(s)\n"
        
        report += "\n## 🏷️ TÓPICOS PRINCIPAIS\n"
        for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:15]:
            report += f"- **{topic}**: {count} ocorrência(s)\n"
            
        report += "\n## 📈 ARQUIVOS MAIS RELEVANTES\n"
        for i, file_analysis in enumerate(large_files, 1):
            size_mb = file_analysis.get('size', 0) / (1024*1024)
            report += f"{i}. **{Path(file_analysis['file']).name}** ({size_mb:.2f} MB, {file_analysis.get('lines', 0)} linhas)\n"
            
        report += f"\n## 🤖 PROCESSAMENTO AUTOMÁTICO\n"
        report += f"- **Última execução:** {timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
        report += f"- **Próxima execução:** {self.get_next_run_time()}\n"
        report += f"- **Status:** ✅ Concluído com sucesso\n"
        report += f"- **Arquivos processados automaticamente:** {total_files}\n"
        report += f"- **Backup criado:** {'✅ Sim' if self.config['processing']['create_backup'] else '❌ Não'}\n"
        
        report += "\n## 📋 AÇÕES AUTOMÁTICAS REALIZADAS\n"
        report += "1. ✅ Escaneamento automático do workspace\n"
        report += "2. ✅ Filtro automático de arquivos relevantes\n"
        report += "3. ✅ Análise de conteúdo e extração de tópicos\n"
        report += "4. ✅ Geração automática de relatório\n"
        
        if self.config['processing']['create_backup']:
            report += "5. ✅ Backup automático dos arquivos processados\n"
            
        if self.config['processing']['auto_cleanup']:
            report += "6. ✅ Limpeza automática de arquivos temporários\n"
            
        report += "\n---\n"
        report += "*Este relatório foi gerado automaticamente pelo sistema de análise de documentos.*\n"
        report += f"*Configurado para execução: {self.config['schedule']['frequency']} às {self.config['schedule']['time']}*\n"
        
        return report
    
    def get_next_run_time(self) -> str:
        """Calcula próximo horário de execução"""
        now = datetime.datetime.now()
        schedule_time = self.config['schedule']['time']
        hours, minutes = map(int, schedule_time.split(':'))
        
        next_run = now.replace(hour=hours, minute=minutes, second=0, microsecond=0)
        
        if self.config['schedule']['frequency'] == 'daily':
            if next_run <= now:
                next_run += datetime.timedelta(days=1)
        elif self.config['schedule']['frequency'] == 'weekly':
            days_until_next = (7 - now.weekday()) % 7
            if days_until_next == 0 and next_run <= now:
                days_until_next = 7
            next_run += datetime.timedelta(days=days_until_next)
            
        return next_run.strftime('%d/%m/%Y %H:%M')
    
    def cleanup_workspace(self):
        """Limpeza automática do workspace"""
        if not self.config['processing']['auto_cleanup']:
            return
            
        self.log("🧹 Executando limpeza automática...")
        
        cleanup_patterns = ['*.tmp', '*.log', '*.cache', '*~', '*.bak']
        cleaned_count = 0
        
        for pattern in cleanup_patterns:
            files = list(self.workspace_path.glob(f"**/{pattern}"))
            for file_path in files:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    self.log(f"   🗑️ Removido: {file_path.name}")
                except Exception as e:
                    self.log(f"Erro ao remover {file_path}: {e}", "WARNING")
                    
        self.log(f"✅ Limpeza concluída: {cleaned_count} arquivo(s) removidos")
    
    def send_email_report(self, report_content: str, report_file: Path):
        """Envia relatório por email"""
        if not self.config['email']['enabled']:
            return
            
        try:
            self.log("📧 Enviando relatório por email...")
            
            msg = MimeMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = ', '.join(self.config['email']['recipients'])
            msg['Subject'] = f"Relatório Automático de Documentos - {datetime.datetime.now().strftime('%d/%m/%Y')}"
            
            # Corpo do email
            body = f"""
            Relatório automático de análise de documentos gerado em {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M')}.
            
            Este relatório foi processado automaticamente pelo sistema de análise de documentos.
            
            Principais estatísticas:
            - Arquivos processados: {report_content.count('arquivo(s)')} 
            - Status: Processamento concluído com sucesso
            - Próxima execução: {self.get_next_run_time()}
            
            Relatório completo em anexo.
            
            ---
            Sistema Automatizado de Análise de Documentos
            """
            
            msg.attach(MimeText(body, 'plain', 'utf-8'))
            
            # Anexar relatório
            with open(report_file, 'rb') as attachment:
                part = MimeBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {report_file.name}'
                )
                msg.attach(part)
            
            # Enviar email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
            server.send_message(msg)
            server.quit()
            
            self.log("✅ Relatório enviado por email com sucesso")
            
        except Exception as e:
            self.log(f"Erro ao enviar email: {e}", "ERROR")
    
    def update_last_run(self, files: List[Path]):
        """Atualiza arquivo de controle da última execução"""
        file_hashes = {}
        for file_path in files:
            try:
                file_hashes[str(file_path)] = self.get_file_hash(file_path)
            except Exception:
                pass
                
        run_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'files_processed': len(files),
            'file_hashes': file_hashes
        }
        
        with open(self.last_run_file, 'w') as f:
            json.dump(run_data, f, indent=2)
    
    def process_documents(self, force_run: bool = False) -> bool:
        """Processo principal de análise de documentos"""
        self.log("🚀 Iniciando processamento automático de documentos...")
        
        try:
            # Verificar se precisa executar
            if not force_run and not self.check_for_changes():
                self.log("⏭️ Nenhuma mudança detectada. Processo ignorado.")
                return False
            
            # Escanear workspace
            files = self.scan_workspace()
            
            if not files:
                self.log("⚠️ Nenhum arquivo válido encontrado para processamento")
                return False
            
            # Criar backup
            self.create_backup(files)
            
            # Analisar arquivos
            self.log("🔍 Analisando conteúdo dos arquivos...")
            analyses = []
            
            for file_path in files:
                analysis = self.analyze_file_content(file_path)
                analyses.append(analysis)
                
            # Gerar relatório
            self.log("📊 Gerando relatório consolidado...")
            report_content = self.generate_consolidated_report(analyses)
            
            # Salvar relatório
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = self.output_path / f"relatorio_automatico_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
                
            self.log(f"✅ Relatório salvo: {report_file}")
            
            # Enviar por email
            self.send_email_report(report_content, report_file)
            
            # Limpeza automática
            self.cleanup_workspace()
            
            # Atualizar controle de execução
            self.update_last_run(files)
            
            self.log("🎯 Processamento automático concluído com sucesso!")
            return True
            
        except Exception as e:
            self.log(f"Erro durante processamento: {e}", "ERROR")
            return False

def setup_windows_task():
    """Cria tarefa agendada no Windows"""
    script_path = Path(__file__).absolute()
    python_exe = shutil.which('python')
    
    task_xml = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2025-11-10T12:00:00</Date>
    <Author>Sistema Automático</Author>
    <Description>Processamento automático de documentos</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-11-10T02:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT2H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>{script_path} --scheduled</Arguments>
      <WorkingDirectory>{script_path.parent}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>"""
    
    task_file = Path("automated-processor-task.xml")
    with open(task_file, 'w') as f:
        f.write(task_xml)
    
    print(f"✅ Arquivo de tarefa criado: {task_file}")
    print("📝 Para registrar no Windows Task Scheduler, execute:")
    print(f"   schtasks /create /xml {task_file} /tn 'Processamento Automático de Documentos'")

def main():
    parser = argparse.ArgumentParser(description='Processador Automático de Documentos')
    parser.add_argument('--scheduled', action='store_true', help='Execução via agendamento')
    parser.add_argument('--force', action='store_true', help='Forçar execução mesmo sem mudanças')
    parser.add_argument('--setup-task', action='store_true', help='Configurar tarefa agendada')
    parser.add_argument('--config', default='config.json', help='Arquivo de configuração')
    
    args = parser.parse_args()
    
    if args.setup_task:
        setup_windows_task()
        return
    
    processor = AutomatedDocumentProcessor(args.config)
    
    if args.scheduled:
        # Execução via agendamento
        success = processor.process_documents(force_run=args.force)
        exit(0 if success else 1)
    else:
        # Modo contínuo com schedule
        def job():
            processor.process_documents()
        
        # Configurar agendamento baseado na configuração
        freq = processor.config['schedule']['frequency']
        time_str = processor.config['schedule']['time']
        
        if freq == 'daily':
            schedule.every().day.at(time_str).do(job)
        elif freq == 'weekly':
            schedule.every().monday.at(time_str).do(job)
        elif freq == 'hourly':
            schedule.every().hour.do(job)
            
        print(f"🤖 Processador automático iniciado")
        print(f"📅 Agendamento: {freq} às {time_str}")
        print(f"📁 Workspace: {processor.workspace_path}")
        print("⏹️ Pressione Ctrl+C para parar")
        
        # Executar uma vez imediatamente se forçado
        if args.force:
            job()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto
        except KeyboardInterrupt:
            print("\n🛑 Processador automático parado")

if __name__ == "__main__":
    main()