import sqlite3
import os

DB_PATH = os.path.join("data", "croche.db")


def remover_duplicatas(conn):
    """Remove entradas duplicadas na tabela `agulhas`, mantendo a menor id por tamanho."""
    cur = conn.cursor()
    # Deleta todas as linhas cujo id não é o mínimo para aquele tamanho
    cur.execute(
        """
        DELETE FROM agulhas
        WHERE id NOT IN (
            SELECT MIN(id) FROM agulhas GROUP BY tamanho
        )
        """
    )
    return cur.rowcount


def inserir_agulha():
    agulhas = [1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0]

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # garante que a tabela exista (se init_db não foi executado)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS agulhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tamanho REAL NOT NULL
        )
        """
    )

    # Remove duplicatas antigas (se houver)
    removed = remover_duplicatas(conn)

    inserted = 0
    for tamanho in agulhas:
        cur.execute("SELECT 1 FROM agulhas WHERE tamanho = ? LIMIT 1", (tamanho,))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO agulhas (tamanho) VALUES (?)", (tamanho,))
            inserted += 1

    conn.commit()
    conn.close()

    print(f"Duplicatas removidas: {removed}")
    print(f"Novas agulhas inseridas: {inserted}")


if __name__ == "__main__":
    conn = sqlite3.connect(r"data\croche.db")
    c = conn.cursor()
    c.execute("DELETE FROM agulhas WHERE tamanho = ?", (5.5,))
    conn.commit()
    conn.close()
    inserir_agulha()