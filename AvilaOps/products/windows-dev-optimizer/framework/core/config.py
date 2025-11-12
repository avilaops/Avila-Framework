# coding: utf-8
"""
Script: config.py
Função: Configurações centralizadas do framework FastAPI
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Configurações usando Pydantic BaseSettings
"""

from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    # App
    app_name: str = Field(default="Windows Dev Optimizer Framework", env="APP_NAME")
    app_env: str = Field(default="dev", env="APP_ENV")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    
    # WhatsApp
    whatsapp_to: str = Field(default="+5517997811471", env="WHATSAPP_TO")
    whatsapp_access_token: Optional[str] = Field(default=None, env="WHATSAPP_ACCESS_TOKEN")
    whatsapp_phone_id: Optional[str] = Field(default=None, env="WHATSAPP_PHONE_NUMBER_ID")
    
    # SMTP
    smtp_host: Optional[str] = Field(default="smtp.office365.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, env="SMTP_USER")
    smtp_pass: Optional[str] = Field(default=None, env="SMTP_PASS")
    smtp_from: Optional[str] = Field(default="noreply@avila.inc", env="SMTP_FROM")
    smtp_to: str = Field(default="nicolas@avila.inc", env="SMTP_TO")
    
    # Sentry
    sentry_token_api: Optional[str] = Field(default=None, env="SENTRY_TOKEN_API")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    
    # Paths
    output_dir: str = Field(default="output", env="OUTPUT_DIR")
    logs_dir: str = Field(default="logs", env="LOGS_DIR")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Instância global
settings = Settings()