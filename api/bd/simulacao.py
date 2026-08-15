from conexao import conecta_db
from datetime import date


def listar_simulacoes(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        select s.idSimulacao, s.tipoCredito, s.valorCredito, s.prazoMeses, s.taxaJuros,
               s.valorRenda, s.valorParcela, s.dataSimulacao, s.idUsuario, s.idBanco, b.nome
        from simulacao s
        left join banco b on b.idBanco = s.idBanco
        order by s.idSimulacao asc
    """)
    registros = cursor.fetchall()
    resultado = []
    for r in registros:
        resultado.append({
            "idSimulacao":   r[0],
            "tipoCredito":   r[1],
            "valorCredito":  float(r[2]),
            "prazoMeses":    r[3],
            "taxaJuros":     float(r[4]),
            "valorRenda":    float(r[5]) if r[5] is not None else None,
            "valorParcela":  float(r[6]),
            "dataSimulacao": str(r[7]),
            "idUsuario":     r[8],
            "idBanco":       r[9],
            "nomeBanco":     r[10]
        })
    return resultado


def consultar_simulacao_por_id(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("""
        select s.idSimulacao, s.tipoCredito, s.valorCredito, s.prazoMeses, s.taxaJuros,
               s.valorRenda, s.valorParcela, s.dataSimulacao, s.idUsuario, s.idBanco, b.nome
        from simulacao s
        left join banco b on b.idBanco = s.idBanco
        where s.idSimulacao = %s
    """, (id,))
    r = cursor.fetchone()
    if r is None:
        return None
    return {
        "idSimulacao":   r[0],
        "tipoCredito":   r[1],
        "valorCredito":  float(r[2]),
        "prazoMeses":    r[3],
        "taxaJuros":     float(r[4]),
        "valorRenda":    float(r[5]) if r[5] is not None else None,
        "valorParcela":  float(r[6]),
        "dataSimulacao": str(r[7]),
        "idUsuario":     r[8],
        "idBanco":       r[9],
        "nomeBanco":     r[10]
    }


def calcular_parcela(valorCredito, prazoMeses, taxaJuros):
    valorCredito = float(valorCredito)
    prazoMeses = int(prazoMeses)
    taxaJuros = float(taxaJuros)

    if prazoMeses <= 0:
        raise ValueError("prazoMeses deve ser maior que zero")

    if taxaJuros > 0:
        taxa = taxaJuros / 100
        parcela = valorCredito * (taxa * (1 + taxa) ** prazoMeses) / ((1 + taxa) ** prazoMeses - 1)
    else:
        parcela = valorCredito / prazoMeses
    return round(parcela, 2)


def inserir_simulacao(conexao, idUsuario, tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda, idBanco):
    valorCredito = float(valorCredito)
    prazoMeses = int(prazoMeses)
    taxaJuros = float(taxaJuros)
    valorRenda = float(valorRenda)

    valorParcela  = calcular_parcela(valorCredito, prazoMeses, taxaJuros)
    dataSimulacao = date.today()
    cursor = conexao.cursor()
    cursor.execute("""
        insert into simulacao (tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda, valorParcela, dataSimulacao, idUsuario, idBanco)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda, valorParcela, dataSimulacao, idUsuario, idBanco))
    conexao.commit()
    return valorParcela


def atualizar_simulacao(conexao, id, tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda):
    valorCredito = float(valorCredito)
    prazoMeses = int(prazoMeses)
    taxaJuros = float(taxaJuros)
    valorRenda = float(valorRenda)

    valorParcela = calcular_parcela(valorCredito, prazoMeses, taxaJuros)
    cursor = conexao.cursor()
    cursor.execute("""
        update simulacao
        set tipoCredito=%s, valorCredito=%s, prazoMeses=%s, taxaJuros=%s, valorRenda=%s, valorParcela=%s
        where idSimulacao=%s
    """, (tipoCredito, valorCredito, prazoMeses, taxaJuros, valorRenda, valorParcela, id))
    conexao.commit()
    return valorParcela


def deletar_simulacao(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("delete from simulacao where idSimulacao = %s", (id,))
    conexao.commit()