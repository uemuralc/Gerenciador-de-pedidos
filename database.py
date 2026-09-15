import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def obter_conexao():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def iniciar_banco():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    # Cria a tabela com a nova estrutura
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id BIGINT PRIMARY KEY,
            cliente VARCHAR(100),
            contato VARCHAR(50),
            item TEXT,
            material_origem VARCHAR(100),
            status VARCHAR(20),
            documento_url TEXT
        )
    ''')
    
    # Migração automática para atualizar o banco antigo sem quebrar o sistema
    try:
        conexao.autocommit = True
        cursor.execute('ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS contato VARCHAR(50);')
        cursor.execute('ALTER TABLE pedidos ADD COLUMN IF NOT EXISTS material_origem VARCHAR(100);')
        cursor.execute('ALTER TABLE pedidos DROP COLUMN IF EXISTS total;')
    except Exception as e:
        print("Aviso na migração: ", e)
    
    # Criação da tabela de estoque (mantida igual)
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