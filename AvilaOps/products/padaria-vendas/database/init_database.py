# coding: utf-8
"""
Script: init_database.py
Função: Inicializar banco de dados com produtos da padaria
Autor: Nicolas Avila
Data: 2025-11-10
Projeto: Avila Inc / Avila Ops
"""

import sqlite3
import os

# Caminho do banco
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'padaria.db')

def init_database():
    """Inicializa o banco de dados com tabelas e dados iniciais"""

    # Criar diretório se não existir
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criar tabelas
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_nome TEXT,
            cliente_telefone TEXT,
            itens TEXT,
            total REAL,
            status TEXT DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Verificar se já existem produtos
    cursor.execute("SELECT COUNT(*) FROM produtos")
    count = cursor.fetchone()[0]

    if count == 0:
        # Inserir produtos iniciais
        produtos = [
            ('Pão Francês', 'Pão francês fresquinho da padaria', 0.50, 'pães', '🍞'),
            ('Pão de Forma', 'Pão de forma integral 500g', 8.90, 'pães', '🍞'),
            ('Croissant', 'Croissant francês com manteiga', 4.50, 'pães', '🥐'),
            ('Bolo de Chocolate', 'Bolo caseiro de chocolate com cobertura', 25.00, 'bolos', '🍰'),
            ('Bolo de Cenoura', 'Bolo de cenoura com chocolate', 22.00, 'bolos', '🥕'),
            ('Torta de Limão', 'Torta de limão siciliano', 28.00, 'bolos', '🍋'),
            ('Coxinha', 'Coxinha de frango com catupiry', 4.50, 'salgados', '🥟'),
            ('Empada', 'Empada de frango ou palmito', 5.00, 'salgados', '🥧'),
            ('Pão de Queijo', 'Pão de queijo mineiro (6 unidades)', 6.00, 'salgados', '🧀'),
            ('Café Expresso', 'Café expresso premium', 3.00, 'bebidas', '☕'),
            ('Cappuccino', 'Cappuccino cremoso', 5.50, 'bebidas', '☕'),
            ('Suco Natural', 'Suco de laranja, acerola ou maracujá', 4.00, 'bebidas', '🧃'),
            ('Sonho', 'Sonho recheado com doce de leite', 3.50, 'doces', '🍩'),
            ('Brigadeiro', 'Brigadeiro gourmet (unidade)', 2.00, 'doces', '🍫'),
            ('Torta Doce', 'Torta holandesa ou mousse', 35.00, 'doces', '🎂')
        ]

        cursor.executemany('''
            INSERT INTO produtos (nome, descricao, preco, categoria, imagem)
            VALUES (?, ?, ?, ?, ?)
        ''', produtos)

        print(f"✅ Inseridos {len(produtos)} produtos no banco")

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")
    print(f"📍 Local: {DB_PATH}")

if __name__ == "__main__":
    init_database()
