import os
from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from database import obter_conexao
import cloudinary
import cloudinary.uploader
from io import BytesIO
import openpyxl

cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET') 
)

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/api/pedidos', methods=['GET', 'POST'])
def gerenciar_pedidos():
    conn = obter_conexao()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        cliente = request.form.get('cliente')
        contato = request.form.get('contato')
        item = request.form.get('item')
        material_origem = request.form.get('material_origem')
        arquivo = request.files.get('documento')
        
        documento_url = None
        
        if arquivo:
            resultado = cloudinary.uploader.upload(arquivo, resource_type="auto")
            documento_url = resultado.get('secure_url')

        id_pedido = int(datetime.timestamp(datetime.now()))
        
        cursor.execute('INSERT INTO pedidos (id, cliente, contato, item, material_origem, status, documento_url) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                     (id_pedido, cliente, contato, item, material_origem, 'Pendente', documento_url))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Pedido cadastrado com sucesso!"}), 201

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
            cursor.execute('UPDATE pedidos SET cliente = %s, contato = %s, item = %s, material_origem = %s WHERE id = %s', 
                         (dados['cliente'], dados['contato'], dados['item'], dados['material_origem'], id_pedido))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Atualizado com sucesso!"}), 200

@pedidos_bp.route('/api/pedidos/exportar', methods=['GET'])
def exportar_pedidos_excel():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pedidos"

    ws.append(['ID', 'Cliente', 'Contato', 'Descrição', 'Material', 'Status'])
    for celula in ws[1]:
        celula.font = openpyxl.styles.Font(bold=True)

    for p in pedidos:
        ws.append([p['id'], p['cliente'], p['contato'], p['item'], p['material_origem'], p['status']])

    for coluna in ws.columns:
        largura = max(len(str(c.value)) for c in coluna if c.value is not None) + 2
        ws.column_dimensions[coluna[0].column_letter].width = largura

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name='pedidos.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )