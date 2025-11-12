# coding: utf-8
"""
Script: logging.py
Função: Sistema de logging estruturado
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Logging JSON estruturado com rotação de arquivos
"""

import logging
import json
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """Formatter para logs estruturados em JSON"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Adicionar campos extras se existirem
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
            
        # Adicionar exception se existir
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging():
    """Configura o sistema de logging"""
    # Criar diretório de logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configurar handler rotativo
    log_file = logs_dir / "app.log"
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1_000_000,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # Aplicar formatter JSON
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    
    # Configurar logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    # Handler para console (desenvolvimento)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    return root_logger

def get_logger(name: str):
    """Obtém logger específico"""
    return logging.getLogger(name)

def log_with_context(logger, level, message, **context):
    """Log com contexto adicional"""
    record = logger.makeRecord(
        logger.name, level, "", 0, message, (), None
    )
    record.extra_fields = context
    logger.handle(record)