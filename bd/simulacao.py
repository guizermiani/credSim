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
        select s.idSimulacao, s.tipoCredito, s.valorCredito, s.prazoMeses, s.taxaJuros,
               s.valorParcela, s.dataSimulacao, u.nome, b.nome
        from simulacao s
        inner join usuario u on s.idUsuario = u.idUsuario
        inner join banco b on s.idBanco = b.idBanco
        order by s.idSimulacao asc
    """)
    registros = cursor.fetchall()
    print("|----------------------------------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | Tipo: {r[1]} | Valor: R${r[2]:.2f} | Prazo: {r[3]}x | Juros: {r[4]}% | Parcela: R${r[5]:.2f} | Data: {r[6]} | Usuário: {r[7]} | Banco: {r[8]}")
    print("|----------------------------------------------------------------|")


def consultar_simulacao_por_id(conexao):
    id = input("Digite o ID da simulação: ")
    cursor = conexao.cursor()
    cursor.execute("""
        select s.idSimulacao, s.valorParcela, s.dataSimulacao, s.taxaJuros, s.valorRenda,
               s.valorCredito, s.tipoCredito, s.prazoMeses, u.nome, b.nome
        from simulacao s
        inner join usuario u on s.idUsuario = u.idUsuario
        inner join banco b on s.idBanco = b.idBanco
        where s.idSimulacao = %s
    """, (id,))
    r = cursor.fetchone()
    if r is None:
        print("Simulação não encontrada")
    else:
        print(f"| ID            : {r[0]}")
        print(f"| Tipo Crédito  : {r[6]}")
        print(f"| Banco         : {r[9]}")
        print(f"| Valor Crédito : R${r[5]:.2f}")
        print(f"| Prazo         : {r[7]} meses")
        print(f"| Taxa de Juros : {r[3]}%")
        print(f"| Valor Parcela : R${r[1]:.2f}")
        print(f"| Valor Renda   : R${r[4]:.2f}")
        print(f"| Data          : {r[2]}")
        print(f"| Usuário       : {r[8]}")


def inserir_simulacao(conexao):
    print("Inserindo Simulação: ")
    cursor = conexao.cursor()

    cursor.execute("select idUsuario, nome from usuario order by idUsuario asc")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
        return

    print("\nUsuários disponíveis:")
    for u in usuarios:
        print(f"  ID: {u[0]} | Nome: {u[1]}")
    idUsuario = int(input("\nID do Usuário: "))

    cursor.execute("select idBanco, nome, taxaPessoal, taxaConsignado, taxaImobiliario from banco order by idBanco asc")
    bancos = cursor.fetchall()
    if not bancos:
        print("Nenhum banco cadastrado. Cadastre um banco primeiro.")
        return

    print("\nBancos disponíveis:")
    for b in bancos:
        print(f"  ID: {b[0]} | Nome: {b[1]} | Pessoal: {b[2]}% | Consignado: {b[3]}% | Imobiliário: {b[4]}%")
    idBanco = int(input("\nID do Banco: "))

    cursor.execute("select taxaPessoal, taxaConsignado, taxaImobiliario from banco where idBanco = %s", (idBanco,))
    taxas = cursor.fetchone()

    print("\nTipo de Crédito:")
    print("  1 - Pessoal")
    print("  2 - Consignado")
    print("  3 - Imobiliário")
    opcao_tipo = input("Escolha: ")

    if opcao_tipo == "1":
        tipoCredito = "Pessoal"
        taxaJuros   = taxas[0]
    elif opcao_tipo == "2":
        tipoCredito = "Consignado"
        taxaJuros   = taxas[1]
    elif opcao_tipo == "3":
        tipoCredito = "Imobiliário"
        taxaJuros   = taxas[2]
    else:
        print("Tipo inválido.")
        return

    print(f"  Taxa de juros aplicada: {taxaJuros}%")

    valorCredito = float(input("Valor do Crédito: R$"))
    prazoMeses   = int(input("Prazo em meses: "))
    valorRenda   = float(input("Valor da Renda: R$"))

    taxa = taxaJuros / 100
    if taxa > 0:
        valorParcela = valorCredito * (taxa * (1 + taxa) ** prazoMeses) / ((1 + taxa) ** prazoMeses - 1)
    else:
        valorParcela = valorCredito / prazoMeses

    print(f"\n  Valor da Parcela calculado: R${valorParcela:.2f}")

    if valorParcela > valorRenda:
        print(f"  Simulação recusada: parcela R${valorParcela:.2f} ultrapassa a renda R${valorRenda:.2f}")
        return

    dataSimulacao = date.today()

    cursor.execute("""
        insert into simulacao (valorParcela, dataSimulacao, taxaJuros, valorRenda, valorCredito, tipoCredito, prazoMeses, idUsuario, idBanco)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (round(valorParcela, 2), dataSimulacao, taxaJuros, valorRenda, valorCredito, tipoCredito, prazoMeses, idUsuario, idBanco))
    conexao.commit()
    print("Simulação inserida com sucesso!")


def atualizar_simulacao(conexao):
    print("Alterando Simulação")
    cursor = conexao.cursor()

    id           = input("Digite o ID da simulação: ")
    valorCredito = float(input("Valor do Crédito: R$"))
    prazoMeses   = int(input("Prazo em meses: "))
    taxaJuros    = float(input("Taxa de Juros mensal (%): "))
    valorRenda   = float(input("Valor da Renda: R$"))

    taxa = taxaJuros / 100
    if taxa > 0:
        valorParcela = valorCredito * (taxa * (1 + taxa) ** prazoMeses) / ((1 + taxa) ** prazoMeses - 1)
    else:
        valorParcela = valorCredito / prazoMeses

    print(f"\n  Valor da Parcela calculado: R${valorParcela:.2f}")

    cursor.execute("""
        update simulacao
        set valorCredito=%s, prazoMeses=%s, taxaJuros=%s, valorRenda=%s, valorParcela=%s
        where idSimulacao=%s
    """, (valorCredito, prazoMeses, taxaJuros, valorRenda, round(valorParcela, 2), id))
    conexao.commit()
    print("Simulação atualizada com sucesso!")


def deletar_simulacao(conexao):
    print("Deletando Simulação")
    cursor = conexao.cursor()
    id = input("Digite o ID da simulação: ")
    cursor.execute("delete from simulacao where idSimulacao = %s", (id,))
    conexao.commit()
    print("Simulação deletada com sucesso!")