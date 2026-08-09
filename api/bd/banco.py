from api.conexao import conecta_db

def listar_banco(conexao):
    cursor = conexao.cursor()
    cursor.execute("select idBanco, nome, taxaBase from banco order by idBanco asc")
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | Nome: {r[1]} | Taxa Base: {r[2]}")
    print("|----------------------------------------|")


def consultar_banco_por_id(conexao):
    id = input("Digite o ID: ")
    cursor = conexao.cursor()
    cursor.execute("select idBanco, nome, taxaBase from banco where idBanco = %s", (id,))
    registro = cursor.fetchone()
    if registro is None:
        print("Banco não encontrado")
    else:
        print(f"| ID        : {registro[0]}")
        print(f"| Nome      : {registro[1]}")
        print(f"| Taxa Base : {registro[2]}")


def inserir_banco(conexao):
    print("Inserindo o Banco: ")
    cursor = conexao.cursor()

    nome     = input("Nome do Banco: ")
    taxaBase = float(input("Taxa base para crédito: "))

    cursor.execute("insert into banco (nome, taxaBase) values (%s, %s)", (nome, taxaBase))
    conexao.commit()
    print("Banco inserido com sucesso!")


def atualizar_banco(conexao):
    print("Alterando dados do Banco")
    cursor = conexao.cursor()

    id = input("Digite o ID: ")
    nome = input("Nome: ")
    taxaBase = float(input("Taxa base: "))

    cursor.execute(
        "update banco set nome=%s, taxaBase=%s where idBanco=%s",
        (nome, taxaBase, id)
    )
    conexao.commit()
    print("Banco atualizado com sucesso!")


def deletar_banco(conexao):
    print("Deletando Banco")
    cursor = conexao.cursor()
    id = input("Digite o ID: ")
    cursor.execute("delete from banco where idBanco = %s", (id,))
    conexao.commit()
    print("Banco deletado com sucesso!")