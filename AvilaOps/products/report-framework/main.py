"""
ÁVILA REPORT FRAMEWORK - INTERFACE PRINCIPAL
============================================
Interface gráfica principal para geração de relatórios
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
from datetime import datetime
import os

# Importar módulos do framework
from config import *
from logger import logger
from exporters.markdown_exporter import MarkdownExporter
from exporters.excel_exporter import ExcelExporter
from exporters.whatsapp_exporter import WhatsAppExporter
from exporters.email_exporter import EmailExporter

class AvilaReportFramework:
    """Interface principal do Ávila Report Framework"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_style()
        self.create_widgets()
        self.current_data = {}

        logger.info("🚀 Ávila Report Framework iniciado")

    def setup_window(self):
        """Configurar janela principal"""
        self.root.title(GUI_CONFIG["title"])
        self.root.geometry(GUI_CONFIG["geometry"])
        self.root.minsize(*GUI_CONFIG["min_size"])

        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")

        # Ícone (se existir)
        icon_path = GUI_CONFIG.get("icon_path")
        if icon_path and os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def setup_style(self):
        """Configurar estilo visual"""
        style = ttk.Style()
        style.theme_use('clam')

        # Cores do tema
        theme = GUI_CONFIG["theme"]

        # Configurar estilos personalizados
        style.configure('Header.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=theme["accent"])

        style.configure('Subheader.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=theme["fg_primary"])

        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'))

        style.configure('Warning.TButton',
                       font=('Segoe UI', 10, 'bold'))

        style.configure('Error.TButton',
                       font=('Segoe UI', 10, 'bold'))

    def create_widgets(self):
        """Criar interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Cabeçalho
        self.create_header(main_frame)

        # Área principal (dividida)
        self.create_main_area(main_frame)

        # Barra de status
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Criar cabeçalho"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(header_frame, text="🏛️ Ávila Report Framework",
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)

        # Info
        info_text = f"v{APP_VERSION} | {get_timestamp('date')}"
        info_label = ttk.Label(header_frame, text=info_text)
        info_label.grid(row=0, column=1, sticky=tk.E)

        # Botões rápidos
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Button(buttons_frame, text="🔄 Atualizar",
                  command=self.refresh_data).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(buttons_frame, text="📊 Logs",
                  command=self.show_logs_window).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="⚙️ Configurações",
                  command=self.show_config_window).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="ℹ️ Ajuda",
                  command=self.show_help_window).pack(side=tk.RIGHT)

    def create_main_area(self, parent):
        """Criar área principal"""
        # Painel esquerdo - Controles
        left_frame = ttk.LabelFrame(parent, text="📋 Geração de Relatórios", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)

        self.create_report_controls(left_frame)

        # Painel direito - Visualização
        right_frame = ttk.LabelFrame(parent, text="👁️ Visualização e Logs", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        self.create_preview_area(right_frame)

    def create_report_controls(self, parent):
        """Criar controles de relatório"""
        # Seleção de tipo de relatório
        type_frame = ttk.LabelFrame(parent, text="📊 Tipo de Relatório", padding="10")
        type_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        type_frame.columnconfigure(1, weight=1)

        # Dropdown de tipos
        ttk.Label(type_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W)

        self.report_type_var = tk.StringVar(value="daily")
        type_combo = ttk.Combobox(type_frame, textvariable=self.report_type_var,
                                 state="readonly", width=30)

        # Preencher opções
        type_options = []
        for key, info in REPORT_TYPES.items():
            type_options.append(f"{info['icon']} {info['name']}")

        type_combo['values'] = type_options
        type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        type_combo.bind('<<ComboboxSelected>>', self.on_report_type_changed)

        # Descrição do relatório selecionado
        self.description_label = ttk.Label(type_frame, text="", wraplength=300)
        self.description_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        # Parâmetros do relatório
        params_frame = ttk.LabelFrame(parent, text="⚙️ Parâmetros", padding="10")
        params_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)

        # Data de início
        ttk.Label(params_frame, text="Data Início:").grid(row=0, column=0, sticky=tk.W)
        self.start_date_var = tk.StringVar(value=get_timestamp("date"))
        ttk.Entry(params_frame, textvariable=self.start_date_var).grid(row=0, column=1,
                                                                       sticky=(tk.W, tk.E), padx=(10, 0))

        # Data de fim
        ttk.Label(params_frame, text="Data Fim:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.end_date_var = tk.StringVar(value=get_timestamp("date"))
        ttk.Entry(params_frame, textvariable=self.end_date_var).grid(row=1, column=1,
                                                                     sticky=(tk.W, tk.E), padx=(10, 0), pady=(5, 0))

        # Botões de geração
        generate_frame = ttk.LabelFrame(parent, text="🚀 Gerar Relatório", padding="10")
        generate_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        generate_frame.columnconfigure(0, weight=1)
        generate_frame.columnconfigure(1, weight=1)

        # Botões por formato
        ttk.Button(generate_frame, text="📝 Markdown",
                  command=lambda: self.generate_report("markdown")).grid(row=0, column=0,
                                                                         sticky=(tk.W, tk.E), padx=(0, 5))

        ttk.Button(generate_frame, text="📊 Excel",
                  command=lambda: self.generate_report("excel")).grid(row=0, column=1,
                                                                     sticky=(tk.W, tk.E), padx=(5, 0))

        ttk.Button(generate_frame, text="📱 WhatsApp",
                  command=lambda: self.send_whatsapp()).grid(row=1, column=0,
                                                            sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))

        ttk.Button(generate_frame, text="📧 Email",
                  command=lambda: self.send_email()).grid(row=1, column=1,
                                                         sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))

        # Botões de ação
        action_frame = ttk.LabelFrame(parent, text="⚡ Ações Rápidas", padding="10")
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        action_frame.columnconfigure(0, weight=1)

        ttk.Button(action_frame, text="🎯 Gerar Dados de Exemplo",
                  command=self.generate_sample_data,
                  style='Success.TButton').grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        ttk.Button(action_frame, text="📋 Testar WhatsApp",
                  command=self.test_whatsapp).grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        ttk.Button(action_frame, text="✉️ Testar Email",
                  command=self.test_email).grid(row=2, column=0, sticky=(tk.W, tk.E))

    def create_preview_area(self, parent):
        """Criar área de visualização"""
        # Notebook para abas
        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Aba de Preview
        preview_frame = ttk.Frame(notebook)
        notebook.add(preview_frame, text="👁️ Visualização")

        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD,
                                                     height=15, width=60)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Aba de Logs
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="📊 Logs")

        self.logs_text = scrolledtext.ScrolledText(logs_frame, wrap=tk.WORD,
                                                  height=15, width=60)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Atualizar logs inicialmente
        self.update_logs()

    def create_status_bar(self, parent):
        """Criar barra de status"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)

        # Status
        self.status_var = tk.StringVar(value="✅ Sistema pronto")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)

        # Info adicional
        self.info_var = tk.StringVar(value=f"📁 Logs: {LOG_CONFIG['file']}")
        info_label = ttk.Label(status_frame, textvariable=self.info_var)
        info_label.grid(row=0, column=1, sticky=tk.E)

        # Inicializar
        self.on_report_type_changed()

    def on_report_type_changed(self, event=None):
        """Callback para mudança de tipo de relatório"""
        selected = self.report_type_var.get()

        # Encontrar tipo selecionado
        for key, info in REPORT_TYPES.items():
            if selected.startswith(info['icon']):
                self.description_label.config(text=f"📋 {info['description']}")
                self.status_var.set(f"📊 Selecionado: {info['name']}")
                break

    def generate_sample_data(self):
        """Gerar dados de exemplo para teste"""
        self.status_var.set("🎯 Gerando dados de exemplo...")
        self.progress_var.set(0)

        # Simular progresso
        for i in range(101):
            self.progress_var.set(i)
            self.root.update()

        sample_data = {
            'summary': 'Relatório de exemplo gerado pelo Ávila Report Framework. Este é um teste completo do sistema.',
            'details': 'Dados simulados para demonstração das funcionalidades do framework.',
            'metrics': {
                'Total de Usuários': '1,250',
                'Receita Mensal': 'R$ 85.430,00',
                'Taxa de Crescimento': '+15%',
                'Satisfação Cliente': '92%',
                'Projetos Ativos': '8',
                'Taxa de Conclusão': '87%'
            },
            'receitas_total': 'R$ 85.430,00',
            'despesas_total': 'R$ 62.180,00',
            'resultado': 'R$ 23.250,00',
            'margem': '27,3%',
            'projetos_andamento': '5',
            'projetos_concluidos': '12',
            'projetos_atrasados': '1',
            'score_eficiencia': '88%',
            'score_qualidade': '92%',
            'score_produtividade': '85%'
        }

        self.current_data = sample_data
        self.update_preview()
        self.status_var.set("✅ Dados de exemplo gerados")
        logger.success("Dados de exemplo gerados com sucesso")

    def generate_report(self, format_type):
        """Gerar relatório no formato especificado"""
        if not self.current_data:
            messagebox.showwarning("Aviso", "Primeiro gere dados de exemplo ou configure dados reais.")
            return

        def generate():
            try:
                self.status_var.set(f"📊 Gerando relatório {format_type.upper()}...")

                # Obter tipo de relatório
                report_type = self.get_selected_report_type()

                if format_type == "markdown":
                    exporter = MarkdownExporter()
                    filepath = exporter.export(self.current_data, report_type)

                elif format_type == "excel":
                    exporter = ExcelExporter()
                    filepath = exporter.export(self.current_data, report_type)

                self.status_var.set(f"✅ Relatório {format_type} gerado: {filepath}")
                messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso!\n\nArquivo: {filepath}")

                # Perguntar se deseja abrir o arquivo
                if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o arquivo gerado?"):
                    os.startfile(filepath)

            except Exception as e:
                error_msg = f"Erro ao gerar relatório: {str(e)}"
                self.status_var.set(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
                logger.error(error_msg)

        # Executar em thread separada
        threading.Thread(target=generate, daemon=True).start()

    def send_whatsapp(self):
        """Enviar relatório via WhatsApp"""
        if not self.current_data:
            messagebox.showwarning("Aviso", "Primeiro gere dados de exemplo ou configure dados reais.")
            return

        def send():
            try:
                self.status_var.set("📱 Enviando via WhatsApp...")

                report_type = self.get_selected_report_type()
                exporter = WhatsAppExporter()
                result = exporter.export(self.current_data, report_type)

                self.status_var.set(f"✅ {result}")
                messagebox.showinfo("WhatsApp", f"WhatsApp Web aberto!\n\n{result}")

            except Exception as e:
                error_msg = f"Erro ao enviar WhatsApp: {str(e)}"
                self.status_var.set(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
                logger.error(error_msg)

        threading.Thread(target=send, daemon=True).start()

    def send_email(self):
        """Enviar relatório via Email"""
        if not self.current_data:
            messagebox.showwarning("Aviso", "Primeiro gere dados de exemplo ou configure dados reais.")
            return

        def send():
            try:
                self.status_var.set("📧 Enviando via Email...")

                report_type = self.get_selected_report_type()
                exporter = EmailExporter()
                result = exporter.export(self.current_data, report_type)

                self.status_var.set(f"✅ {result}")
                messagebox.showinfo("Email", f"Email enviado com sucesso!\n\n{result}")

            except Exception as e:
                error_msg = f"Erro ao enviar email: {str(e)}"
                self.status_var.set(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)
                logger.error(error_msg)

        threading.Thread(target=send, daemon=True).start()

    def test_whatsapp(self):
        """Testar conectividade WhatsApp"""
        def test():
            try:
                self.status_var.set("🧪 Testando WhatsApp...")
                exporter = WhatsAppExporter()
                result = exporter.send_test_message()
                self.status_var.set("✅ Teste WhatsApp concluído")
                messagebox.showinfo("Teste WhatsApp", "WhatsApp Web aberto com mensagem de teste!")
            except Exception as e:
                error_msg = f"Erro no teste WhatsApp: {str(e)}"
                self.status_var.set(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)

        threading.Thread(target=test, daemon=True).start()

    def test_email(self):
        """Testar conectividade Email"""
        def test():
            try:
                self.status_var.set("🧪 Testando Email...")
                exporter = EmailExporter()
                result = exporter.send_test_email()
                self.status_var.set("✅ Teste Email concluído")
                messagebox.showinfo("Teste Email", "Email de teste enviado com sucesso!")
            except Exception as e:
                error_msg = f"Erro no teste Email: {str(e)}"
                self.status_var.set(f"❌ {error_msg}")
                messagebox.showerror("Erro", error_msg)

        threading.Thread(target=test, daemon=True).start()

    def get_selected_report_type(self):
        """Obter tipo de relatório selecionado"""
        selected = self.report_type_var.get()

        for key, info in REPORT_TYPES.items():
            if selected.startswith(info['icon']):
                return key

        return "custom"

    def update_preview(self):
        """Atualizar visualização"""
        if not self.current_data:
            return

        preview_content = "📊 PREVIEW DO RELATÓRIO\n"
        preview_content += "=" * 50 + "\n\n"

        preview_content += f"📅 Timestamp: {get_timestamp('br')}\n"
        preview_content += f"📊 Tipo: {self.report_type_var.get()}\n\n"

        preview_content += f"📋 RESUMO:\n{self.current_data.get('summary', 'N/A')}\n\n"

        if 'metrics' in self.current_data:
            preview_content += "📈 MÉTRICAS:\n"
            for metric, value in self.current_data['metrics'].items():
                preview_content += f"• {metric}: {value}\n"

        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, preview_content)

    def update_logs(self):
        """Atualizar visualização de logs"""
        try:
            logs = logger.get_recent_logs(50)
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(1.0, logs)
            self.logs_text.see(tk.END)
        except Exception as e:
            self.logs_text.delete(1.0, tk.END)
            self.logs_text.insert(1.0, f"Erro ao carregar logs: {e}")

    def refresh_data(self):
        """Atualizar dados"""
        self.update_logs()
        self.status_var.set("🔄 Dados atualizados")
        logger.info("Interface atualizada")

    def show_logs_window(self):
        """Mostrar janela de logs"""
        logs_window = tk.Toplevel(self.root)
        logs_window.title("📊 Logs do Sistema")
        logs_window.geometry("800x600")

        logs_text = scrolledtext.ScrolledText(logs_window, wrap=tk.WORD)
        logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Carregar logs completos
        full_logs = logger.get_recent_logs(1000)
        logs_text.insert(1.0, full_logs)
        logs_text.see(tk.END)

    def show_config_window(self):
        """Mostrar janela de configurações"""
        config_window = tk.Toplevel(self.root)
        config_window.title("⚙️ Configurações")
        config_window.geometry("600x400")

        # Notebook para diferentes categorias
        notebook = ttk.Notebook(config_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba WhatsApp
        whatsapp_frame = ttk.Frame(notebook)
        notebook.add(whatsapp_frame, text="📱 WhatsApp")

        ttk.Label(whatsapp_frame, text="Número WhatsApp:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(whatsapp_frame, width=50,
                 text=WHATSAPP_CONFIG["phone_number"]).pack(fill=tk.X, pady=(5, 10))

        # Aba Email
        email_frame = ttk.Frame(notebook)
        notebook.add(email_frame, text="📧 Email")

        ttk.Label(email_frame, text="Email Destinatário:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(email_frame, width=50,
                 text=EMAIL_CONFIG["to_email"]).pack(fill=tk.X, pady=(5, 10))

    def show_help_window(self):
        """Mostrar janela de ajuda"""
        help_window = tk.Toplevel(self.root)
        help_window.title("ℹ️ Ajuda")
        help_window.geometry("700x500")

        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        help_content = f"""
🏛️ ÁVILA REPORT FRAMEWORK - AJUDA

VISÃO GERAL
===========
O Ávila Report Framework é um sistema completo para geração e distribuição
de relatórios corporativos.

FUNCIONALIDADES
===============
📊 Geração de relatórios em múltiplos formatos (Markdown, Excel)
📱 Envio via WhatsApp
📧 Envio via Email
📋 Visualização de logs em tempo real
⚙️ Configurações personalizáveis

TIPOS DE RELATÓRIO
==================
• 📅 Diário: Resumo das atividades do dia
• 📊 Semanal: Consolidado da semana
• 📈 Mensal: Análise mensal completa
• 🏗️ Projetos: Status dos projetos ativos
• 💰 Financeiro: Análise financeira
• 🚀 Performance: Métricas de desempenho
• 🏛️ Governança: Compliance e governança
• ⚙️ Personalizado: Relatório customizado

COMO USAR
=========
1. Selecione o tipo de relatório desejado
2. Configure os parâmetros (datas, etc.)
3. Gere dados de exemplo para teste
4. Escolha o formato de saída
5. Clique no botão correspondente

CONFIGURAÇÕES
=============
WhatsApp: {WHATSAPP_CONFIG["phone_number"]}
Email: {EMAIL_CONFIG["to_email"]}
Logs: {LOG_CONFIG["file"]}

SUPORTE
=======
AvilaOps Team
Email: nicolas@avila.inc
GitHub: https://github.com/avilaops/Avila-Framework

Versão: {APP_VERSION}
"""

        help_text.insert(1.0, help_content)
        help_text.config(state=tk.DISABLED)

    def run(self):
        """Executar aplicação"""
        logger.info("🚀 Interface gráfica iniciada")
        self.root.mainloop()
        logger.info("🛑 Interface gráfica encerrada")

if __name__ == "__main__":
    try:
        app = AvilaReportFramework()
        app.run()
    except Exception as e:
        logger.critical(f"Erro crítico na aplicação: {e}")
        messagebox.showerror("Erro Crítico", f"Erro crítico na aplicação:\n\n{e}")
