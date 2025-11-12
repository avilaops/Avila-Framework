# coding: utf-8
"""
Script: __init__.py
Função: Inicialização do módulo core
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
"""

from .config import settings
from .logging_config import setup_logging
from .sentry_config import init_sentry

__all__ = ["settings", "setup_logging", "init_sentry"]