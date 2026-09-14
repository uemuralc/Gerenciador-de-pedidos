import os
from dotenv import load_dotenv
from flask import Flask, render_template

from database import iniciar_banco, obter_conexao
from auth import auth_bp
from rotas_pedidos import pedidos_bp
from rotas_estoque import estoque_bp

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = os.getenv("SECRET_KEY")

iniciar_banco()

app.register_blueprint(auth_bp)
app.register_blueprint(pedidos_bp)
app.register_blueprint(estoque_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # O servidor web vai definir a porta automaticamente aqui:
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta)