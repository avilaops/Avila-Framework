# coding: utf-8
"""
Script: app.py
Função: API REST para plataforma de vendas da padaria
Autor: Nicolas Avila
Data: 2025-11-10
Projeto: Avila Inc / Avila Ops
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db

app = Flask(__name__)
CORS(app)  # Permite requests do frontend

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    """Retorna lista de produtos disponíveis"""
    try:
        produtos = db.get_produtos()
        return jsonify({'success': True, 'produtos': produtos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pedidos', methods=['POST'])
def criar_pedido():
    """Cria um novo pedido"""
    try:
        data = request.get_json()

        cliente_nome = data.get('cliente_nome')
        cliente_telefone = data.get('cliente_telefone')
        itens = data.get('itens', [])
        total = data.get('total', 0)

        if not cliente_nome or not itens:
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400

        pedido_id = db.criar_pedido(cliente_nome, cliente_telefone, itens, total)

        return jsonify({
            'success': True,
            'pedido_id': pedido_id,
            'message': 'Pedido criado com sucesso'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    """Retorna lista de pedidos (para admin)"""
    try:
        pedidos = db.get_pedidos()
        return jsonify({'success': True, 'pedidos': pedidos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Página inicial da API"""
    return jsonify({
        'message': 'API Plataforma de Vendas - Padaria Rio Preto',
        'endpoints': {
            'GET /api/produtos': 'Lista produtos',
            'POST /api/pedidos': 'Cria pedido',
            'GET /api/pedidos': 'Lista pedidos'
        }
    })

if __name__ == '__main__':
    print("Iniciando API da Padaria...")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
