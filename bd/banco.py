from conexao import conecta_db
from menu import opcoes_menu_resumido

def menu_banco(titulo):
    opcoes_menu_resumido(titulo)
    while True: 
        opcao = input("Escolha uma opção:  ")
        conexao = conecta_db()
        if opcao == "1":
            listar_banco(conexao)
        elif opcao == "3":
            inserir_banco(conexao)
        elif opcao == "6":
            print("Sair")
            break
        else:
            print("Opção inválida, tente novamente")

def listar_banco(conexao):
    cursor = conexao.cursor()
    sql_listar = """select idBanco, nome, taxaBase, simulacao from banco          
                    order by id asc
                 """
    
    cursor.execute(sql_listar)
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for registro in registros:
        print(f"| ID: {registro[0]}  - Login: {registro[1]} - Admin: {registro[2]}  ")
    print("|----------------------------------------|")


def inserir_banco(conexao):
    print("Inserindo o Banco: ")
    cursor = conexao.cursor()

    nome = input("Nome do Banco: ")
    taxaBase = float(input("Taxa base para crédito: "))

    cursor.execute("insert into banco (nome, taxaBase) values (%s, %s)", (nome, taxaBase))
    conexao.commit()
    print("Banco inserido com sucesso!")

