from flask import Blueprint, request, jsonify
from datetime import datetime
from database import obter_conexao
from auth import login_obrigatorio

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/api/estoque', methods=['GET', 'POST'])
@login_obrigatorio
def gerenciar_estoque():
    conn = obter_conexao()
    if request.method == 'POST':
        dados = request.json
        id_material = int(datetime.timestamp(datetime.now()))
        conn.execute('INSERT INTO estoque (id, nome, quantidade, unidade) VALUES (?, ?, ?, ?)',
                     (id_material, dados['nome'], float(dados['quantidade']), dados['unidade']))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Material adicionado!"}), 201

    estoque = conn.execute('SELECT * FROM estoque').fetchall()
    conn.close()
    return jsonify([dict(m) for m in estoque])

@estoque_bp.route('/api/estoque/<int:id_material>', methods=['PUT', 'DELETE'])
@login_obrigatorio
def acoes_estoque(id_material):
    conn = obter_conexao()
    if request.method == 'DELETE':
        conn.execute('DELETE FROM estoque WHERE id = ?', (id_material,))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Material excluído!"}), 200

    if request.method == 'PUT':
        dados = request.json
        if 'nome' in dados:
            conn.execute('UPDATE estoque SET nome = ?, quantidade = ?, unidade = ? WHERE id = ?',
                         (dados['nome'], max(0, float(dados['quantidade'])), dados['unidade'], id_material))
        else:
            conn.execute('UPDATE estoque SET quantidade = ? WHERE id = ?',
                         (max(0, float(dados['quantidade'])), id_material))
        conn.commit()
        conn.close()
        return jsonify({"mensagem": "Estoque atualizado!"}), 200