from usuario import menu_usuario, login
from banco import menu_banco
from simulacao import menu_simulacao
from conexao import conecta_db

def menu_principal():
    print("|------------------------------------------|")
    print("|    Menu -> Programa                      |")
    print("|------------------------------------------|")
    print("|        1  -  Usuário                     |")
    print("|        2  -  Banco                       |")
    print("|        3  -  Simulação                   |")
    print("|        6  -  Sair do Sistema             |")
    print("|------------------------------------------|")

    while True:
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_usuario()
        elif opcao == "2":
            menu_banco("Banco")
        elif opcao == "3":
            menu_simulacao("Simulação")
        elif opcao == "6":
            print("Sair do sistema")
            break
        else:
            print("Opção inválida, tente novamente")


if __name__ == "__main__":
    conexao = conecta_db()
    while True:
        resultado = login(conexao)
        if resultado is True:
            menu_principal()