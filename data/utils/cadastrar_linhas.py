import sqlite3
import os

DB_PATH = os.path.join("data", "croche.db")


def conectar_e_preparar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, isolation_level=None)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS linhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            marca TEXT,
            peso_novelo REAL NOT NULL
        )
        """
    )
    # garante índice único em nome para evitar duplicatas futuras
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_linhas_nome_unique ON linhas (nome)")
    # tabela de marcas (opcional) para facilitar seleção de marcas comuns
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
        """
    )
    # garante que a marca 'Círculo' exista (marca usada com frequência)
    cur.execute("INSERT OR IGNORE INTO marcas (nome) VALUES (?)", ("Círculo",))
    conn.commit()
    return conn


def remover_duplicatas(conn):
    """Remove entradas duplicadas na tabela `linhas`, mantendo a menor id por nome."""
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM linhas
        WHERE id NOT IN (
            SELECT MIN(id) FROM linhas GROUP BY nome
        )
        """
    )
    removed = cur.rowcount
    conn.commit()
    return removed


def listar_linhas(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, nome, marca, peso_novelo FROM linhas ORDER BY nome")
    return cur.fetchall()


def listar_marcas(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM marcas ORDER BY nome")
    return cur.fetchall()


def adicionar_marca(conn, nome):
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO marcas (nome) VALUES (?)", (nome,))
        conn.commit()
        return True
    except Exception:
        return False


def deletar_marca(conn, id_or_nome):
    cur = conn.cursor()
    if isinstance(id_or_nome, int):
        cur.execute("DELETE FROM marcas WHERE id = ?", (id_or_nome,))
    else:
        cur.execute("DELETE FROM marcas WHERE nome = ?", (id_or_nome,))
    cnt = cur.rowcount
    conn.commit()
    return cnt


def inserir_linha(conn, nome, marca, peso):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM linhas WHERE nome = ? LIMIT 1", (nome,))
    if cur.fetchone() is not None:
        return False
    cur.execute("INSERT INTO linhas (nome, marca, peso_novelo) VALUES (?, ?, ?)", (nome, marca, peso))
    conn.commit()
    return True


def deletar_linha_por_id(conn, id_):
    cur = conn.cursor()
    cur.execute("DELETE FROM linhas WHERE id = ?", (id_,))
    conn.commit()
    return cur.rowcount


def deletar_linha_por_nome(conn, nome):
    cur = conn.cursor()
    cur.execute("DELETE FROM linhas WHERE nome = ?", (nome,))
    conn.commit()
    return cur.rowcount


def prompt_float(prompt, default=None):
    while True:
        val = input(f"{prompt}" + (f" [{default}]" if default is not None else "") + ": ")
        if val == "" and default is not None:
            return default
        try:
            return float(val)
        except ValueError:
            print("Valor inválido. Digite um número (ex: 50.0).")


def main():
    conn = conectar_e_preparar()
    removed = remover_duplicatas(conn)
    if removed:
        print(f"Removidas {removed} duplicatas existentes.")

    menu = """
Escolha uma opção:
1) Listar linhas
2) Cadastrar nova linha
3) Deletar linha por id
4) Deletar linha por nome
5) Inserir sample (bulk)
6) Sair
7) Gerenciar marcas

"""

    while True:
        print(menu)
        opc = input("Opção: ").strip()
        if opc == "1":
            rows = listar_linhas(conn)
            if not rows:
                print("Nenhuma linha cadastrada.")
            else:
                for r in rows:
                    print(f"{r[0]} | {r[1]} | {r[2] or ''} | {r[3]}g")


        elif opc == "2":
            nome = input("Nome da linha: ").strip()
            if not nome:
                print("Nome não pode ser vazio.")
                continue
            # Seleção de marca rápida: mostra marcas existentes e opção Círculo como padrão
            marcas = listar_marcas(conn)
            print("Escolha uma marca:")
            print("0) Digitar outra marca")
            for m in marcas:
                print(f"{m[0]}) {m[1]}")
            escolha = input("Marca (id, 0 para digitar): ").strip()
            if escolha == "0" or escolha == "":
                marca = input("Marca (digite ou deixe vazio): ").strip() or None
            else:
                try:
                    mid = int(escolha)
                    marca = next((m[1] for m in marcas if m[0] == mid), None)
                except ValueError:
                    marca = None
            peso = prompt_float("Peso do novelo (g)")
            ok = inserir_linha(conn, nome, marca, peso)
            if ok:
                print("Linha cadastrada com sucesso.")
            else:
                print("Já existe uma linha com esse nome. Cadastro ignorado.")
        elif opc == "3":
            try:
                id_ = int(input("ID da linha a deletar: ").strip())
            except ValueError:
                print("ID inválido.")
                continue
            cnt = deletar_linha_por_id(conn, id_)
            print(f"Removidos: {cnt}")
        elif opc == "4":
            nome = input("Nome da linha a deletar: ").strip()
            if not nome:
                print("Nome não pode ser vazio.")
                continue
            cnt = deletar_linha_por_nome(conn, nome)
            print(f"Removidos: {cnt}")
        elif opc == "5":
            sample = []
            print("Digite linhas no formato: nome,marca,peso (vazio para terminar)")
            while True:
                line = input("Linha: ").strip()
                if not line:
                    break
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 3:
                    print("Formato inválido. Use: nome,marca,peso")
                    continue
                try:
                    peso = float(parts[2])
                except ValueError:
                    print("Peso inválido. Use número como 50.0")
                    continue
                sample.append((parts[0], parts[1] or None, peso))
            for nome, marca, peso in sample:
                ok = inserir_linha(conn, nome, marca, peso)
                if ok:
                    print(f"Inserida: {nome}")
                else:
                    print(f"Ignorado (já existe): {nome}")
        elif opc == "6":
            print("Saindo...")
            break
        elif opc == "7":
            # Gerenciamento simples de marcas
            while True:
                print("\nGerenciar marcas:\n1) Listar marcas\n2) Adicionar marca\n3) Deletar marca\n4) Voltar")
                sub = input("Opção: ").strip()
                if sub == "1":
                    m = listar_marcas(conn)
                    if not m:
                        print("Nenhuma marca cadastrada.")
                    else:
                        for it in m:
                            print(f"{it[0]} | {it[1]}")
                elif sub == "2":
                    nome_m = input("Nome da marca: ").strip()
                    if not nome_m:
                        print("Nome não pode ser vazio.")
                        continue
                    ok = adicionar_marca(conn, nome_m)
                    print("Marca adicionada." if ok else "Falha ao adicionar (já existe?).")
                elif sub == "3":
                    chave = input("Digite id ou nome da marca para deletar: ").strip()
                    if not chave:
                        print("Entrada vazia.")
                        continue
                    try:
                        chave_int = int(chave)
                        cnt = deletar_marca(conn, chave_int)
                    except ValueError:
                        cnt = deletar_marca(conn, chave)
                    print(f"Removidas: {cnt}")
                elif sub == "4":
                    break
                else:
                    print("Opção inválida.")
        else:
            print("Opção inválida.")

    conn.close()


if __name__ == "__main__":
    main()