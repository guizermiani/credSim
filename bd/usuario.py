from conexao import conecta_db
from menu import opcoes_menu_resumido

def menu_usuario():
    opcoes_menu_resumido("Usuário")
    while True:
        opcao = input("Escolha uma opção: ")
        conexao = conecta_db()

        if opcao == "1":
            listar_usuario(conexao)
            opcoes_menu_resumido("Usuário")
        elif opcao == "3":
            inserir_usuario(conexao)
            listar_usuario(conexao)
            opcoes_menu_resumido("Usuário")
        elif opcao == "6":
            print("Sair")
            break
        else:
            print("Opção inválida, tente novamente")

def login(conexao) -> bool:
    print("-----------------------------------------")
    cpf = input("Digite o CPF: ")
    senha = input("Digite a Senha: ")

    cursor = conexao.cursor()
    cursor.execute(
        "select idUsuario, nome from usuario where cpf = %s and senha = %s",
        (cpf, senha)
    )
    registro = cursor.fetchone()

    if registro is None:
        print("CPF ou Senha inválidos")
        return False
    else:
        print(f"Bem-vindo, {registro[1]}!")
        return True

def listar_usuario(conexao):
    cursor = conexao.cursor()
    cursor.execute("select idUsuario, cpf, nome, email from usuario order by idUsuario asc")
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | CPF: {r[1]} | Nome: {r[2]} | E-mail: {r[3]}")
    print("|----------------------------------------|")

def consultar_usuario_por_id(conexao):
    id = input("Digite o ID: ")
    cursor = conexao.cursor()
    cursor.execute(
        "select idUsuario, cpf, nome, email, senha from usuario where idUsuario = %s",
        (id,)
    )
    registro = cursor.fetchone()

    if registro is None:
        print("Usuário não encontrado")
    else:
        print(f"| ID          : {registro[0]}")
        print(f"| CPF         : {registro[1]}")
        print(f"| Nome        : {registro[2]}")
        print(f"| E-mail      : {registro[3]}")
        print(f"| Senha       : {registro[4]}")

def inserir_usuario(conexao):
    print("Inserindo o Usuário: ")
    cursor = conexao.cursor()

    cpf = input("CPF: ")
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    cursor.execute(
        "insert into usuario (cpf, nome, email, senha) values (%s, %s, %s, %s)",
        (cpf, nome, email, senha)
    )
    conexao.commit()
    print("Usuário inserido com sucesso!")

def atualizar_usuario(conexao):
    print("Alterando dados do Usuário")
    cursor = conexao.cursor()

    id = input("Digite o ID: ")
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    cursor.execute(
        "update usuario set nome=%s, email=%s, senha=%s where idUsuario=%s",
        (nome, email, senha, id)
    )
    conexao.commit()
    print("Usuário atualizado com sucesso!")

def deletar_usuario(conexao):
    print("Deletando Usuário")
    cursor = conexao.cursor()
    id = input("Digite o ID: ")
    cursor.execute("delete from usuario where idUsuario = %s", (id,))
    conexao.commit()
    print("Usuário deletado com sucesso!")