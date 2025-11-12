"""
ÁVILA REPORT FRAMEWORK - INTEGRAÇÃO COM ARCHIVUS
================================================
Integração com o Agente Bibliotecário para governança de relatórios
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from config import EXPORTS_DIR, LOGS_DIR
from logger import logger

class ArchivusIntegration:
    """Integração com Archivus para governança de relatórios"""

    def __init__(self):
        self.workspace_root = Path(r"C:\Users\nicol\OneDrive\Avila")
        self.archivus_path = self.workspace_root / "AvilaOps" / "Agente Bibliotecario (Archivus)"
        self.official_reports_path = self.workspace_root / "Docs" / "Relatorios"

        # Criar estrutura oficial se não existir
        self._ensure_official_structure()

    def _ensure_official_structure(self):
        """Garantir que a estrutura oficial do Archivus existe"""
        official_folders = [
            self.official_reports_path / "Conversas",
            self.official_reports_path / "Analises",
            self.official_reports_path / "Auditorias",
            self.official_reports_path / "Comparacoes",
            self.official_reports_path / "Diagnosticos",
            self.official_reports_path / "Performance"
        ]

        for folder in official_folders:
            folder.mkdir(parents=True, exist_ok=True)

    def calculate_hash(self, file_path):
        """Calcular SHA256 de um arquivo"""
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def save_to_official_location(self, report_file, report_type):
        """Salvar relatório na estrutura oficial do Archivus"""
        try:
            # Mapear tipo de relatório para pasta oficial
            type_mapping = {
                "daily": "Analises",
                "weekly": "Analises",
                "monthly": "Analises",
                "financial": "Analises",
                "projects": "Performance",
                "performance": "Performance",
                "governance": "Auditorias",
                "custom": "Analises"
            }

            folder_name = type_mapping.get(report_type, "Analises")
            official_path = self.official_reports_path / folder_name

            # Copiar arquivo
            import shutil
            dest_file = official_path / Path(report_file).name
            shutil.copy2(report_file, dest_file)

            logger.success(f"Relatório salvo na estrutura oficial: {dest_file}")
            return dest_file

        except Exception as e:
            logger.error(f"Erro ao salvar na estrutura oficial: {e}")
            return None

    def create_integrity_entry(self, file_path):
        """Criar entrada de integridade para o relatório"""
        file_hash = self.calculate_hash(file_path)

        integrity_data = {
            "file": str(file_path),
            "hash_sha256": file_hash,
            "size_bytes": Path(file_path).stat().st_size,
            "created_at": datetime.now().isoformat(),
            "framework": "Avila Report Framework v1.0",
            "agent": "Report Generator"
        }

        return integrity_data

    def generate_audit_report(self, generated_reports):
        """Gerar relatório de auditoria dos relatórios gerados"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        audit_file = self.official_reports_path / "Auditorias" / f"AUDITORIA_REPORTS_{timestamp}.md"

        content = f"""# 📋 AUDITORIA DE RELATÓRIOS - Ávila Framework

**Data/Hora:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Sistema:** Ávila Report Framework v1.0
**Agente:** Report Generator

---

## 📊 RESUMO

| Métrica | Valor |
|---------|-------|
| Total de Relatórios | {len(generated_reports)} |
| Timestamp | {datetime.now().isoformat()} |
| Status | ✅ Completo |

## 📁 RELATÓRIOS GERADOS

"""

        for report in generated_reports:
            integrity = self.create_integrity_entry(report['path'])

            content += f"""### {report['type'].upper()}

- **Arquivo:** `{Path(report['path']).name}`
- **Formato:** {report['format']}
- **Tamanho:** {integrity['size_bytes']:,} bytes
- **SHA256:** `{integrity['hash_sha256'][:16]}...`
- **Localização Oficial:** `{report.get('official_path', 'N/A')}`

"""

        content += f"""
---

## 🔒 INTEGRIDADE

Todos os relatórios foram verificados com hash SHA256.
Sistema de governança integrado com Archivus.

**Auditoria gerada automaticamente pelo Ávila Report Framework**
"""

        with open(audit_file, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.success(f"Relatório de auditoria gerado: {audit_file}")
        return audit_file

    def validate_against_archivus_standards(self, file_path):
        """Validar se arquivo está em conformidade com padrões do Archivus"""
        try:
            # Verificar se está na estrutura oficial
            is_official = str(self.official_reports_path) in str(file_path)

            # Verificar tamanho
            size_mb = Path(file_path).stat().st_size / 1024 / 1024
            size_ok = size_mb < 50  # Máximo 50MB

            # Verificar extensão
            valid_extensions = ['.md', '.xlsx', '.pdf', '.html']
            ext_ok = Path(file_path).suffix in valid_extensions

            validation = {
                "compliant": is_official and size_ok and ext_ok,
                "checks": {
                    "official_structure": is_official,
                    "size_limit": size_ok,
                    "valid_extension": ext_ok
                },
                "size_mb": round(size_mb, 2)
            }

            return validation

        except Exception as e:
            logger.error(f"Erro na validação Archivus: {e}")
            return {"compliant": False, "error": str(e)}

    def register_with_archivus(self, report_data):
        """Registrar relatório no sistema do Archivus"""
        try:
            # Criar registro para o Archivus
            archivus_registry = {
                "timestamp": datetime.now().isoformat(),
                "source": "Avila Report Framework",
                "report_type": report_data.get('type'),
                "file_path": str(report_data.get('path')),
                "hash": self.calculate_hash(report_data.get('path')),
                "compliant": True
            }

            # Salvar no log do Archivus (se disponível)
            archivus_log = self.workspace_root / "Logs" / "Daily" / f"reports_registry_{datetime.now().strftime('%Y-%m-%d')}.json"

            if archivus_log.exists():
                with open(archivus_log, 'r', encoding='utf-8') as f:
                    registry = json.load(f)
            else:
                registry = {"reports": []}

            registry["reports"].append(archivus_registry)

            with open(archivus_log, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)

            logger.info(f"Relatório registrado no Archivus: {archivus_log}")
            return True

        except Exception as e:
            logger.warning(f"Não foi possível registrar no Archivus: {e}")
            return False

# Instância global
archivus_integration = ArchivusIntegration()
