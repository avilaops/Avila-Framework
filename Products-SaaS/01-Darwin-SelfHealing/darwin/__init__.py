"""
🧬 Darwin - Self-Healing Python Library

Sua aplicação que aprende com os próprios erros e se auto-corrige.

Usage:
    from darwin import heal

    @heal
    def minha_funcao():
        # Código que será auto-corrigido
        pass
"""

__version__ = "1.0.0"
__author__ = "Nicolas Ávila"
__email__ = "nicolas@avila.inc"
__url__ = "https://github.com/avila/darwin"

from .core import Darwin, SelfHealing, heal
from .patterns import PatternMatcher, ErrorPattern
from .storage import LearningStorage

__all__ = [
    "Darwin",
    "SelfHealing",
    "heal",
    "PatternMatcher",
    "ErrorPattern",
    "LearningStorage"
]
