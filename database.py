import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = "postgresql://neondb_owner:npg_Bsgiv6Ynxjb8@ep-red-leaf-a5wbvtme-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def obter_conexao():
    # RealDictCursor faz o Postgres retornar as informações em formato de dicionário para o JSON
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