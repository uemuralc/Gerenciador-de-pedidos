import webview
from flask import Flask, render_template, jsonify, request, Response
from datetime import datetime
import sqlite3
import os
import csv

app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'banco_de_dados.db')

SENHA_SISTEMA = "1234"

def iniciar_banco():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, item TEXT, status TEXT NOT NULL, total REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY, nome TEXT NOT NULL, quantidade REAL NOT NULL, unidade TEXT NOT NULL
            )
        ''')
        conn.commit()

iniciar_banco()

def obter_conexao():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

# --- ROTAS DA INTERFACE ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ROTAS API: SEGURANÇA ---
@app.route('/api/login', methods=['POST'])
def verificar_login():
    dados = request.json
    if dados.get('senha', '') == SENHA_SISTEMA:
        return jsonify({"sucesso": True, "mensagem": "Acesso liberado!"}), 200
    return jsonify({"sucesso": False, "erro": "Senha incorreta!"}), 401

# --- ROTAS API: PEDIDOS ---
@app.route('/api/pedidos', methods=['GET', 'POST'])
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

@app.route('/api/pedidos/<int:id_pedido>', methods=['PUT', 'DELETE'])
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

# --- ROTAS API: ESTOQUE ---
@app.route('/api/estoque', methods=['GET', 'POST'])
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

@app.route('/api/estoque/<int:id_material>', methods=['PUT', 'DELETE'])
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

# --- CLASSE DE EXPORTAÇÃO NATIVA (Janela Salvar Como) ---
class ApiExportacao:
    def exportar_pedidos_nativ(self):
        janela_ativa = webview.windows[0]
        arquivo_salvar = janela_ativa.create_file_dialog(
            webview.SAVE_DIALOG, 
            directory='', # Deixamos vazio para o Windows usar a última pasta aberta
            save_filename='relatorio_pedidos.csv',
            file_types=('Arquivos CSV (*.csv)', 'Todos os arquivos (*.*)')
        )
        
        if not arquivo_salvar:
            return {"sucesso": False, "msg": "Cancelado"}

        # A CORREÇÃO: Extrai o texto do caminho caso o pywebview retorne uma lista/tupla
        caminho_final = arquivo_salvar[0] if isinstance(arquivo_salvar, (tuple, list)) else arquivo_salvar

        try:
            conn = obter_conexao()
            pedidos = conn.execute('SELECT * FROM pedidos').fetchall()
            conn.close()

            with open(caminho_final, mode='w', newline='', encoding='utf-8-sig') as f:
                cw = csv.writer(f, delimiter=';')
                cw.writerow(['ID', 'Cliente', 'Produto/Item', 'Status', 'Total (R$)'])
                for p in pedidos:
                    total_br = str(p['total']).replace('.', ',')
                    cw.writerow([p['id'], p['cliente'], p['item'], p['status'], total_br])
            
            return {"sucesso": True, "msg": "Relatório de pedidos salvo com sucesso!"}
        except Exception as e:
            return {"sucesso": False, "msg": str(e)}

    def exportar_estoque_nativ(self):
        janela_ativa = webview.windows[0]
        arquivo_salvar = janela_ativa.create_file_dialog(
            webview.SAVE_DIALOG, 
            directory='', 
            save_filename='relatorio_estoque.csv',
            file_types=('Arquivos CSV (*.csv)', 'Todos os arquivos (*.*)')
        )
        
        if not arquivo_salvar:
            return {"sucesso": False, "msg": "Cancelado"}

        # A CORREÇÃO
        caminho_final = arquivo_salvar[0] if isinstance(arquivo_salvar, (tuple, list)) else arquivo_salvar

        try:
            conn = obter_conexao()
            estoque = conn.execute('SELECT * FROM estoque').fetchall()
            conn.close()

            with open(caminho_final, mode='w', newline='', encoding='utf-8-sig') as f:
                cw = csv.writer(f, delimiter=';')
                cw.writerow(['ID', 'Material', 'Quantidade', 'Unidade'])
                for m in estoque:
                    qtd_br = str(m['quantidade']).replace('.', ',')
                    cw.writerow([m['id'], m['nome'], qtd_br, m['unidade']])
            
            return {"sucesso": True, "msg": "Relatório de estoque salvo com sucesso!"}
        except Exception as e:
            return {"sucesso": False, "msg": str(e)}

# --- INICIALIZAÇÃO BLINDADA ---
if __name__ == '__main__':
    api = ApiExportacao()
    # Passamos o app e a API juntos!
    webview.create_window("Painel de Gestão", app, width=1050, height=750, js_api=api)
    webview.start()