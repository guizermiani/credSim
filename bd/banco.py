from conexao import conecta_db
from menu import opcoes_menu_resumido

def menu_banco(titulo):
    opcoes_menu_resumido(titulo)
    while True:
        opcao = input("Escolha uma opção: ")
        conexao = conecta_db()
        if opcao == "1":
            listar_banco(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "2":
            consultar_banco_por_id(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "3":
            inserir_banco(conexao)
            listar_banco(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "4":
            atualizar_banco(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "5":
            deletar_banco(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "6":
            print("Sair")
            break
        else:
            print("Opção inválida, tente novamente")


def listar_banco(conexao):
    cursor = conexao.cursor()
    cursor.execute("select idBanco, nome, taxaPessoal, taxaConsignado, taxaImobiliario from banco order by idBanco asc")
    registros = cursor.fetchall()
    print("|----------------------------------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | Nome: {r[1]} | Pessoal: {r[2]}% | Consignado: {r[3]}% | Imobiliário: {r[4]}%")
    print("|----------------------------------------------------------------|")


def consultar_banco_por_id(conexao):
    id = input("Digite o ID: ")
    cursor = conexao.cursor()
    cursor.execute("select idBanco, nome, taxaPessoal, taxaConsignado, taxaImobiliario from banco where idBanco = %s", (id,))
    r = cursor.fetchone()
    if r is None:
        print("Banco não encontrado")
    else:
        print(f"| ID               : {r[0]}")
        print(f"| Nome             : {r[1]}")
        print(f"| Taxa Pessoal     : {r[2]}%")
        print(f"| Taxa Consignado  : {r[3]}%")
        print(f"| Taxa Imobiliário : {r[4]}%")


def inserir_banco(conexao):
    print("Inserindo o Banco: ")
    cursor = conexao.cursor()

    nome            = input("Nome do Banco: ")
    taxaPessoal     = float(input("Taxa para Crédito Pessoal (%): "))
    taxaConsignado  = float(input("Taxa para Crédito Consignado (%): "))
    taxaImobiliario = float(input("Taxa para Crédito Imobiliário (%): "))

    cursor.execute(
        "insert into banco (nome, taxaPessoal, taxaConsignado, taxaImobiliario) values (%s, %s, %s, %s)",
        (nome, taxaPessoal, taxaConsignado, taxaImobiliario)
    )
    conexao.commit()
    print("Banco inserido com sucesso!")


def atualizar_banco(conexao):
    print("Alterando dados do Banco")
    cursor = conexao.cursor()

    id              = input("Digite o ID: ")
    nome            = input("Nome: ")
    taxaPessoal     = float(input("Taxa para Crédito Pessoal (%): "))
    taxaConsignado  = float(input("Taxa para Crédito Consignado (%): "))
    taxaImobiliario = float(input("Taxa para Crédito Imobiliário (%): "))

    cursor.execute(
        "update banco set nome=%s, taxaPessoal=%s, taxaConsignado=%s, taxaImobiliario=%s where idBanco=%s",
        (nome, taxaPessoal, taxaConsignado, taxaImobiliario, id)
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