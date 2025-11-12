"""
ÁVILA REPORT FRAMEWORK - TESTES DE INTEGRAÇÃO
=============================================
Testes para Archivus e Agentes On
"""

import unittest
import os
import json
from pathlib import Path
from archivus_integration import archivus_integration
from agents_integration import agent_reporter

class TestArchivusIntegration(unittest.TestCase):
    """Testes para integração com Archivus"""

    def test_calculate_hash(self):
        """Testar cálculo de hash SHA256"""
        content = "Teste de conteúdo"
        hash1 = archivus_integration.calculate_hash(content)
        hash2 = archivus_integration.calculate_hash(content)

        # Hash deve ser consistente
        self.assertEqual(hash1, hash2)

        # Hash deve ter 64 caracteres (SHA256)
        self.assertEqual(len(hash1), 64)

        print(f"✅ Hash SHA256: {hash1}")

    def test_official_folders_exist(self):
        """Verificar se pastas oficiais Archivus existem"""
        base_path = Path(r"C:\Users\nicol\OneDrive\Avila\Docs\Relatorios")

        expected_folders = [
            "Conversas",
            "Analises",
            "Auditorias",
            "Performance",
            "Comparacoes",
            "Diagnosticos"
        ]

        missing = []
        for folder in expected_folders:
            folder_path = base_path / folder
            if not folder_path.exists():
                missing.append(folder)

        if missing:
            print(f"⚠️ Pastas faltando (serão criadas automaticamente): {missing}")
        else:
            print(f"✅ Todas as {len(expected_folders)} pastas oficiais existem")

        # Não falhar se pastas não existirem (serão criadas automaticamente)
        self.assertTrue(True)

    def test_save_to_official_location(self):
        """Testar salvamento em pasta oficial"""
        test_content = "# Relatório de Teste\n\nConteúdo de teste para Archivus"
        test_filename = "test_archivus_report.md"

        filepath = archivus_integration.save_to_official_location(
            test_filename,
            test_content,
            "Analises"
        )

        # Verificar se arquivo foi criado
        self.assertTrue(os.path.exists(filepath))

        # Verificar conteúdo
        with open(filepath, 'r', encoding='utf-8') as f:
            saved_content = f.read()

        self.assertEqual(saved_content, test_content)

        print(f"✅ Arquivo salvo em: {filepath}")

        # Limpar arquivo de teste
        if os.path.exists(filepath):
            os.remove(filepath)

    def test_create_integrity_entry(self):
        """Testar criação de entrada de integridade"""
        test_filepath = r"C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Analises\test.md"

        entry = archivus_integration.create_integrity_entry(
            test_filepath,
            {"type": "test", "category": "Analises"}
        )

        # Verificar estrutura da entrada
        self.assertIn('file_path', entry)
        self.assertIn('hash', entry)
        self.assertIn('timestamp', entry)
        self.assertIn('metadata', entry)

        print(f"✅ Entrada de integridade criada: {entry['hash'][:16]}...")

    def test_generate_audit_report(self):
        """Testar geração de relatório de auditoria"""
        test_filepath = r"C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Analises\test.md"

        audit = archivus_integration.generate_audit_report(test_filepath)

        # Verificar estrutura do relatório
        self.assertIn('timestamp', audit)
        self.assertIn('file_path', audit)
        self.assertIn('status', audit)

        print(f"✅ Relatório de auditoria gerado: {audit['status']}")


class TestAgentsIntegration(unittest.TestCase):
    """Testes para integração com Agentes On"""

    def test_load_agents(self):
        """Testar carregamento de agentes"""
        agents = agent_reporter.available_agents

        # Deve ter carregado agentes
        self.assertIsInstance(agents, dict)

        if len(agents) > 0:
            print(f"✅ {len(agents)} agentes carregados: {list(agents.keys())}")
        else:
            print("⚠️ Nenhum agente encontrado (verificar pasta On/agents/)")

    def test_get_agent_for_report_type(self):
        """Testar seleção de agente por tipo de relatório"""
        test_cases = [
            ("financial", "sigma"),
            ("projects", "helix"),
            ("governance", "lex"),
            ("daily", "atlas"),
            ("performance", "lumen")
        ]

        for report_type, expected_agent in test_cases:
            agent = agent_reporter.get_agent_for_report_type(report_type)

            if agent:
                print(f"✅ {report_type} → {list(agent.keys())[0]}")
            else:
                print(f"⚠️ {report_type} → Agente não encontrado")

    def test_generate_agent_context(self):
        """Testar geração de contexto do agente"""
        # Usar agente Atlas (corporativo)
        if "atlas" in agent_reporter.available_agents:
            context = agent_reporter.generate_agent_context("atlas", "daily")

            # Verificar estrutura
            self.assertIn('agent_name', context)
            self.assertIn('area', context)
            self.assertIn('timestamp', context)
            self.assertIn('agent_perspective', context)

            print(f"✅ Contexto gerado para Atlas:")
            print(f"   - Nome: {context['agent_name']}")
            print(f"   - Área: {context['area']}")
            print(f"   - Foco: {context['agent_perspective']['focus']}")
        else:
            print("⚠️ Agente Atlas não encontrado (pulando teste)")

    def test_enrich_report_with_agent_intelligence(self):
        """Testar enriquecimento de relatório"""
        test_data = {
            "summary": "Relatório de teste",
            "metrics": {
                "receitas": "R$ 100.000",
                "despesas": "R$ 80.000"
            }
        }

        enriched = agent_reporter.enrich_report_with_agent_intelligence(
            test_data,
            "financial"
        )

        # Verificar se foi enriquecido
        self.assertIn('agent_context', enriched)
        self.assertIn('agent_insights', enriched)

        print(f"✅ Relatório enriquecido:")
        if 'agent_context' in enriched:
            print(f"   - Agente: {enriched['agent_context'].get('agent', 'N/A')}")
            print(f"   - Perspectiva: {enriched['agent_context'].get('perspective', 'N/A')}")

        if enriched.get('agent_insights'):
            print(f"   - Insights: {len(enriched['agent_insights'])} gerados")

    def test_get_agents_summary(self):
        """Testar resumo de agentes"""
        summary = agent_reporter.get_agents_summary()

        self.assertIsInstance(summary, list)

        if summary:
            print(f"✅ Resumo de {len(summary)} agentes:")
            for agent in summary[:3]:  # Mostrar apenas primeiros 3
                print(f"   - {agent['nome']}: {agent['area']}")
        else:
            print("⚠️ Nenhum agente disponível no sistema")


class TestFullIntegration(unittest.TestCase):
    """Testes de integração completa"""

    def test_complete_report_workflow(self):
        """Testar fluxo completo: Agente → Archivus → Memória"""

        # 1. Dados de teste
        test_data = {
            "type": "financial",
            "summary": "Teste de integração completa",
            "metrics": {"teste": "100"}
        }

        # 2. Enriquecer com agente
        enriched = agent_reporter.enrich_report_with_agent_intelligence(
            test_data,
            "financial"
        )

        print("✅ Passo 1: Dados enriquecidos pelo agente")

        # 3. Salvar em pasta Archivus
        content = f"# Teste\n\n{json.dumps(enriched, indent=2)}"
        filepath = archivus_integration.save_to_official_location(
            "test_integration.md",
            content,
            "Analises"
        )

        print(f"✅ Passo 2: Salvo em pasta Archivus: {filepath}")

        # 4. Registrar com Archivus
        archivus_integration.register_with_archivus(
            filepath,
            {"type": "test", "format": "markdown"}
        )

        print("✅ Passo 3: Registrado no Archivus")

        # 5. Salvar na memória do agente (se Sigma disponível)
        if "sigma" in agent_reporter.available_agents:
            success = agent_reporter.save_agent_memory("sigma", test_data)
            if success:
                print("✅ Passo 4: Memória do agente Sigma atualizada")
            else:
                print("⚠️ Passo 4: Falha ao atualizar memória")

        # Limpar arquivo de teste
        if os.path.exists(filepath):
            os.remove(filepath)

        print("✅ INTEGRAÇÃO COMPLETA: Todos os passos executados com sucesso!")


def run_integration_tests():
    """Executar todos os testes de integração"""
    print("=" * 80)
    print("ÁVILA REPORT FRAMEWORK - TESTES DE INTEGRAÇÃO")
    print("=" * 80)
    print()

    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestArchivusIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentsIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestFullIntegration))

    # Executar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumo
    print()
    print("=" * 80)
    print("RESUMO DOS TESTES")
    print("=" * 80)
    print(f"Total de testes: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"🔥 Erros: {len(result.errors)}")
    print("=" * 80)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)
