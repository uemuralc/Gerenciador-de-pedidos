import webview
from flask import Flask, render_template
import os
import csv

# Importando os nossos módulos modulares!
from database import iniciar_banco, obter_conexao
from auth import auth_bp
from rotas_pedidos import pedidos_bp
from rotas_estoque import estoque_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = "chave_super_secreta_painel_gestao_2026"

iniciar_banco()

# A MÁGICA DOS BLUEPRINTS: "Plugando" as rotas no aplicativo
app.register_blueprint(auth_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(estoque_bp)

@app.route('/')
def index():
    return render_template('index.html')

# --- CLASSE DE EXPORTAÇÃO (Mantida no app.py pois usa a janela ativa) ---
class ApiExportacao:
    def exportar_pedidos_nativ(self):
        janela_ativa = webview.windows[0]
        arquivo_salvar = janela_ativa.create_file_dialog(webview.SAVE_DIALOG, directory='', save_filename='relatorio_pedidos.csv', file_types=('Arquivos CSV (*.csv)', 'Todos os arquivos (*.*)'))
        if not arquivo_salvar: return {"sucesso": False, "msg": "Cancelado"}
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
        arquivo_salvar = janela_ativa.create_file_dialog(webview.SAVE_DIALOG, directory='', save_filename='relatorio_estoque.csv', file_types=('Arquivos CSV (*.csv)', 'Todos os arquivos (*.*)'))
        if not arquivo_salvar: return {"sucesso": False, "msg": "Cancelado"}
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

if __name__ == '__main__':
    api = ApiExportacao()
    webview.create_window("Painel de Gestão", app, width=1050, height=750, js_api=api)
    webview.start()