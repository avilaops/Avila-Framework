"""
Darwin Pattern Matcher - Identifica padrões de erro
"""

import re
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass


@dataclass
class ErrorPattern:
    """Representa um padrão de erro detectável"""
    id: str
    title: str
    pattern: str  # Regex ou substring
    severity: str  # 'error', 'warning', 'info'
    fix_function: Callable
    safe: bool = True  # Se é seguro aplicar em produção
    description: str = ""


class PatternMatcher:
    """
    Detecta padrões de erro e retorna correção apropriada
    """

    def __init__(self):
        self.patterns: List[ErrorPattern] = []
        self._load_builtin_patterns()

    def _load_builtin_patterns(self):
        """Carrega os 12 padrões built-in do Darwin"""

        from .fixes import (
            fix_module_not_found,
            fix_port_in_use,
            fix_permission_denied,
            fix_connection_timeout,
            fix_file_not_found,
            fix_import_error,
            fix_memory_error,
            fix_disk_full
        )

        self.patterns = [
            ErrorPattern(
                id="MODULE_NOT_FOUND",
                title="Módulo Python não encontrado",
                pattern=r"ModuleNotFoundError: No module named ['\"](.+)['\"]",
                severity="error",
                fix_function=fix_module_not_found,
                safe=True,
                description="Instala o módulo automaticamente via pip"
            ),

            ErrorPattern(
                id="PORT_IN_USE",
                title="Porta já está em uso",
                pattern=r"(?:Address already in use|Port \d+ is already in use)",
                severity="error",
                fix_function=fix_port_in_use,
                safe=True,
                description="Tenta porta alternativa ou mata processo"
            ),

            ErrorPattern(
                id="PERMISSION_DENIED",
                title="Permissão negada",
                pattern=r"PermissionError: \[Errno 13\] Permission denied",
                severity="error",
                fix_function=fix_permission_denied,
                safe=False,
                description="Ajusta permissões do arquivo/diretório"
            ),

            ErrorPattern(
                id="CONNECTION_TIMEOUT",
                title="Timeout de conexão",
                pattern=r"(?:ConnectionTimeout|TimeoutError|timed out)",
                severity="warning",
                fix_function=fix_connection_timeout,
                safe=True,
                description="Retry com exponential backoff"
            ),

            ErrorPattern(
                id="FILE_NOT_FOUND",
                title="Arquivo não encontrado",
                pattern=r"FileNotFoundError: \[Errno 2\] No such file or directory: ['\"](.+)['\"]",
                severity="error",
                fix_function=fix_file_not_found,
                safe=True,
                description="Cria arquivo/diretório ausente"
            ),

            ErrorPattern(
                id="IMPORT_ERROR",
                title="Erro de importação",
                pattern=r"ImportError: (.+)",
                severity="error",
                fix_function=fix_import_error,
                safe=True,
                description="Instala dependências faltantes"
            ),

            ErrorPattern(
                id="MEMORY_ERROR",
                title="Memória insuficiente",
                pattern=r"MemoryError",
                severity="error",
                fix_function=fix_memory_error,
                safe=True,
                description="Libera memória não utilizada"
            ),

            ErrorPattern(
                id="DISK_FULL",
                title="Disco cheio",
                pattern=r"(?:No space left on device|Disk quota exceeded)",
                severity="error",
                fix_function=fix_disk_full,
                safe=False,
                description="Limpa arquivos temporários"
            ),
        ]

    def match(self, error: Exception) -> Optional[ErrorPattern]:
        """
        Encontra padrão correspondente ao erro

        Args:
            error: Exceção Python

        Returns:
            ErrorPattern se encontrado, None caso contrário
        """
        error_str = str(error)
        error_type = type(error).__name__

        for pattern in self.patterns:
            # Tenta match por regex
            if re.search(pattern.pattern, error_str, re.IGNORECASE):
                return pattern

            # Tenta match por tipo de erro
            if pattern.id in error_type.upper():
                return pattern

        return None

    def add_custom_pattern(self, pattern: ErrorPattern):
        """Adiciona pattern customizado (Darwin Pro)"""
        self.patterns.append(pattern)

    def get_all_patterns(self) -> List[ErrorPattern]:
        """Retorna todos os patterns registrados"""
        return self.patterns
