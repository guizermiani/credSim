from conexao import conecta_db
from menu import opcoes_menu_resumido

def menu_usuario(titulo):
    opcoes_menu_resumido(titulo)
    while True: 
        opcao = input("Escolha uma opção:  ")
        conexao = conecta_db()

        if opcao == "1":
            listar_usuario(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "2":
            listar_usuario(conexao)
            consultar_usuario_por_id(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "3":
            inserir_usuario(conexao)
            listar_usuario(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "4":
            listar_usuario(conexao)
            atualizar_usuario(conexao)
            listar_usuario(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "5":
            listar_usuario(conexao)
            deletar_usuario(conexao)
            listar_usuario(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "6":
            print("Sair")
            break
        else:
            print("Opção inválida, tente novamente")

def login(conexao) -> bool:
    print("-----------------------------------------")
    login = input("Digite o Login: ")
    senha = input("Digite a Senha: ")

    cursor = conexao.cursor()
    sql_listar = """select id, login, admin from usuario          
                    where login = %s and senha = %s
                 """
    dados = (login, senha)
    cursor.execute(sql_listar, dados)
    registro = cursor.fetchone()

    if registro is None:
        print("Usuário e Senha Inválidos")
        return False
    else:
        admin = registro[2]
        return True



def listar_usuario(conexao):
    cursor = conexao.cursor()
    sql_listar = """select id, login, admin from usuario          
                    order by id asc
                 """
    
    cursor.execute(sql_listar)
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for registro in registros:
        print(f"| ID: {registro[0]}  - Login: {registro[1]} - Admin: {registro[2]}  ")
    print("|----------------------------------------|")


def consultar_usuario_por_id(conexao):
    id = input("Digite o ID: ")
    cursor = conexao.cursor()
    cursor.execute("select id,login,admin, from usuario where id = " + id)
    registro = cursor.fetchone()

    if registro is None:
        print("Usuário não encontrado:")
    else:
        print(f"| ID        ..: {registro[0]} ")
        print(f"| Login       : {registro[1]} ")
        print(f"| Admin       : {registro[2]} ")
       

def inserir_usuario(conexao):
    print("Inserindo o Usuário ..: ")
    cursor = conexao.cursor()

    login = input("Login :")
    senha = input("Senha :")
    admin = input("Admin: ")

    sql_insert = "insert into usuario (login,senha,admin) values ( %s, %s, %s )"
    dados = (login,senha,admin)

    cursor.execute(sql_insert, dados)
    conexao.commit()

def atualizar_usuario(conexao):
    print("Alterando dados do Usuário")
    cursor = conexao.cursor()

    id    = input("Digite o ID : ")
    login = input("Login: ")
    senha = input("Senha: ")
    admin = input("Admin: ")

    sql_update = "update usuario set login = %s, senha = %s, admin = %s where id = %s"
    dados = (login,senha,admin,id)

    cursor.execute(sql_update,dados)
    conexao.commit()

def deletar_usuario(conexao):
    print("Deletando Usuário")
    cursor = conexao.cursor()
    id   = input("Digite o ID : ")
    sql_delete = "delete from usuario where id = "+ id
    cursor.execute(sql_delete)
    conexao.commit()