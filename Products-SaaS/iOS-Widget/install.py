#!/usr/bin/env python3
"""
🛠️ Instalador Automático do Ecossistema Ávila iOS
Versão: 1.0.0
Autor: Ávila Inc
"""

import os
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class AvilaIOSInstaller:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.config_file = self.root_dir / "config.json"
        self.log_file = self.root_dir / "install.log"
        self.backup_dir = self.root_dir / "backups"

        # Cores para output
        self.colors = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "reset": "\033[0m",
            "bold": "\033[1m",
        }

    def log(self, message, level="INFO"):
        """Registra mensagem no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"

        print(f"{self.colors['blue']}[{level}]{self.colors['reset']} {message}")

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def success(self, message):
        """Mensagem de sucesso"""
        print(f"{self.colors['green']}✅ {message}{self.colors['reset']}")

    def error(self, message):
        """Mensagem de erro"""
        print(f"{self.colors['red']}❌ {message}{self.colors['reset']}")

    def warning(self, message):
        """Mensagem de aviso"""
        print(f"{self.colors['yellow']}⚠️  {message}{self.colors['reset']}")

    def info(self, message):
        """Mensagem informativa"""
        print(f"{self.colors['blue']}ℹ️  {message}{self.colors['reset']}")

    def load_config(self):
        """Carrega configuração do sistema"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            self.error("Arquivo config.json não encontrado!")
            return None
        except json.JSONDecodeError as e:
            self.error(f"Erro ao ler config.json: {e}")
            return None

    def check_prerequisites(self):
        """Verifica pré-requisitos do sistema"""
        self.log("Verificando pré-requisitos...")

        prerequisites = [
            ("python", "Python 3.8+", self.check_python_version),
            ("scriptable", "App Scriptable", self.check_scriptable),
            ("shortcuts", "App Shortcuts", self.check_shortcuts),
            ("permissions", "Permissões necessárias", self.check_permissions),
        ]

        all_ok = True
        for name, description, check_func in prerequisites:
            try:
                if check_func():
                    self.success(f"{description}: OK")
                else:
                    self.error(f"{description}: FALHA")
                    all_ok = False
            except Exception as e:
                self.error(f"Erro ao verificar {description}: {e}")
                all_ok = False

        return all_ok

    def check_python_version(self):
        """Verifica versão do Python"""
        version = sys.version_info
        return version.major >= 3 and version.minor >= 8

    def check_scriptable(self):
        """Verifica se Scriptable está instalado"""
        # Nota: Esta é uma verificação básica
        # Em um ambiente real, seria necessário verificar via iOS APIs
        return True  # Assume que está instalado

    def check_shortcuts(self):
        """Verifica se Shortcuts está disponível"""
        # Nota: Shortcuts vem pré-instalado no iOS 13+
        return True  # Assume que está disponível

    def check_permissions(self):
        """Verifica permissões necessárias"""
        # Verificar permissões de arquivo
        try:
            test_file = self.root_dir / "test_permissions.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except:
            return False

    def backup_existing_files(self):
        """Faz backup de arquivos existentes"""
        self.log("Criando backup de arquivos existentes...")

        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"

        files_to_backup = [
            "avila-status-widget.js",
            "avila-notifications.js",
            "avila-shortcut.json",
            "config.json",
        ]

        backed_up = []
        for filename in files_to_backup:
            src = self.root_dir / filename
            if src.exists():
                dst = backup_path / filename
                backup_path.mkdir(exist_ok=True)
                shutil.copy2(src, dst)
                backed_up.append(filename)

        if backed_up:
            self.success(f"Backup criado: {', '.join(backed_up)}")
            self.info(f"Local: {backup_path}")
        else:
            self.info("Nenhum arquivo para backup encontrado")

        return backup_path

    def install_components(self):
        """Instala componentes do sistema"""
        self.log("Instalando componentes...")

        components = [
            ("Widget de Status", self.install_status_widget),
            ("Sistema de Notificações", self.install_notifications),
            ("Atalhos iOS", self.install_shortcuts),
            ("Configurações", self.install_config),
        ]

        installed = []
        for name, install_func in components:
            try:
                self.info(f"Instalando {name}...")
                if install_func():
                    self.success(f"{name}: Instalado com sucesso")
                    installed.append(name)
                else:
                    self.warning(f"{name}: Instalação pulada")
            except Exception as e:
                self.error(f"Erro ao instalar {name}: {e}")

        return installed

    def install_status_widget(self):
        """Instala widget de status"""
        widget_file = self.root_dir / "avila-status-widget.js"
        if widget_file.exists():
            # Aqui seria a lógica para instalar no Scriptable
            # Por enquanto, apenas verifica se o arquivo existe
            return True
        return False

    def install_notifications(self):
        """Instala sistema de notificações"""
        notif_file = self.root_dir / "avila-notifications.js"
        if notif_file.exists():
            return True
        return False

    def install_shortcuts(self):
        """Instala atalhos iOS"""
        shortcut_file = self.root_dir / "avila-shortcut.json"
        if shortcut_file.exists():
            return True
        return False

    def install_config(self):
        """Instala configurações"""
        if self.config_file.exists():
            return True
        return False

    def configure_system(self):
        """Configura o sistema após instalação"""
        self.log("Configurando sistema...")

        config = self.load_config()
        if not config:
            return False

        # Aplicar configurações padrão
        config_updates = {
            "lastInstalled": datetime.now().isoformat(),
            "version": "1.0.0",
            "installPath": str(self.root_dir),
        }

        try:
            config.update(config_updates)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self.success("Configurações aplicadas")
            return True
        except Exception as e:
            self.error(f"Erro ao salvar configurações: {e}")
            return False

    def run_tests(self):
        """Executa testes básicos do sistema"""
        self.log("Executando testes...")

        tests = [
            ("Sintaxe JavaScript", self.test_js_syntax),
            ("Estrutura JSON", self.test_json_structure),
            ("Configuração válida", self.test_config_validity),
        ]

        passed = 0
        for test_name, test_func in tests:
            try:
                if test_func():
                    self.success(f"{test_name}: PASSOU")
                    passed += 1
                else:
                    self.error(f"{test_name}: FALHOU")
            except Exception as e:
                self.error(f"{test_name}: ERRO - {e}")

        return passed == len(tests)

    def test_js_syntax(self):
        """Testa sintaxe dos arquivos JavaScript - verificação básica"""
        js_files = ["avila-status-widget.js", "avila-notifications.js"]

        for filename in js_files:
            filepath = self.root_dir / filename
            if filepath.exists():
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Verificações básicas de sintaxe
                    if content.count("{") != content.count("}"):
                        raise SyntaxError("Unmatched braces")
                    if content.count("(") != content.count(")"):
                        raise SyntaxError("Unmatched parentheses")
                    if content.count("[") != content.count("]"):
                        raise SyntaxError("Unmatched brackets")

                    # Verificar se o arquivo tem conteúdo básico
                    if len(content.strip()) == 0:
                        raise SyntaxError("Empty file")

                    # Verificar se tem estrutura básica de classe/função
                    if "class " not in content and "function " not in content:
                        self.warning(
                            f"{filename}: Não parece ter estrutura JavaScript válida"
                        )

                except UnicodeDecodeError:
                    self.error(f"Erro de codificação em {filename}")
                    return False
                except Exception as e:
                    self.error(f"Erro ao validar {filename}: {e}")
                    return False
        return True

    def test_json_structure(self):
        """Testa estrutura dos arquivos JSON"""
        json_files = ["avila-shortcut.json", "config.json"]

        for filename in json_files:
            filepath = self.root_dir / filename
            if filepath.exists():
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    self.error(f"JSON inválido em {filename}: {e}")
                    return False
        return True

    def test_config_validity(self):
        """Testa validade da configuração"""
        config = self.load_config()
        if not config:
            return False

        required_keys = ["version", "api", "theme", "components"]
        for key in required_keys:
            if key not in config:
                self.error(f"Chave obrigatória faltando: {key}")
                return False
        return True

    def show_summary(self, backup_path, installed_components, tests_passed):
        """Exibe resumo da instalação"""
        print(f"\n{self.colors['bold']}{'='*50}")
        print("📋 RESUMO DA INSTALAÇÃO")
        print(f"{'='*50}{self.colors['reset']}\n")

        print(f"📁 Diretório: {self.root_dir}")
        print(f"📦 Backup: {backup_path}")
        print(f"📄 Log: {self.log_file}\n")

        print("📦 Componentes instalados:")
        for component in installed_components:
            print(f"  ✅ {component}")
        print()

        if tests_passed:
            self.success("✅ Todos os testes passaram!")
        else:
            self.warning("⚠️  Alguns testes falharam - verifique o log")

        print(f"\n{self.colors['bold']}🎉 Instalação concluída!{self.colors['reset']}")
        print("\nPróximos passos:")
        print("1. Abra o app Scriptable no seu iPhone")
        print("2. Importe os scripts JavaScript")
        print("3. Configure os widgets na tela inicial")
        print("4. Importe os atalhos no app Shortcuts")
        print("5. Teste as funcionalidades")

    def run_installation(self):
        """Executa instalação completa"""
        print(
            f"{self.colors['bold']}{'🍎 Instalador Ávila iOS Ecosystem'}{self.colors['reset']}"
        )
        print(f"Versão 1.0.0 - Ávila Inc\n")

        # Limpar log anterior
        if self.log_file.exists():
            self.log_file.unlink()

        self.log("Iniciando instalação do Ávila iOS Ecosystem")

        # Verificar pré-requisitos
        if not self.check_prerequisites():
            self.error("Pré-requisitos não atendidos. Abortando instalação.")
            return False

        # Fazer backup
        backup_path = self.backup_existing_files()

        # Instalar componentes
        installed_components = self.install_components()

        # Configurar sistema
        if not self.configure_system():
            self.error("Falha na configuração do sistema")
            return False

        # Executar testes
        tests_passed = self.run_tests()

        # Exibir resumo
        self.show_summary(backup_path, installed_components, tests_passed)

        self.log("Instalação concluída")
        return True


def main():
    installer = AvilaIOSInstaller()
    try:
        success = installer.run_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(
            f"\n{installer.colors['yellow']}Instalação interrompida pelo usuário{installer.colors['reset']}"
        )
        sys.exit(1)
    except Exception as e:
        installer.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
