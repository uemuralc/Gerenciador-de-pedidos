from flask import Blueprint, request, jsonify
from datetime import datetime
from database import obter_conexao

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/api/pedidos', methods=['GET', 'POST'])
def gerenciar_pedidos():
    conn = obter_conexao()
    cursor = conn.cursor() 
    
    if request.method == 'POST':
        dados = request.json
        id_pedido = int(datetime.timestamp(datetime.now()))
        cursor.execute('INSERT INTO pedidos (id, cliente, item, status, total) VALUES (%s, %s, %s, %s, %s)',
                     (id_pedido, dados['cliente'], dados['item'], 'Pendente', float(dados['total'])))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Pedido cadastrado!"}), 201

    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(p) for p in pedidos])

@pedidos_bp.route('/api/pedidos/<int:id_pedido>', methods=['PUT', 'DELETE'])
def acoes_pedido(id_pedido):
    conn = obter_conexao()
    cursor = conn.cursor()
    
    if request.method == 'DELETE':
        cursor.execute('DELETE FROM pedidos WHERE id = %s', (id_pedido,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Pedido excluído!"}), 200

    if request.method == 'PUT':
        dados = request.json
        if 'status' in dados:
            cursor.execute('UPDATE pedidos SET status = %s WHERE id = %s', (dados['status'], id_pedido))
        else:
            cursor.execute('UPDATE pedidos SET cliente = %s, item = %s, total = %s WHERE id = %s', 
                         (dados['cliente'], dados['item'], float(dados['total']), id_pedido))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Atualizado com sucesso!"}), 200