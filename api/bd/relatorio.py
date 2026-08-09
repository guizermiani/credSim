from api.conexao import conecta_db
from simulacao import listar_simulacao, consultar_simulacao_por_id, inserir_simulacao, atualizar_simulacao, deletar_simulacao

def gerar_relatorio_simulacoes(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
            select s.idSimulacao, s.tipoCredito, s.valorCredito, s.prazoMeses, u.nome
            from simulacao s
            inner join usuario u on s.idUsuario = u.idUsuario
            order by s.idSimulacao asc
     """)
    registros = cursor.fetchall()
    print("|----------------------------------------|")
    for r in registros:
        print(f"| ID: {r[0]} | Tipo: {r[1]} | Valor: R${r[2]:.2f} | Prazo: {r[3]}x | Usuário: {r[4]}")
    print("|----------------------------------------|")
