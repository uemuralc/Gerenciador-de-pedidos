from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from database import obter_conexao
from io import BytesIO 
import openpyxl

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/api/estoque', methods=['GET', 'POST'])
def gerenciar_estoque():
    conn = obter_conexao()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        dados = request.json
        id_material = int(datetime.timestamp(datetime.now()))
        cursor.execute('INSERT INTO estoque (id, nome, quantidade, unidade) VALUES (%s, %s, %s, %s)',
                     (id_material, dados['nome'], float(dados['quantidade']), dados['unidade']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Material adicionado!"}), 201

    cursor.execute('SELECT * FROM estoque')
    estoque = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(m) for m in estoque])

@estoque_bp.route('/api/estoque/<int:id_material>', methods=['PUT', 'DELETE'])
def acoes_estoque(id_material):
    conn = obter_conexao()
    cursor = conn.cursor()
    
    if request.method == 'DELETE':
        cursor.execute('DELETE FROM estoque WHERE id = %s', (id_material,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Material excluído!"}), 200

    if request.method == 'PUT':
        dados = request.json
        if 'nome' in dados:
            cursor.execute('UPDATE estoque SET nome = %s, quantidade = %s, unidade = %s WHERE id = %s',
                         (dados['nome'], max(0, float(dados['quantidade'])), dados['unidade'], id_material))
        else:
            cursor.execute('UPDATE estoque SET quantidade = %s WHERE id = %s',
                         (max(0, float(dados['quantidade'])), id_material))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Estoque atualizado!"}), 200

@estoque_bp.route('/api/estoque/exportar', methods=['GET'])
def exportar_estoque_excel():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque')
    estoque = cursor.fetchall()
    cursor.close()
    conn.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Estoque"

    ws.append(['ID', 'Material', 'Quantidade', 'Unidade'])
    for celula in ws[1]:
        celula.font = openpyxl.styles.Font(bold=True)

    for m in estoque:
        ws.append([m['id'], m['nome'], m['quantidade'], m['unidade']])

    for coluna in ws.columns:
        largura = max(len(str(c.value)) for c in coluna if c.value is not None) + 2
        ws.column_dimensions[coluna[0].column_letter].width = largura

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='estoque.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )