import sqlite3
import os

# Caminho absoluto para o banco dentro da pasta data
DB_PATH = os.path.join(os.path.dirname(__file__), "croche.db")

def criar_banco():
    """Cria as tabelas iniciais do banco de dados Crochê Manager."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Tabela de linhas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS linhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca TEXT,
            peso_novelo REAL NOT NULL
        )
    """)

    # Tabela de projetos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            linha_id INTEGER,
            cor_nome TEXT,
            cor_numero TEXT,
            qtd_novelos INTEGER NOT NULL,
            peso_novelo REAL NOT NULL,
            valor_novelo REAL NOT NULL,
            peso_restante REAL NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (linha_id) REFERENCES linhas (id)
        )
    """)

    # Tabela de agulhas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS agulhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tamanho REAL NOT NULL UNIQUE
        )
    """)

    # Tabela de receitas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('vídeo', 'imagem')) NOT NULL,
            caminho TEXT,
            observacoes TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"Banco criado com sucesso em: {DB_PATH}")

if __name__ == "__main__":
    criar_banco()
