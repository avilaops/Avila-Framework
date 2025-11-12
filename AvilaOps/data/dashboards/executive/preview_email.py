"""
👀 PREVIEW DO EMAIL - Plano de Ação Global
Gera HTML local para visualização sem enviar email
"""

from pathlib import Path
from datetime import datetime
import webbrowser

# Importar template do script principal
import sys
sys.path.insert(0, str(Path(__file__).parent))
from enviar_plano import get_premium_email_html

def gerar_preview():
    """Gera HTML local e abre no navegador"""
    
    print("=" * 80)
    print("👀 PREVIEW DO EMAIL - PLANO DE AÇÃO GLOBAL")
    print("=" * 80)
    print()
    
    # Gerar HTML
    html_content = get_premium_email_html()
    
    # Salvar arquivo
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"email_plano_global_preview_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Preview gerado: {output_file}")
    print()
    print("🌐 Abrindo no navegador...")
    
    # Abrir no navegador
    webbrowser.open(output_file.as_uri())
    
    print()
    print("=" * 80)
    print("✅ PREVIEW ABERTO NO NAVEGADOR!")
    print("=" * 80)
    print()
    print("💡 Para enviar o email de verdade:")
    print("   python enviar_plano.py")
    print()
    
    return output_file


if __name__ == "__main__":
    gerar_preview()
