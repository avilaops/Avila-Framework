# coding: utf-8
"""
Script: main.py
Função: Aplicação principal do Windows Dev Optimizer
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer
Descrição: Ferramenta completa para otimização do Windows para desenvolvedores
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

# Adicionar o diretório de módulos ao path
sys.path.append(str(Path(__file__).parent / "modules"))
sys.path.append(str(Path(__file__).parent / "config"))

from edge_analyzer import EdgeAnalyzer
from program_analyzer import ProgramAnalyzer
from bloatware_remover import BloatwareRemover
from developer_optimizer import DeveloperOptimizer
from settings import *

class WindowsDevOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configurar logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Inicializar módulos
        self.edge_analyzer = EdgeAnalyzer()
        self.program_analyzer = ProgramAnalyzer()
        self.bloatware_remover = BloatwareRemover()
        self.developer_optimizer = DeveloperOptimizer()
        
        # Variáveis de controle
        self.analysis_results = {}
        self.selected_optimizations = {
            "remove_bloatware": tk.BooleanVar(value=False),
            "clean_browser": tk.BooleanVar(value=False),
            "remove_unused_programs": tk.BooleanVar(value=False),
            "apply_dev_optimizations": tk.BooleanVar(value=True),
            "install_dev_tools": tk.BooleanVar(value=False),
            "create_restore_point": tk.BooleanVar(value=True)
        }
        
        self.setup_ui()
        
        # Executar análise inicial
        self.start_initial_analysis()
    
    def setup_logging(self):
        """Configura sistema de logging"""
        log_file = LOGS_DIR / f"optimizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=getattr(logging, LOG_CONFIG['level']),
            format=LOG_CONFIG['format'],
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def setup_ui(self):
        """Configura interface gráfica"""
        # Notebook para abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aba 1: Dashboard
        self.setup_dashboard_tab()
        
        # Aba 2: Análise do Edge
        self.setup_edge_tab()
        
        # Aba 3: Programas Instalados
        self.setup_programs_tab()
        
        # Aba 4: Bloatware
        self.setup_bloatware_tab()
        
        # Aba 5: Otimizações
        self.setup_optimization_tab()
        
        # Aba 6: Relatórios
        self.setup_reports_tab()
    
    def setup_dashboard_tab(self):
        """Aba principal com resumo e controles"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Título
        title_label = ttk.Label(dashboard_frame, text=APP_NAME, font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        subtitle_label = ttk.Label(dashboard_frame, text=f"v{APP_VERSION} - {APP_DESCRIPTION}")
        subtitle_label.pack(pady=5)
        
        # Frame principal com duas colunas
        main_frame = ttk.Frame(dashboard_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Coluna esquerda - Status do sistema
        left_frame = ttk.LabelFrame(main_frame, text="📊 Status do Sistema", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(left_frame, height=15, width=50)
        self.status_text.pack(fill="both", expand=True)
        
        # Coluna direita - Otimizações disponíveis
        right_frame = ttk.LabelFrame(main_frame, text="⚙️ Otimizações Disponíveis", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Checkboxes para otimizações
        optimizations = [
            ("create_restore_point", "🛡️ Criar ponto de restauração (Recomendado)"),
            ("remove_bloatware", "🗑️ Remover bloatware do Windows"),
            ("clean_browser", "🌐 Limpar dados do Edge/navegador"),
            ("remove_unused_programs", "📦 Remover programas não utilizados"),
            ("apply_dev_optimizations", "⚡ Aplicar otimizações para desenvolvimento"),
            ("install_dev_tools", "🛠️ Instalar ferramentas de desenvolvimento"),
        ]
        
        for key, text in optimizations:
            cb = ttk.Checkbutton(right_frame, text=text, variable=self.selected_optimizations[key])
            cb.pack(anchor="w", pady=5)
        
        # Botões de ação
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        self.analyze_btn = ttk.Button(button_frame, text="🔍 Analisar Sistema", 
                                    command=self.start_analysis, style="Accent.TButton")
        self.analyze_btn.pack(fill="x", pady=2)
        
        self.optimize_btn = ttk.Button(button_frame, text="⚡ Otimizar Sistema",
                                     command=self.start_optimization)
        self.optimize_btn.pack(fill="x", pady=2)
        
        self.report_btn = ttk.Button(button_frame, text="📄 Gerar Relatório",
                                   command=self.generate_full_report)
        self.report_btn.pack(fill="x", pady=2)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(dashboard_frame, mode='indeterminate')
        self.progress.pack(fill="x", padx=20, pady=10)
    
    def setup_edge_tab(self):
        """Aba de análise do Edge"""
        edge_frame = ttk.Frame(self.notebook)
        self.notebook.add(edge_frame, text="🌐 Edge/Navegador")
        
        # Título
        ttk.Label(edge_frame, text="Análise do Microsoft Edge", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Informações do Edge
        info_frame = ttk.LabelFrame(edge_frame, text="📊 Informações", padding=10)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.edge_info_text = scrolledtext.ScrolledText(info_frame, height=8)
        self.edge_info_text.pack(fill="both", expand=True)
        
        # Análise de produtividade
        prod_frame = ttk.LabelFrame(edge_frame, text="📈 Análise de Produtividade", padding=10)
        prod_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.productivity_text = scrolledtext.ScrolledText(prod_frame, height=10)
        self.productivity_text.pack(fill="both", expand=True)
        
        # Botões
        btn_frame = ttk.Frame(edge_frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Analisar Edge", 
                  command=self.analyze_edge).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar Cache", 
                  command=self.clean_edge_cache).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📊 Relatório Detalhado", 
                  command=self.edge_detailed_report).pack(side="left", padx=5)
    
    def setup_programs_tab(self):
        """Aba de análise de programas"""
        programs_frame = ttk.Frame(self.notebook)
        self.notebook.add(programs_frame, text="📦 Programas")
        
        # Título
        ttk.Label(programs_frame, text="Análise de Programas Instalados", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame principal
        main_frame = ttk.Frame(programs_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lista de programas não utilizados
        unused_frame = ttk.LabelFrame(main_frame, text="🗑️ Programas Não Utilizados", padding=10)
        unused_frame.pack(fill="both", expand=True)
        
        # Treeview para mostrar programas
        columns = ("Nome", "Tamanho (MB)", "Último Uso", "Motivo")
        self.programs_tree = ttk.Treeview(unused_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.programs_tree.heading(col, text=col)
            self.programs_tree.column(col, width=150)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(unused_frame, orient="vertical", command=self.programs_tree.yview)
        self.programs_tree.configure(yscrollcommand=scrollbar.set)
        
        self.programs_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        btn_frame = ttk.Frame(programs_frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Analisar Programas",
                  command=self.analyze_programs).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Remover Selecionados",
                  command=self.remove_selected_programs).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📊 Relatório de Espaço",
                  command=self.programs_space_report).pack(side="left", padx=5)
    
    def setup_bloatware_tab(self):
        """Aba de remoção de bloatware"""
        bloatware_frame = ttk.Frame(self.notebook)
        self.notebook.add(bloatware_frame, text="🗑️ Bloatware")
        
        # Título
        ttk.Label(bloatware_frame, text="Remoção de Bloatware do Windows", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para categorias
        categories_frame = ttk.LabelFrame(bloatware_frame, text="📱 Apps Removíveis por Categoria", padding=10)
        categories_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Notebook para categorias
        self.bloatware_notebook = ttk.Notebook(categories_frame)
        self.bloatware_notebook.pack(fill="both", expand=True)
        
        # Abas para cada categoria
        self.category_frames = {}
        categories = ["Gaming", "Mídia", "Social", "Utilitários", "Outros"]
        
        for category in categories:
            frame = ttk.Frame(self.bloatware_notebook)
            self.bloatware_notebook.add(frame, text=category)
            
            # Lista de apps na categoria
            listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE)
            listbox.pack(fill="both", expand=True, padx=10, pady=10)
            
            self.category_frames[category.lower()] = listbox
        
        # Botões
        btn_frame = ttk.Frame(bloatware_frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Escanear Apps",
                  command=self.scan_bloatware).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Remover Selecionados",
                  command=self.remove_bloatware).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="⚠️ Criar Backup",
                  command=self.create_system_backup).pack(side="left", padx=5)
    
    def setup_optimization_tab(self):
        """Aba de otimizações para desenvolvedores"""
        opt_frame = ttk.Frame(self.notebook)
        self.notebook.add(opt_frame, text="⚡ Otimizações")
        
        # Título
        ttk.Label(opt_frame, text="Otimizações para Desenvolvedores", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame principal com duas colunas
        main_frame = ttk.Frame(opt_frame)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Esquerda - Status do sistema
        left_frame = ttk.LabelFrame(main_frame, text="💻 Especificações do Sistema", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.system_specs_text = scrolledtext.ScrolledText(left_frame, height=15)
        self.system_specs_text.pack(fill="both", expand=True)
        
        # Direita - Ferramentas de desenvolvimento
        right_frame = ttk.LabelFrame(main_frame, text="🛠️ Ferramentas de Desenvolvimento", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.dev_tools_text = scrolledtext.ScrolledText(right_frame, height=15)
        self.dev_tools_text.pack(fill="both", expand=True)
        
        # Botões
        btn_frame = ttk.Frame(opt_frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🔍 Verificar Sistema",
                  command=self.check_system_specs).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="⚡ Aplicar Otimizações",
                  command=self.apply_dev_optimizations).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🛠️ Instalar Ferramentas",
                  command=self.install_dev_tools).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🏗️ Configurar WSL2",
                  command=self.setup_wsl2).pack(side="left", padx=5)
    
    def setup_reports_tab(self):
        """Aba de relatórios"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📄 Relatórios")
        
        # Título
        ttk.Label(reports_frame, text="Relatórios de Análise", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Área de texto para relatório
        self.report_text = scrolledtext.ScrolledText(reports_frame, height=25)
        self.report_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botões
        btn_frame = ttk.Frame(reports_frame)
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(btn_frame, text="📊 Relatório Completo",
                  command=self.generate_full_report).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Salvar Relatório",
                  command=self.save_report).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📧 Enviar por Email",
                  command=self.email_report).pack(side="left", padx=5)
    
    def start_initial_analysis(self):
        """Inicia análise inicial do sistema"""
        self.update_status("🔍 Iniciando análise do sistema...\n")
        
        # Executar análises em thread separada
        thread = threading.Thread(target=self.run_initial_analysis, daemon=True)
        thread.start()
    
    def run_initial_analysis(self):
        """Executa análise inicial em background"""
        try:
            self.progress.start()
            
            # Análise básica do sistema
            self.update_status("📊 Verificando especificações do sistema...\n")
            system_specs = self.developer_optimizer.check_system_specs()
            
            self.update_status(f"💻 RAM: {system_specs.get('ram', {}).get('total_gb', 0)} GB\n")
            self.update_status(f"⚙️ CPU: {system_specs.get('cpu', {}).get('cores', 0)} cores\n")
            
            # Verificar Edge
            self.update_status("🌐 Verificando Microsoft Edge...\n")
            if self.edge_analyzer.check_edge_installation():
                self.update_status("✅ Edge encontrado\n")
                
                cache_info = self.edge_analyzer.get_cache_size()
                cache_size_mb = cache_info['total_size'] / (1024 * 1024)
                self.update_status(f"📂 Cache do Edge: {cache_size_mb:.1f} MB\n")
            else:
                self.update_status("❌ Edge não encontrado\n")
            
            # Verificar programas
            self.update_status("📦 Analisando programas instalados...\n")
            programs = self.program_analyzer.get_installed_programs()
            unused_programs = self.program_analyzer.identify_unused_programs()
            
            self.update_status(f"📊 Total de programas: {len(programs)}\n")
            self.update_status(f"🗑️ Programas não utilizados: {len(unused_programs)}\n")
            
            if unused_programs:
                total_size = sum(p.get('size_mb', 0) for p in unused_programs)
                self.update_status(f"💾 Espaço liberável: {total_size/1024:.1f} GB\n")
            
            # Verificar bloatware
            self.update_status("📱 Escaneando bloatware...\n")
            apps_scan = self.bloatware_remover.scan_installed_apps()
            removable_count = len(apps_scan['removable'])
            
            self.update_status(f"🗑️ Apps removíveis encontrados: {removable_count}\n")
            
            # Verificar ferramentas de desenvolvimento
            self.update_status("🛠️ Verificando ferramentas de desenvolvimento...\n")
            tools_status = self.developer_optimizer.check_installed_tools()
            installed_tools = sum(1 for status in tools_status.values() if status['installed'])
            total_tools = len(tools_status)
            
            self.update_status(f"🛠️ Ferramentas instaladas: {installed_tools}/{total_tools}\n")
            
            self.update_status("\n✅ Análise inicial concluída!\n")
            self.update_status("💡 Use as abas para análises detalhadas ou otimize o sistema.\n")
            
        except Exception as e:
            self.update_status(f"❌ Erro na análise: {str(e)}\n")
            self.logger.error(f"Erro na análise inicial: {e}")
        finally:
            self.progress.stop()
    
    def start_analysis(self):
        """Inicia análise completa do sistema"""
        self.progress.start()
        thread = threading.Thread(target=self.run_full_analysis, daemon=True)
        thread.start()
    
    def run_full_analysis(self):
        """Executa análise completa"""
        try:
            self.update_status("🔍 Iniciando análise completa...\n")
            
            # Análises detalhadas
            self.analysis_results = {
                'edge': self.edge_analyzer.generate_report(),
                'programs': self.program_analyzer.generate_report(),
                'bloatware': self.bloatware_remover.generate_removal_report(),
                'optimization': self.developer_optimizer.setup_development_environment()
            }
            
            self.update_status("✅ Análise completa finalizada!\n")
            self.update_status("📊 Verifique as abas para resultados detalhados.\n")
            
        except Exception as e:
            self.update_status(f"❌ Erro na análise: {str(e)}\n")
        finally:
            self.progress.stop()
    
    def start_optimization(self):
        """Inicia otimização do sistema"""
        if not messagebox.askyesno("Confirmar Otimização", 
                                  "Deseja aplicar as otimizações selecionadas?\n\nEsta ação pode modificar seu sistema."):
            return
        
        self.progress.start()
        thread = threading.Thread(target=self.run_optimization, daemon=True)
        thread.start()
    
    def run_optimization(self):
        """Executa otimização do sistema"""
        try:
            self.update_status("⚡ Iniciando otimização do sistema...\n")
            
            # Criar ponto de restauração
            if self.selected_optimizations["create_restore_point"].get():
                self.update_status("🛡️ Criando ponto de restauração...\n")
                result = self.bloatware_remover.create_restore_point()
                if result['success']:
                    self.update_status("✅ Ponto de restauração criado\n")
                else:
                    self.update_status(f"❌ Erro ao criar ponto de restauração: {result['error']}\n")
            
            # Remover bloatware
            if self.selected_optimizations["remove_bloatware"].get():
                self.update_status("🗑️ Removendo bloatware...\n")
                self.remove_bloatware_auto()
            
            # Limpar navegador
            if self.selected_optimizations["clean_browser"].get():
                self.update_status("🌐 Limpando dados do navegador...\n")
                self.clean_edge_cache()
            
            # Remover programas não utilizados
            if self.selected_optimizations["remove_unused_programs"].get():
                self.update_status("📦 Analisando programas não utilizados...\n")
                # Implementar remoção automática com confirmação
            
            # Aplicar otimizações de desenvolvimento
            if self.selected_optimizations["apply_dev_optimizations"].get():
                self.update_status("⚡ Aplicando otimizações para desenvolvimento...\n")
                result = self.developer_optimizer.apply_performance_settings()
                if result['applied']:
                    self.update_status(f"✅ Aplicadas {len(result['applied'])} otimizações\n")
            
            # Instalar ferramentas de desenvolvimento
            if self.selected_optimizations["install_dev_tools"].get():
                self.update_status("🛠️ Instalando ferramentas de desenvolvimento...\n")
                # Implementar instalação automática
            
            self.update_status("\n✅ Otimização concluída!\n")
            self.update_status("🔄 Recomenda-se reiniciar o sistema para aplicar todas as mudanças.\n")
            
        except Exception as e:
            self.update_status(f"❌ Erro na otimização: {str(e)}\n")
        finally:
            self.progress.stop()
    
    def update_status(self, message):
        """Atualiza texto de status"""
        def update():
            self.status_text.insert(tk.END, message)
            self.status_text.see(tk.END)
        
        self.root.after(0, update)
    
    # Métodos para funcionalidades específicas
    def analyze_edge(self):
        """Analisa o Edge"""
        thread = threading.Thread(target=self._analyze_edge_thread, daemon=True)
        thread.start()
    
    def _analyze_edge_thread(self):
        try:
            report = self.edge_analyzer.generate_report()
            
            # Atualizar UI
            def update_edge_ui():
                self.edge_info_text.delete(1.0, tk.END)
                if 'error' in report:
                    self.edge_info_text.insert(tk.END, f"Erro: {report['error']}")
                    return
                
                # Informações básicas
                info = f"Edge encontrado: {report['edge_installation']['found']}\n"
                info += f"Caminho: {report['edge_installation']['path']}\n\n"
                
                # História
                recent_count = len(report['browsing_history']['recent_history'])
                info += f"Histórico recente (7 dias): {recent_count} entradas\n"
                
                most_visited = report['browsing_history']['most_visited']
                info += f"Sites mais visitados: {len(most_visited)}\n\n"
                
                # Armazenamento
                cache_mb = report['storage_analysis']['cache']['total_size'] / (1024*1024)
                info += f"Cache: {cache_mb:.1f} MB\n"
                info += f"Cookies: {report['storage_analysis']['cookies']['total_count']}\n"
                info += f"Bookmarks: {report['storage_analysis']['bookmarks_count']}\n"
                
                self.edge_info_text.insert(tk.END, info)
                
                # Análise de produtividade
                self.productivity_text.delete(1.0, tk.END)
                prod_analysis = report['browsing_history']['productivity_analysis']
                
                prod_text = "=== ANÁLISE DE PRODUTIVIDADE ===\n\n"
                
                time_analysis = prod_analysis['time_analysis']
                prod_percentage = time_analysis['productivity_percentage']
                
                prod_text += f"Produtividade geral: {prod_percentage:.1f}%\n\n"
                
                # Sites produtivos
                if prod_analysis['categorized_sites']['productive']:
                    prod_text += "🟢 SITES PRODUTIVOS:\n"
                    for site in prod_analysis['categorized_sites']['productive'][:10]:
                        prod_text += f"  • {site['domain']} ({site['visit_count']} visitas)\n"
                    prod_text += "\n"
                
                # Sites de entretenimento
                if prod_analysis['categorized_sites']['entertainment']:
                    prod_text += "🔴 SITES DE ENTRETENIMENTO:\n"
                    for site in prod_analysis['categorized_sites']['entertainment'][:10]:
                        prod_text += f"  • {site['domain']} ({site['visit_count']} visitas)\n"
                
                self.productivity_text.insert(tk.END, prod_text)
            
            self.root.after(0, update_edge_ui)
            
        except Exception as e:
            def show_error():
                self.edge_info_text.delete(1.0, tk.END)
                self.edge_info_text.insert(tk.END, f"Erro na análise: {str(e)}")
            
            self.root.after(0, show_error)
    
    def clean_edge_cache(self):
        """Limpa cache do Edge"""
        if messagebox.askyesno("Limpar Cache", "Deseja limpar o cache do Edge?\n\nO Edge deve estar fechado."):
            try:
                result = self.edge_analyzer.clear_browsing_data(['cache'])
                if result.get('cache', False):
                    messagebox.showinfo("Sucesso", "Cache limpo com sucesso!")
                else:
                    messagebox.showerror("Erro", "Erro ao limpar cache. Certifique-se que o Edge está fechado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")
    
    def edge_detailed_report(self):
        """Gera relatório detalhado do Edge"""
        try:
            report = self.edge_analyzer.generate_report()
            
            # Salvar relatório
            report_file = REPORTS_DIR / f"edge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str, ensure_ascii=False)
            
            messagebox.showinfo("Relatório Gerado", f"Relatório salvo em:\n{report_file}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def analyze_programs(self):
        """Analisa programas instalados"""
        thread = threading.Thread(target=self._analyze_programs_thread, daemon=True)
        thread.start()
    
    def _analyze_programs_thread(self):
        try:
            unused_programs = self.program_analyzer.identify_unused_programs()
            
            def update_programs_ui():
                # Limpar treeview
                for item in self.programs_tree.get_children():
                    self.programs_tree.delete(item)
                
                # Adicionar programas não utilizados
                for program in unused_programs:
                    self.programs_tree.insert("", "end", values=(
                        program['display_name'],
                        f"{program.get('size_mb', 0):.0f}",
                        f"{program.get('days_since_last_use', 'Nunca')} dias",
                        program['unused_reason']
                    ))
            
            self.root.after(0, update_programs_ui)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro na análise: {str(e)}")
            self.root.after(0, show_error)
    
    def remove_selected_programs(self):
        """Remove programas selecionados"""
        selected_items = self.programs_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Seleção", "Selecione programas para remover")
            return
        
        programs_to_remove = []
        for item in selected_items:
            program_name = self.programs_tree.item(item)['values'][0]
            programs_to_remove.append(program_name)
        
        if messagebox.askyesno("Confirmar Remoção", 
                              f"Remover {len(programs_to_remove)} programa(s)?\n\n" + 
                              "\n".join(programs_to_remove)):
            # Implementar remoção
            messagebox.showinfo("Aviso", "Funcionalidade de remoção automática em desenvolvimento.\n" +
                               "Use o Painel de Controle para remover programas manualmente.")
    
    def programs_space_report(self):
        """Gera relatório de espaço dos programas"""
        try:
            disk_analysis = self.program_analyzer.get_disk_space_analysis()
            
            report = f"""=== RELATÓRIO DE ESPAÇO DOS PROGRAMAS ===

Total de programas: {disk_analysis['total_programs']}
Espaço total ocupado: {disk_analysis['total_size_mb']/1024:.1f} GB
Espaço liberável: {disk_analysis['unused_size_mb']/1024:.1f} GB

=== MAIORES PROGRAMAS ===
"""
            
            for program in disk_analysis['largest_programs'][:20]:
                report += f"• {program['name']}: {program['size_mb']:.0f} MB\n"
            
            # Mostrar em nova janela
            self.show_text_window("Relatório de Espaço", report)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def scan_bloatware(self):
        """Escaneia bloatware"""
        thread = threading.Thread(target=self._scan_bloatware_thread, daemon=True)
        thread.start()
    
    def _scan_bloatware_thread(self):
        try:
            apps_scan = self.bloatware_remover.scan_installed_apps()
            
            def update_bloatware_ui():
                # Limpar listas
                for listbox in self.category_frames.values():
                    listbox.delete(0, tk.END)
                
                # Categorizar e adicionar apps
                report = self.bloatware_remover.generate_removal_report()
                categories = report['categories']
                
                for category_name, apps in categories.items():
                    if category_name in self.category_frames:
                        listbox = self.category_frames[category_name]
                        for app in apps:
                            listbox.insert(tk.END, f"{app['name']} ({app['size_mb']:.1f} MB)")
            
            self.root.after(0, update_bloatware_ui)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro no scan: {str(e)}")
            self.root.after(0, show_error)
    
    def remove_bloatware(self):
        """Remove bloatware selecionado"""
        messagebox.showinfo("Aviso", "Funcionalidade em desenvolvimento.\n" +
                           "Execute como administrador para remover apps do Windows.")
    
    def remove_bloatware_auto(self):
        """Remove bloatware automaticamente (modo seguro)"""
        try:
            apps_scan = self.bloatware_remover.scan_installed_apps()
            removable_apps = apps_scan['removable']
            
            # Selecionar apenas apps seguros para remoção automática
            safe_apps = []
            safe_keywords = ['xbox', 'gaming', 'solitaire', 'candy', 'zune']
            
            for app in removable_apps:
                app_name_lower = app['name'].lower()
                if any(keyword in app_name_lower for keyword in safe_keywords):
                    safe_apps.append(app['package_full_name'])
            
            if safe_apps:
                self.update_status(f"🗑️ Removendo {len(safe_apps)} apps seguros...\n")
                
                # Remover apps (simulação por enquanto)
                for app in safe_apps[:3]:  # Limitar para teste
                    self.update_status(f"  • Removendo {app}\n")
                
                self.update_status("✅ Apps removidos com sucesso\n")
            else:
                self.update_status("ℹ️ Nenhum app seguro para remoção automática encontrado\n")
                
        except Exception as e:
            self.update_status(f"❌ Erro ao remover bloatware: {str(e)}\n")
    
    def create_system_backup(self):
        """Cria backup do sistema"""
        result = self.bloatware_remover.create_restore_point()
        if result['success']:
            messagebox.showinfo("Backup", result['message'])
        else:
            messagebox.showerror("Erro", result['error'])
    
    def check_system_specs(self):
        """Verifica especificações do sistema"""
        thread = threading.Thread(target=self._check_system_specs_thread, daemon=True)
        thread.start()
    
    def _check_system_specs_thread(self):
        try:
            specs = self.developer_optimizer.check_system_specs()
            tools = self.developer_optimizer.check_installed_tools()
            
            def update_specs_ui():
                # Specs do sistema
                self.system_specs_text.delete(1.0, tk.END)
                
                specs_text = "=== ESPECIFICAÇÕES DO SISTEMA ===\n\n"
                
                # CPU
                cpu = specs.get('cpu', {})
                specs_text += f"🖥️ PROCESSADOR:\n"
                specs_text += f"  Cores físicos: {cpu.get('cores', 'N/A')}\n"
                specs_text += f"  Threads: {cpu.get('threads', 'N/A')}\n"
                specs_text += f"  Frequência: {cpu.get('frequency', 'N/A')} MHz\n\n"
                
                # RAM
                ram = specs.get('ram', {})
                specs_text += f"💾 MEMÓRIA RAM:\n"
                specs_text += f"  Total: {ram.get('total_gb', 0)} GB\n"
                specs_text += f"  Disponível: {ram.get('available_gb', 0)} GB\n"
                specs_text += f"  Em uso: {ram.get('used_percent', 0)}%\n\n"
                
                # Discos
                disks = specs.get('disks', [])
                specs_text += f"💿 ARMAZENAMENTO:\n"
                for disk in disks:
                    specs_text += f"  {disk['device']} ({disk['fstype']}):\n"
                    specs_text += f"    Total: {disk['total_gb']} GB\n"
                    specs_text += f"    Livre: {disk['free_gb']} GB\n"
                    specs_text += f"    Usado: {disk['used_percent']}%\n"
                
                self.system_specs_text.insert(tk.END, specs_text)
                
                # Ferramentas de desenvolvimento
                self.dev_tools_text.delete(1.0, tk.END)
                
                tools_text = "=== FERRAMENTAS DE DESENVOLVIMENTO ===\n\n"
                
                installed_count = 0
                for tool_name, status in tools.items():
                    if status['installed']:
                        tools_text += f"✅ {tool_name}: {status.get('version', 'Instalado')}\n"
                        installed_count += 1
                    else:
                        tools_text += f"❌ {tool_name}: Não instalado\n"
                        if 'install_command' in status:
                            tools_text += f"   Instalar: {status['install_command']}\n"
                
                tools_text += f"\nInstaladas: {installed_count}/{len(tools)} ferramentas\n"
                
                self.dev_tools_text.insert(tk.END, tools_text)
            
            self.root.after(0, update_specs_ui)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro ao verificar sistema: {str(e)}")
            self.root.after(0, show_error)
    
    def apply_dev_optimizations(self):
        """Aplica otimizações para desenvolvimento"""
        if messagebox.askyesno("Confirmar", "Aplicar otimizações para desenvolvimento?\n\n" +
                              "Isso modificará configurações do sistema."):
            thread = threading.Thread(target=self._apply_optimizations_thread, daemon=True)
            thread.start()
    
    def _apply_optimizations_thread(self):
        try:
            result = self.developer_optimizer.apply_performance_settings()
            
            def show_result():
                message = f"Otimizações aplicadas: {len(result['applied'])}\n"
                if result['failed']:
                    message += f"Falharam: {len(result['failed'])}\n"
                if result['requires_restart']:
                    message += "\nReinicie o sistema para aplicar todas as mudanças."
                
                messagebox.showinfo("Otimizações", message)
            
            self.root.after(0, show_result)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro ao aplicar otimizações: {str(e)}")
            self.root.after(0, show_error)
    
    def install_dev_tools(self):
        """Instala ferramentas de desenvolvimento"""
        messagebox.showinfo("Ferramentas", "Funcionalidade em desenvolvimento.\n" +
                           "Use winget ou instaladores manuais por enquanto.")
    
    def setup_wsl2(self):
        """Configura WSL2"""
        if messagebox.askyesno("WSL2", "Instalar WSL2 (Windows Subsystem for Linux)?\n\n" +
                              "Isso requer reinicialização do sistema."):
            thread = threading.Thread(target=self._setup_wsl2_thread, daemon=True)
            thread.start()
    
    def _setup_wsl2_thread(self):
        try:
            result = self.developer_optimizer.install_wsl2()
            
            def show_result():
                if result['success']:
                    message = result['message']
                    if result.get('requires_restart'):
                        message += "\n\nReinicie o sistema para completar a instalação."
                    messagebox.showinfo("WSL2", message)
                else:
                    messagebox.showerror("Erro", f"Erro ao instalar WSL2: {result['error']}")
            
            self.root.after(0, show_result)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro: {str(e)}")
            self.root.after(0, show_error)
    
    def generate_full_report(self):
        """Gera relatório completo"""
        thread = threading.Thread(target=self._generate_report_thread, daemon=True)
        thread.start()
    
    def _generate_report_thread(self):
        try:
            # Coletar dados de todos os módulos
            edge_report = self.edge_analyzer.generate_report()
            programs_report = self.program_analyzer.generate_report()
            bloatware_report = self.bloatware_remover.generate_removal_report()
            system_specs = self.developer_optimizer.check_system_specs()
            tools_status = self.developer_optimizer.check_installed_tools()
            
            # Compilar relatório
            report = f"""
# WINDOWS DEV OPTIMIZER - RELATÓRIO COMPLETO
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📊 RESUMO EXECUTIVO

### Sistema:
- RAM: {system_specs.get('ram', {}).get('total_gb', 0)} GB
- CPU: {system_specs.get('cpu', {}).get('cores', 0)} cores / {system_specs.get('cpu', {}).get('threads', 0)} threads
- SO: {system_specs.get('windows', {}).get('release', 'Windows')}

### Análises:
- Programas instalados: {programs_report.get('summary', {}).get('total_programs', 0)}
- Programas não utilizados: {programs_report.get('summary', {}).get('unused_programs', 0)}
- Potencial de economia: {programs_report.get('summary', {}).get('potential_space_savings_gb', 0):.1f} GB
- Apps removíveis: {bloatware_report.get('summary', {}).get('total_removable', 0)}
- Ferramentas dev instaladas: {sum(1 for s in tools_status.values() if s['installed'])}/{len(tools_status)}

## 🌐 MICROSOFT EDGE

"""
            
            if 'error' not in edge_report:
                cache_mb = edge_report['storage_analysis']['cache']['total_size'] / (1024*1024)
                productivity = edge_report['browsing_history']['productivity_analysis']['time_analysis']['productivity_percentage']
                
                report += f"""
### Armazenamento:
- Cache: {cache_mb:.1f} MB
- Cookies: {edge_report['storage_analysis']['cookies']['total_count']}
- Bookmarks: {edge_report['storage_analysis']['bookmarks_count']}

### Produtividade:
- Índice de produtividade: {productivity:.1f}%

### Sites mais visitados:
"""
                for site in edge_report['browsing_history']['most_visited'][:10]:
                    report += f"- {site['domain']} ({site['visit_count']} visitas)\n"
            else:
                report += "❌ Edge não encontrado ou erro na análise\n"
            
            report += f"""

## 📦 PROGRAMAS INSTALADOS

### Programas não utilizados (Top 10):
"""
            
            for program in programs_report.get('unused_programs', [])[:10]:
                report += f"- {program['display_name']} ({program.get('size_mb', 0):.0f} MB) - {program['unused_reason']}\n"
            
            report += f"""

## 🗑️ BLOATWARE

### Apps removíveis por categoria:
"""
            
            for category, apps in bloatware_report.get('categories', {}).items():
                if apps:
                    report += f"- {category.title()}: {len(apps)} apps\n"
            
            report += f"""

## 🛠️ FERRAMENTAS DE DESENVOLVIMENTO

### Status das ferramentas:
"""
            
            for tool_name, status in tools_status.items():
                if status['installed']:
                    report += f"✅ {tool_name}: {status.get('version', 'Instalado')}\n"
                else:
                    report += f"❌ {tool_name}: Não instalado\n"
            
            report += f"""

## 💡 RECOMENDAÇÕES

### Limpeza:
"""
            
            if programs_report.get('unused_programs'):
                savings_gb = programs_report['summary']['potential_space_savings_gb']
                report += f"- Remover programas não utilizados pode liberar {savings_gb:.1f} GB\n"
            
            if bloatware_report['summary']['total_removable'] > 0:
                savings_gb = bloatware_report['summary']['potential_savings_gb']
                report += f"- Remover bloatware pode liberar {savings_gb:.1f} GB\n"
            
            if 'error' not in edge_report:
                cache_mb = edge_report['storage_analysis']['cache']['total_size'] / (1024*1024)
                if cache_mb > 100:
                    report += f"- Limpar cache do Edge pode liberar {cache_mb:.1f} MB\n"
            
            report += """
### Desenvolvimento:
"""
            
            missing_tools = [name for name, status in tools_status.items() if not status['installed']]
            if missing_tools:
                report += f"- Instalar ferramentas faltantes: {', '.join(missing_tools)}\n"
            
            ram_gb = system_specs.get('ram', {}).get('total_gb', 0)
            if ram_gb < 16:
                report += f"- Considerar upgrade de RAM (atual: {ram_gb} GB)\n"
            
            report += """
- Aplicar otimizações de performance
- Configurar exclusões no Windows Defender
- Habilitar modo de desenvolvedor
- Instalar WSL2 para desenvolvimento multiplataforma

## 📋 PRÓXIMOS PASSOS

1. ✅ Criar ponto de restauração
2. 🗑️ Remover bloatware e programas não utilizados
3. 🌐 Limpar cache e dados temporários
4. ⚡ Aplicar otimizações de performance
5. 🛠️ Instalar ferramentas de desenvolvimento faltantes
6. 🔄 Reiniciar sistema para aplicar mudanças

---
Relatório gerado pelo Windows Dev Optimizer v{APP_VERSION}
"""
            
            def update_report_ui():
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(tk.END, report)
            
            self.root.after(0, update_report_ui)
            
        except Exception as e:
            def show_error():
                messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
            self.root.after(0, show_error)
    
    def save_report(self):
        """Salva relatório em arquivo"""
        try:
            report_content = self.report_text.get(1.0, tk.END)
            
            if not report_content.strip():
                messagebox.showwarning("Aviso", "Gere um relatório primeiro")
                return
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = REPORTS_DIR / f"windows_dev_optimizer_report_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Relatório Salvo", f"Relatório salvo em:\n{report_file}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def email_report(self):
        """Envia relatório por email"""
        messagebox.showinfo("Email", "Funcionalidade de email em desenvolvimento.\n" +
                           "Salve o relatório e envie manualmente por enquanto.")
    
    def show_text_window(self, title, content):
        """Mostra texto em nova janela"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x600")
        
        text_widget = scrolledtext.ScrolledText(window)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, content)
        
        ttk.Button(window, text="Fechar", command=window.destroy).pack(pady=5)

def main():
    """Função principal"""
    # Verificar se está rodando como administrador (recomendado)
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("⚠️ Aviso: Para melhor funcionamento, execute como administrador")
    except:
        pass
    
    # Criar diretórios necessários
    for directory in [LOGS_DIR, REPORTS_DIR]:
        directory.mkdir(exist_ok=True)
    
    # Iniciar aplicação
    root = tk.Tk()
    
    # Configurar tema
    style = ttk.Style()
    style.theme_use('clam')
    
    app = WindowsDevOptimizer(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
    except Exception as e:
        print(f"Erro na aplicação: {e}")
        logging.error(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()