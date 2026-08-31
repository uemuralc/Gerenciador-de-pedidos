import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env local
load_dotenv()

# Puxa a URL de forma segura
DB_URL = os.getenv("DATABASE_URL")

def obter_conexao():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def iniciar_banco():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    # Criação da tabela com colunas idênticas às usadas nas rotas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id BIGINT PRIMARY KEY,
            cliente VARCHAR(100),
            item TEXT,
            status VARCHAR(20),
            total REAL
        )
    ''')
    
    # Criação da tabela de estoque
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id BIGINT PRIMARY KEY,
            nome VARCHAR(100),
            quantidade REAL,
            unidade VARCHAR(20)
        )
    ''')
    
    conexao.commit()
    cursor.close()
    conexao.close()