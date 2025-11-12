# coding: utf-8
"""
Script: __init__.py
Função: Inicialização do módulo services
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
"""

from .reporting import WindowsOptimizerService, get_optimizer_service

__all__ = ["WindowsOptimizerService", "get_optimizer_service"]