"""
Darwin Core - Self-Healing Engine
"""

import functools
import traceback
import sys
from typing import Callable, Any, Optional
from .patterns import PatternMatcher
from .storage import LearningStorage
from .fixes import AutoFix


class Darwin:
    """
    Motor principal do Darwin Self-Healing System

    Usage:
        darwin = Darwin(auto_install_packages=True)

        @darwin.heal
        def minha_funcao():
            # Auto-corrigido
            pass
    """

    def __init__(
        self,
        auto_install_packages: bool = True,
        auto_fix_ports: bool = True,
        auto_fix_permissions: bool = False,
        learning_mode: bool = True,
        safe_mode: bool = False,
        notification: bool = True,
        storage_path: str = "./darwin_knowledge",
        max_retries: int = 3
    ):
        self.auto_install_packages = auto_install_packages
        self.auto_fix_ports = auto_fix_ports
        self.auto_fix_permissions = auto_fix_permissions
        self.learning_mode = learning_mode
        self.safe_mode = safe_mode
        self.notification = notification
        self.max_retries = max_retries

        # Componentes
        self.pattern_matcher = PatternMatcher()
        self.storage = LearningStorage(storage_path) if learning_mode else None
        self.auto_fix = AutoFix(self)

        print("🧬 Darwin initialized - Self-healing active")

    def heal(self, func: Callable) -> Callable:
        """
        Decorator que aplica self-healing em uma função

        Usage:
            @darwin.heal
            def minha_funcao():
                pass
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            last_error = None

            while retries < self.max_retries:
                try:
                    # Tenta executar função
                    result = func(*args, **kwargs)

                    # Sucesso - registra se houve erro antes
                    if last_error and self.learning_mode:
                        self.storage.save_success(last_error, result)

                    return result

                except Exception as e:
                    last_error = e
                    retries += 1

                    if self.notification:
                        print(f"⚠️  Darwin detectou erro: {type(e).__name__}: {str(e)}")

                    # Analisa padrão de erro
                    pattern = self.pattern_matcher.match(e)

                    if pattern:
                        if self.notification:
                            print(f"🔍 Pattern identificado: {pattern.id} - {pattern.title}")

                        # Verifica se já aprendeu correção
                        learned_fix = self.storage.get_learned_fix(pattern.id) if self.storage else None

                        if learned_fix:
                            if self.notification:
                                print(f"🧠 Darwin lembra a solução! Aplicando...")
                            fix_func = learned_fix['fix_function']
                        else:
                            if self.notification:
                                print(f"🛠️  Aplicando correção padrão...")
                            fix_func = pattern.fix_function

                        # Aplica correção
                        if not self.safe_mode or pattern.safe:
                            try:
                                fix_result = self.auto_fix.apply(fix_func, e, pattern)

                                # Salva aprendizado
                                if self.learning_mode and fix_result['success']:
                                    self.storage.save_fix(pattern, fix_result)
                                    if self.notification:
                                        print(f"✅ Correção aplicada! Tentando novamente...")

                                # Retry
                                continue

                            except Exception as fix_error:
                                if self.notification:
                                    print(f"❌ Falha ao aplicar correção: {str(fix_error)}")

                    else:
                        if self.notification:
                            print(f"❓ Pattern não identificado - erro não tratável automaticamente")

                    # Se chegou aqui, não conseguiu corrigir
                    if retries >= self.max_retries:
                        if self.notification:
                            print(f"💥 Darwin não conseguiu corrigir após {self.max_retries} tentativas")
                        raise

            # Nunca deveria chegar aqui
            raise last_error

        return wrapper


class SelfHealing:
    """
    Context manager para self-healing

    Usage:
        with SelfHealing() as healer:
            # Código auto-corrigido
            pass
    """

    def __init__(self, **kwargs):
        self.darwin = Darwin(**kwargs)
        self.original_excepthook = None

    def __enter__(self):
        # Intercepta todas as exceções não tratadas
        self.original_excepthook = sys.excepthook

        def darwin_excepthook(exc_type, exc_value, exc_traceback):
            # Tenta auto-corrigir
            pattern = self.darwin.pattern_matcher.match(exc_value)

            if pattern:
                print(f"🧬 Darwin interceptou exceção não tratada")
                print(f"🔍 Pattern: {pattern.title}")
                print(f"🛠️  Tentando auto-correção...")

                try:
                    fix_result = self.darwin.auto_fix.apply(
                        pattern.fix_function,
                        exc_value,
                        pattern
                    )

                    if fix_result['success']:
                        print(f"✅ Correção aplicada!")
                        return

                except Exception as e:
                    print(f"❌ Falha na correção: {str(e)}")

            # Se não corrigiu, mostra erro normal
            self.original_excepthook(exc_type, exc_value, exc_traceback)

        sys.excepthook = darwin_excepthook
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Restaura excepthook original
        sys.excepthook = self.original_excepthook

        # Não suprime exceções
        return False


# Singleton para uso simples
_default_darwin = Darwin()

def heal(func: Callable) -> Callable:
    """
    Decorator simples para self-healing

    Usage:
        from darwin import heal

        @heal
        def minha_funcao():
            pass
    """
    return _default_darwin.heal(func)
