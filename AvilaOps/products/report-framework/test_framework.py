"""
ÁVILA REPORT FRAMEWORK - TESTE COMPLETO
=======================================
Script de teste para validar todas as funcionalidades
"""

import sys
import os
import traceback
from datetime import datetime

# Adicionar o diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_imports():
    """Testar importações"""
    print("📦 TESTANDO IMPORTAÇÕES...")

    try:
        import config
        print("  ✅ Config importado")

        import logger
        print("  ✅ Logger importado")

        from exporters import MarkdownExporter, ExcelExporter
        print("  ✅ Exportadores Markdown e Excel importados")

        from exporters import WhatsAppExporter, EmailExporter
        print("  ✅ Exportadores WhatsApp e Email importados")

        return True

    except Exception as e:
        print(f"  ❌ Erro na importação: {e}")
        traceback.print_exc()
        return False

def test_config():
    """Testar configurações"""
    print("\n⚙️ TESTANDO CONFIGURAÇÕES...")

    try:
        from config import REPORT_TYPES, WHATSAPP_CONFIG, EMAIL_CONFIG

        print(f"  ✅ {len(REPORT_TYPES)} tipos de relatório configurados")
        print(f"  ✅ WhatsApp: {WHATSAPP_CONFIG['phone_number']}")
        print(f"  ✅ Email: {EMAIL_CONFIG['to_email']}")

        return True

    except Exception as e:
        print(f"  ❌ Erro na configuração: {e}")
        return False

def test_sample_data():
    """Testar geração de dados de exemplo"""
    print("\n📊 TESTANDO DADOS DE EXEMPLO...")

    sample_data = {
        'summary': 'Teste do sistema Ávila Report Framework',
        'details': 'Sistema funcionando corretamente em modo de teste.',
        'metrics': {
            'Status': '✅ Operacional',
            'Teste': 'Aprovado',
            'Timestamp': datetime.now().strftime('%H:%M:%S')
        }
    }

    print("  ✅ Dados de exemplo criados")
    return sample_data

def test_markdown_export(sample_data):
    """Testar exportação Markdown"""
    print("\n📝 TESTANDO EXPORTAÇÃO MARKDOWN...")

    try:
        from exporters.markdown_exporter import MarkdownExporter

        exporter = MarkdownExporter()
        filepath = exporter.export(sample_data, "custom", "teste_markdown.md")

        if os.path.exists(filepath):
            print(f"  ✅ Arquivo criado: {filepath}")
            return True
        else:
            print(f"  ❌ Arquivo não encontrado: {filepath}")
            return False

    except Exception as e:
        print(f"  ❌ Erro no Markdown: {e}")
        traceback.print_exc()
        return False

def test_excel_export(sample_data):
    """Testar exportação Excel"""
    print("\n📊 TESTANDO EXPORTAÇÃO EXCEL...")

    try:
        from exporters.excel_exporter import ExcelExporter

        exporter = ExcelExporter()
        filepath = exporter.export(sample_data, "custom", "teste_excel.xlsx")

        if os.path.exists(filepath):
            print(f"  ✅ Arquivo criado: {filepath}")
            return True
        else:
            print(f"  ❌ Arquivo não encontrado: {filepath}")
            return False

    except Exception as e:
        print(f"  ❌ Erro no Excel: {e}")
        print(f"  💡 Instale dependências: pip install pandas openpyxl")
        return False

def test_whatsapp_export(sample_data):
    """Testar exportação WhatsApp"""
    print("\n📱 TESTANDO WHATSAPP...")

    try:
        from exporters.whatsapp_exporter import WhatsAppExporter

        exporter = WhatsAppExporter()
        # Não enviar de verdade no teste, só validar geração
        message = exporter._generate_whatsapp_message(sample_data, "custom", "resumo")

        if len(message) > 0:
            print("  ✅ Mensagem WhatsApp gerada com sucesso")
            print(f"  📏 Tamanho da mensagem: {len(message)} caracteres")
            return True
        else:
            print("  ❌ Falha ao gerar mensagem WhatsApp")
            return False

    except Exception as e:
        print(f"  ❌ Erro no WhatsApp: {e}")
        return False

def test_email_export(sample_data):
    """Testar exportação Email"""
    print("\n📧 TESTANDO EMAIL...")

    try:
        from exporters.email_exporter import EmailExporter

        exporter = EmailExporter()
        # Não enviar de verdade no teste, só validar geração
        subject = exporter._generate_subject("custom")
        body = exporter._generate_body(sample_data, "custom", "html")

        if len(subject) > 0 and len(body) > 0:
            print("  ✅ Email HTML gerado com sucesso")
            print(f"  📧 Assunto: {subject}")
            return True
        else:
            print("  ❌ Falha ao gerar email")
            return False

    except Exception as e:
        print(f"  ❌ Erro no Email: {e}")
        return False

def test_logger():
    """Testar sistema de logs"""
    print("\n📊 TESTANDO LOGGER...")

    try:
        from logger import logger

        logger.info("Teste de log INFO")
        logger.success("Teste de log SUCCESS")
        logger.warning("Teste de log WARNING")

        # Verificar se arquivo de log existe
        from config import LOG_CONFIG
        if os.path.exists(LOG_CONFIG["file"]):
            print(f"  ✅ Arquivo de log criado: {LOG_CONFIG['file']}")
            return True
        else:
            print("  ❌ Arquivo de log não encontrado")
            return False

    except Exception as e:
        print(f"  ❌ Erro no Logger: {e}")
        return False

def test_directories():
    """Testar estrutura de diretórios"""
    print("\n📁 TESTANDO DIRETÓRIOS...")

    required_dirs = ['logs', 'exports', 'exporters']
    all_exist = True

    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ Diretório {dir_name} existe")
        else:
            print(f"  ❌ Diretório {dir_name} não encontrado")
            all_exist = False

    return all_exist

def run_all_tests():
    """Executar todos os testes"""
    print("🏛️ ÁVILA REPORT FRAMEWORK - TESTE COMPLETO")
    print("=" * 60)

    tests = [
        ("Importações", test_imports),
        ("Configurações", test_config),
        ("Diretórios", test_directories),
        ("Logger", test_logger)
    ]

    # Testes básicos
    for test_name, test_func in tests:
        if not test_func():
            print(f"\n❌ FALHA NO TESTE: {test_name}")
            return False

    # Dados de exemplo
    sample_data = test_sample_data()
    if not sample_data:
        return False

    # Testes de exportação
    export_tests = [
        ("Markdown", test_markdown_export),
        ("Excel", test_excel_export),
        ("WhatsApp", test_whatsapp_export),
        ("Email", test_email_export)
    ]

    results = {}
    for test_name, test_func in export_tests:
        results[test_name] = test_func(sample_data)

    # Relatório final
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO FINAL")
    print("=" * 60)

    passed = sum(results.values())
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status} - {test_name}")

    print(f"\n📊 RESULTADO: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Framework pronto para uso.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique as dependências.")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()

        if success:
            print("\n✅ Para executar o framework:")
            print("   python main.py")
        else:
            print("\n🔧 Para corrigir problemas:")
            print("   python setup.py")

    except Exception as e:
        print(f"\n💥 ERRO CRÍTICO: {e}")
        traceback.print_exc()

    finally:
        input("\nPressione Enter para sair...")
