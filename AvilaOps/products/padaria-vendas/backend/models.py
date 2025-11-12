# coding: utf-8
"""
Script: models.py
Função: Modelos de dados para plataforma de vendas da padaria
Autor: Nicolas Avila
Data: 2025-11-10
Projeto: Avila Inc / Avila Ops
"""

from datetime import datetime
import sqlite3
import json

class Database:
    def __init__(self, db_path='../../database/padaria.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL NOT NULL,
                    categoria TEXT,
                    imagem TEXT,
                    disponivel BOOLEAN DEFAULT 1,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de pedidos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_nome TEXT,
                    cliente_telefone TEXT,
                    itens TEXT,  -- JSON com itens do pedido
                    total REAL,
                    status TEXT DEFAULT 'pendente',
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def get_produtos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM produtos WHERE disponivel = 1")
            rows = cursor.fetchall()

            produtos = []
            for row in rows:
                produto = {
                    'id': row[0],
                    'nome': row[1],
                    'descricao': row[2],
                    'preco': row[3],
                    'categoria': row[4],
                    'imagem': row[5],
                    'disponivel': bool(row[6])
                }
                produtos.append(produto)

            return produtos

    def criar_pedido(self, cliente_nome, cliente_telefone, itens, total):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            itens_json = json.dumps(itens)

            cursor.execute('''
                INSERT INTO pedidos (cliente_nome, cliente_telefone, itens, total)
                VALUES (?, ?, ?, ?)
            ''', (cliente_nome, cliente_telefone, itens_json, total))

            pedido_id = cursor.lastrowid
            conn.commit()

            return pedido_id

    def get_pedidos(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos ORDER BY criado_em DESC")
            rows = cursor.fetchall()

            pedidos = []
            for row in rows:
                pedido = {
                    'id': row[0],
                    'cliente_nome': row[1],
                    'cliente_telefone': row[2],
                    'itens': json.loads(row[3]),
                    'total': row[4],
                    'status': row[5],
                    'criado_em': row[6]
                }
                pedidos.append(pedido)

            return pedidos

# Instancia global do banco
db = Database()
