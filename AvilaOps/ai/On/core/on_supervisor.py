"""
📊 ON Supervisor - Mini-framework de Supervisão
Painel CLI para análise de logs, tarefas e turnos dos agentes
"""
import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "registry" / "on_core.db"
console = Console()

def show_logs(agent):
    """Exibe os últimos logs de um agente específico"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT timestamp, message FROM logs WHERE agent=? ORDER BY id DESC LIMIT 10", 
        (agent,)
    ).fetchall()
    conn.close()

    table = Table(title=f"Últimos logs de {agent}")
    table.add_column("Horário", style="cyan")
    table.add_column("Mensagem", style="white")
    
    for r in rows:
        timestamp_display = r[0][-8:] if len(r[0]) > 8 else r[0]
        table.add_row(timestamp_display, r[1])
    
    console.print(table)

def show_tasks(agent):
    """Exibe as tarefas de um agente específico"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, task, status FROM tasks WHERE agent=?", 
        (agent,)
    ).fetchall()
    conn.close()

    table = Table(title=f"Tarefas de {agent}")
    table.add_column("ID", style="cyan")
    table.add_column("Tarefa", style="white")
    table.add_column("Status", style="green")
    
    for r in rows:
        table.add_row(str(r[0]), r[1], r[2])
    
    console.print(table)

def show_shifts(agent):
    """Exibe os turnos de um agente específico"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT start_time, end_time, duration_min FROM shifts WHERE agent=?", 
        (agent,)
    ).fetchall()
    conn.close()

    table = Table(title=f"Turnos de {agent}")
    table.add_column("Início", style="cyan")
    table.add_column("Fim", style="white")
    table.add_column("Duração (min)", style="green")
    
    for r in rows:
        start_display = r[0][-8:] if r[0] and len(r[0]) > 8 else r[0]
        end_display = r[1][-8:] if r[1] and len(r[1]) > 8 else r[1]
        table.add_row(start_display, end_display, str(r[2]))
    
    console.print(table)

def list_agents():
    """Lista todos os agentes que têm registros no sistema"""
    conn = sqlite3.connect(DB_PATH)
    agents = conn.execute(
        "SELECT DISTINCT agent FROM logs UNION SELECT DISTINCT agent FROM tasks UNION SELECT DISTINCT agent FROM shifts"
    ).fetchall()
    conn.close()
    
    if agents:
        console.print("\n[bold yellow]Agentes disponíveis:[/bold yellow]")
        for agent in agents:
            console.print(f"• {agent[0]}")
    else:
        console.print("[yellow]Nenhum agente encontrado no sistema[/yellow]")

def supervisor_panel():
    """Painel principal de supervisão"""
    console.rule("[bold blue]Painel do Supervisor - On.Core[/bold blue]")
    
    while True:
        console.print("\n[bold cyan]Comandos disponíveis:[/bold cyan]")
        console.print("• Digite o nome do agente para analisar")
        console.print("• 'lista' para ver agentes disponíveis")
        console.print("• 'sair' para encerrar")
        
        command = console.input("\n[yellow]Digite seu comando:[/yellow] ").strip().lower()
        
        if command == "sair":
            console.print("[green]Encerrando painel de supervisão...[/green]")
            break
        elif command == "lista":
            list_agents()
        elif command:
            show_logs(command)
            show_tasks(command)
            show_shifts(command)
        else:
            console.print("[red]Comando inválido[/red]")

if __name__ == "__main__":
    supervisor_panel()