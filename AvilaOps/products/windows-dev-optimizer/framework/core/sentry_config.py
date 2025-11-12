# coding: utf-8
"""
Script: sentry.py
Função: Integração com Sentry para monitoramento
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Configuração opcional do Sentry
"""

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from .config import settings

def init_sentry():
    """Inicializa Sentry se DSN estiver configurado"""
    dsn = settings.sentry_dsn or settings.sentry_token_api
    
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            environment=settings.app_env,
            integrations=[
                FastApiIntegration(auto_enabling_integrations=False),
                LoggingIntegration(
                    level=None,        # Capturar todos os logs
                    event_level=None   # Não enviar logs como eventos
                ),
            ],
            # Filtrar informações sensíveis
            before_send=filter_sensitive_data
        )
        
        sentry_sdk.set_tag("app_name", settings.app_name)
        sentry_sdk.set_tag("app_version", settings.app_version)
        
        return True
    
    return False

def filter_sensitive_data(event, hint):
    """Filtra dados sensíveis antes de enviar para Sentry"""
    # Remover campos sensíveis
    sensitive_keys = ['password', 'token', 'key', 'secret', 'smtp_pass']
    
    def clean_dict(data):
        if isinstance(data, dict):
            cleaned = {}
            for k, v in data.items():
                if any(sensitive in k.lower() for sensitive in sensitive_keys):
                    cleaned[k] = "[FILTERED]"
                else:
                    cleaned[k] = clean_dict(v)
            return cleaned
        elif isinstance(data, list):
            return [clean_dict(item) for item in data]
        else:
            return data
    
    if 'extra' in event:
        event['extra'] = clean_dict(event['extra'])
    
    if 'contexts' in event:
        event['contexts'] = clean_dict(event['contexts'])
    
    return event

def capture_exception(exception=None):
    """Captura exceção no Sentry"""
    sentry_sdk.capture_exception(exception)

def capture_message(message, level="info"):
    """Captura mensagem no Sentry"""
    sentry_sdk.capture_message(message, level=level)