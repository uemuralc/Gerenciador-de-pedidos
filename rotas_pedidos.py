from flask import Blueprint, request, jsonify
from datetime import datetime
from database import obter_conexao
from auth import login_obrigatorio

# Criando o Blueprint de Pedidos
pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/api/pedidos', methods=['GET', 'POST'])
@login_obrigatorio
def gerenciar_pedidos():
    conn = obter_conexao()
    if request.method == 'POST':
        dados = request.json
        id_pedido = int(datetime.timestamp(datetime.now()))
        conn.execute('INSERT INTO pedidos (id, cliente, item, status, total) VALUES (?, ?, ?, ?, ?)',
                     (id_pedido, dados['cliente'], dados['item'], 'Pendente', float(dados['total'])))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Pedido cadastrado!"}), 201

    pedidos = conn.execute('SELECT * FROM pedidos').fetchall()
    conn.close()
    return jsonify([dict(p) for p in pedidos])

@pedidos_bp.route('/api/pedidos/<int:id_pedido>', methods=['PUT', 'DELETE'])
@login_obrigatorio
def acoes_pedido(id_pedido):
    conn = obter_conexao()
    if request.method == 'DELETE':
        conn.execute('DELETE FROM pedidos WHERE id = ?', (id_pedido,))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Pedido excluído!"}), 200

    if request.method == 'PUT':
        dados = request.json
        if 'status' in dados:
            conn.execute('UPDATE pedidos SET status = ? WHERE id = ?', (dados['status'], id_pedido))
        else:
            conn.execute('UPDATE pedidos SET cliente = ?, item = ?, total = ? WHERE id = ?', 
                         (dados['cliente'], dados['item'], float(dados['total']), id_pedido))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Atualizado com sucesso!"}), 200