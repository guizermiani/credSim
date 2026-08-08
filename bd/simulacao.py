from conexao import conecta_db
from menu import opcoes_menu_resumido
from datetime import date

def menu_simulacao(titulo):
    opcoes_menu_resumido(titulo)
    while True:
        opcao = input("Escolha uma opção: ")
        conexao = conecta_db()
        if opcao == "1":
            listar_simulacao(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "2":
            consultar_simulacao_por_id(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "3":
            inserir_simulacao(conexao)
            listar_simulacao(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "4":
            atualizar_simulacao(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "5":
            deletar_simulacao(conexao)
            opcoes_menu_resumido(titulo)
        elif opcao == "6":
            print("Sair")
            break
        else:
            print("Opção inválida, tente novamente")


def listar_simulacao(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        select idSimulacao, tipoCredito, valorCredito, prazoMeses, taxaJuros, valorParcela, dataSimulacao, idUsuario
        from simulacao
        order by idSimulacao asc
    """)
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | Tipo: {r[1]} | Valor: R${r[2]:.2f} | Prazo: {r[3]}x | Juros: {r[4]}% | Parcela: R${r[5]:.2f} | Data: {r[6]} | Usuário: {r[7]}")
    print("|----------------------------------------|")


def consultar_simulacao_por_id(conexao):
    id = input("Digite o ID da simulação: ")
    cursor = conexao.cursor()
    cursor.execute("""
        select idSimulacao, valorParcela, dataSimulacao, taxaJuros, valorRenda, valorCredito, tipoCredito, prazoMeses, idUsuario
        from simulacao where idSimulacao = %s
    """, (id,))
    r = cursor.fetchone()
    if r is None:
        print("Simulação não encontrada")
    else:
        print(f"| ID            : {r[0]}")
        print(f"| Tipo Crédito  : {r[6]}")
        print(f"| Valor Crédito : R${r[5]:.2f}")
        print(f"| Prazo         : {r[7]} meses")
        print(f"| Taxa de Juros : {r[3]}%")
        print(f"| Valor Parcela : R${r[1]:.2f}")
        print(f"| Valor Renda   : R${r[4]:.2f}")
        print(f"| Data          : {r[2]}")
        print(f"| ID Usuário    : {r[8]}")


def inserir_simulacao(conexao):
    print("Inserindo Simulação: ")
    cursor = conexao.cursor()

    # lista usuários disponíveis
    cursor.execute("select idUsuario, nome, rendaMensal from usuario order by idUsuario asc")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
        return

    print("\nUsuários disponíveis:")
    for u in usuarios:
        print(f"  ID: {u[0]} | Nome: {u[1]} | Renda: R${u[2]:.2f}")

    idUsuario    = int(input("\nID do Usuário: "))
    tipoCredito  = input("Tipo de Crédito (ex: Pessoal, Consignado, Imobiliário): ")
    valorCredito = float(input("Valor do Crédito: R$"))
    prazoMeses   = int(input("Prazo em meses: "))
    taxaJuros    = float(input("Taxa de Juros mensal (%): "))
    valorRenda   = float(input("Valor da Renda: R$"))

    # calcula parcela com juros compostos
    if taxaJuros > 0:
        taxa = taxaJuros / 100
        valorParcela = valorCredito * (taxa * (1 + taxa) ** prazoMeses) / ((1 + taxa) ** prazoMeses - 1)
    else:
        valorParcela = valorCredito / prazoMeses

    dataSimulacao = date.today()

    print(f"\n  Valor da Parcela calculado: R${valorParcela:.2f}")

    cursor.execute("""
        insert into simulacao (valorParcela, dataSimulacao, taxaJuros, valorRenda, valorCredito, tipoCredito, prazoMeses, idUsuario)
        values (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (round(valorParcela, 2), dataSimulacao, taxaJuros, valorRenda, valorCredito, tipoCredito, prazoMeses, idUsuario))
    conexao.commit()
    print("Simulação inserida com sucesso!")


def atualizar_simulacao(conexao):
    print("Alterando Simulação")
    cursor = conexao.cursor()

    id           = input("Digite o ID da simulação: ")
    tipoCredito  = input("Tipo de Crédito: ")
    valorCredito = float(input("Valor do Crédito: R$"))
    prazoMeses   = int(input("Prazo em meses: "))
    taxaJuros    = float(input("Taxa de Juros mensal (%): "))
    valorRenda   = float(input("Valor da Renda: R$"))

    if taxaJuros > 0:
        taxa = taxaJuros / 100
        valorParcela = valorCredito * (taxa * (1 + taxa) ** prazoMeses) / ((1 + taxa) ** prazoMeses - 1)
    else:
        valorParcela = valorCredito / prazoMeses

    print(f"\n  Valor da Parcela calculado: R${valorParcela:.2f}")

    cursor.execute("""
        update simulacao
        set tipoCredito=%s, valorCredito=%s, prazoMeses=%s, taxaJuros=%s, valorRenda=%s, valorParcela=%s
        where idSimulacao=%s
    """, (tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda, round(valorParcela, 2), id))
    conexao.commit()
    print("Simulação atualizada com sucesso!")


def deletar_simulacao(conexao):
    print("Deletando Simulação")
    cursor = conexao.cursor()
    id = input("Digite o ID da simulação: ")
    cursor.execute("delete from simulacao where idSimulacao = %s", (id,))
    conexao.commit()
    print("Simulação deletada com sucesso!")