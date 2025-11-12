#!/usr/bin/env python3
"""
Script para encontrar e mover todos os arquivos .ps1 de subpastas para a pasta Scripts
"""

import os
import shutil
from pathlib import Path
import logging

def setup_logging():
    """Configura o logging para acompanhar as operações"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('mover_scripts.log'),
            logging.StreamHandler()
        ]
    )

def deve_ignorar_pasta(caminho):
    """
    Verifica se uma pasta deve ser ignorada baseado em padrões de exclusão
    
    Args:
        caminho (Path): Caminho da pasta para verificar
        
    Returns:
        bool: True se deve ignorar, False caso contrário
    """
    # Lista de pastas/arquivos a ignorar
    pastas_ignorar = {
        'node_modules',
        'dist',
        'coverage',
        '.vscode',
        '.git',
        '.svn',
        '__pycache__',
        'venv',
        'env'
    }
    
    # Lista de padrões de arquivos a ignorar
    arquivos_ignorar = {
        '.env',
        '.DS_Store',
        'azure-appsettings.json',
        'publish-profile.xml'
    }
    
    nome = caminho.name.lower()
    
    # Verifica se é uma pasta a ser ignorada
    if nome in pastas_ignorar:
        return True
    
    # Verifica se é um arquivo a ser ignorado
    if nome in arquivos_ignorar:
        return True
    
    # Verifica padrões específicos
    if nome.startswith('.env.') and nome != '.env.example':
        return True
    
    if nome.endswith('.publishsettings'):
        return True
    
    return False

def encontrar_arquivos_ps1(pasta_origem):
    """
    Encontra todos os arquivos .ps1 na pasta origem e subpastas
    
    Args:
        pasta_origem (str): Caminho da pasta para pesquisar
        
    Returns:
        list: Lista de caminhos dos arquivos .ps1 encontrados
    """
    arquivos_ps1 = []
    pasta_origem = Path(pasta_origem)
    
    logging.info(f"Procurando arquivos .ps1 em: {pasta_origem}")
    
    try:
        # Usa walk para ter mais controle sobre as pastas visitadas
        for root, dirs, files in os.walk(pasta_origem):
            root_path = Path(root)
            
            # Remove pastas que devem ser ignoradas da lista de diretórios a visitar
            dirs[:] = [d for d in dirs if not deve_ignorar_pasta(root_path / d)]
            
            # Processa arquivos .ps1 na pasta atual
            for file in files:
                if file.lower().endswith('.ps1'):
                    arquivo_path = root_path / file
                    
                    # Verifica se o arquivo deve ser ignorado
                    if not deve_ignorar_pasta(arquivo_path):
                        arquivos_ps1.append(arquivo_path)
                        logging.info(f"Encontrado: {arquivo_path}")
                    else:
                        logging.debug(f"Ignorado: {arquivo_path}")
    
    except PermissionError as e:
        logging.error(f"Erro de permissão ao acessar pasta: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
    
    return arquivos_ps1

def mover_arquivos(arquivos_ps1, pasta_destino):
    """
    Move os arquivos .ps1 para a pasta de destino
    
    Args:
        arquivos_ps1 (list): Lista de arquivos para mover
        pasta_destino (str): Pasta de destino
    """
    pasta_destino = Path(pasta_destino)
    
    # Cria a pasta de destino se não existir
    pasta_destino.mkdir(parents=True, exist_ok=True)
    
    movidos = 0
    erros = 0
    
    for arquivo in arquivos_ps1:
        try:
            # Verifica se o arquivo já está na pasta de destino
            if arquivo.parent == pasta_destino:
                logging.info(f"Arquivo já está na pasta de destino: {arquivo.name}")
                continue
            
            # Define o caminho de destino
            destino = pasta_destino / arquivo.name
            
            # Se já existe um arquivo com o mesmo nome no destino
            if destino.exists():
                # Cria um nome único adicionando um número
                contador = 1
                nome_base = arquivo.stem
                extensao = arquivo.suffix
                
                while destino.exists():
                    novo_nome = f"{nome_base}_{contador}{extensao}"
                    destino = pasta_destino / novo_nome
                    contador += 1
                
                logging.warning(f"Arquivo renomeado para evitar conflito: {destino.name}")
            
            # Move o arquivo
            shutil.move(str(arquivo), str(destino))
            logging.info(f"Movido: {arquivo} -> {destino}")
            movidos += 1
            
        except PermissionError as e:
            logging.error(f"Erro de permissão ao mover {arquivo}: {e}")
            erros += 1
        except Exception as e:
            logging.error(f"Erro ao mover {arquivo}: {e}")
            erros += 1
    
    return movidos, erros

def main():
    """Função principal do script"""
    setup_logging()
    
    # Definir os caminhos
    pasta_origem = r"C:\Users\nicol\OneDrive\Avila"
    pasta_destino = r"C:\Users\nicol\OneDrive\Avila\Scripts"
    
    logging.info("=" * 60)
    logging.info("INICIANDO SCRIPT DE MOVIMENTAÇÃO DE ARQUIVOS .PS1")
    logging.info("=" * 60)
    
    # Verificar se a pasta origem existe
    if not Path(pasta_origem).exists():
        logging.error(f"Pasta origem não encontrada: {pasta_origem}")
        return
    
    # Encontrar todos os arquivos .ps1
    arquivos_ps1 = encontrar_arquivos_ps1(pasta_origem)
    
    if not arquivos_ps1:
        logging.info("Nenhum arquivo .ps1 encontrado.")
        return
    
    logging.info(f"Total de arquivos .ps1 encontrados: {len(arquivos_ps1)}")
    
    # Mostrar lista de arquivos encontrados
    print("\nArquivos .ps1 encontrados:")
    print("-" * 40)
    for i, arquivo in enumerate(arquivos_ps1, 1):
        print(f"{i:2d}. {arquivo}")
    
    # Confirmar antes de mover
    resposta = input(f"\nDeseja mover {len(arquivos_ps1)} arquivo(s) para {pasta_destino}? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        # Mover os arquivos
        movidos, erros = mover_arquivos(arquivos_ps1, pasta_destino)
        
        logging.info("=" * 60)
        logging.info("OPERAÇÃO CONCLUÍDA")
        logging.info(f"Arquivos movidos com sucesso: {movidos}")
        logging.info(f"Erros encontrados: {erros}")
        logging.info("=" * 60)
        
        if erros > 0:
            logging.warning("Verifique os logs acima para detalhes dos erros.")
    else:
        logging.info("Operação cancelada pelo usuário.")

if __name__ == "__main__":
    main()