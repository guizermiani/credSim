
from usuario import menu_usuario, login
from vendas import menu_vendas

from conexao import conecta_db

def menu_principal():
    print("|------------------------------------------|")
    print("|    Menu -> Programa                      |")
    print("|------------------------------------------|")
    print("|        1  -  Cliente                     |")
    print("|        2  -  Categoria                   |")
    print("|        3  -  Produto                     |")
    print("|        4  -  Usuário                     |")
    print("|        5  -  Vendas                      |")
    print("|        6  -  Sair do Sistema             |")
    print("|------------------------------------------|")

    while True: 
        opcao = input("Escolha uma opção:  ")

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_categoria("Categoria")
        elif opcao == "3":
            menu_produto("Produto")
        elif opcao == "4":
            menu_usuario("Usuario")
        elif opcao == "5":
            menu_vendas()
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
        