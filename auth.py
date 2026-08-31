from flask import Blueprint, request, jsonify, session
from functools import wraps

# Criando o Blueprint de Autenticação
auth_bp = Blueprint('auth', __name__)
SENHA_SISTEMA = "1234"

def login_obrigatorio(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not session.get('logado'):
            return jsonify({"sucesso": False, "erro": "Acesso negado! Área restrita."}), 403
        return f(*args, **kwargs)
    return decorador

@auth_bp.route('/api/login', methods=['POST'])
def verificar_login():
    dados = request.json
    if dados.get('senha', '') == SENHA_SISTEMA:
        session['logado'] = True 
        return jsonify({"sucesso": True, "mensagem": "Acesso liberado!"}), 200
    
    return jsonify({"sucesso": False, "erro": "Senha incorreta!"}), 401