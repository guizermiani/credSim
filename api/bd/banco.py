from conexao import conecta_db


def listar_bancos(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
        select idBanco, nome, taxaPessoal, taxaConsignado, taxaImobiliario
        from banco
        order by idBanco asc
    """)
    registros = cursor.fetchall()
    resultado = []
    for r in registros:
        resultado.append({
            "idBanco":         r[0],
            "nome":            r[1],
            "taxaPessoal":     r[2],
            "taxaConsignado":  r[3],
            "taxaImobiliario": r[4]
        })
    return resultado


def consultar_banco_por_id(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("""
        select idBanco, nome, taxaPessoal, taxaConsignado, taxaImobiliario
        from banco
        where idBanco = %s
    """, (id,))
    r = cursor.fetchone()
    if r is None:
        return None
    return {
        "idBanco":         r[0],
        "nome":            r[1],
        "taxaPessoal":     r[2],
        "taxaConsignado":  r[3],
        "taxaImobiliario": r[4]
    }


def inserir_banco(conexao, nome, taxaPessoal, taxaConsignado, taxaImobiliario):
    cursor = conexao.cursor()
    cursor.execute("""
        insert into banco (nome, taxaPessoal, taxaConsignado, taxaImobiliario)
        values (%s, %s, %s, %s)
    """, (nome, taxaPessoal, taxaConsignado, taxaImobiliario))
    conexao.commit()


def atualizar_banco(conexao, id, nome, taxaPessoal, taxaConsignado, taxaImobiliario):
    cursor = conexao.cursor()
    cursor.execute("""
        update banco
        set nome=%s, taxaPessoal=%s, taxaConsignado=%s, taxaImobiliario=%s
        where idBanco=%s
    """, (nome, taxaPessoal, taxaConsignado, taxaImobiliario, id))
    conexao.commit()


def deletar_banco(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("delete from banco where idBanco = %s", (id,))
    conexao.commit()