import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'banco_de_dados.db')

def iniciar_banco():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY, cliente TEXT NOT NULL, item TEXT, status TEXT NOT NULL, total REAL NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS estoque (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, quantidade REAL NOT NULL, unidade TEXT NOT NULL)''')
        conn.commit()

def obter_conexao():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn