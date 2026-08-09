def login_bd(conexao, cpf, senha):
    cursor = conexao.cursor()
    cursor.execute(
        "select idUsuario, nome from usuario where cpf = %s and senha = %s",
        (cpf, senha)
    )
    return cursor.fetchone()

def listar_usuario_bd(conexao):
    cursor = conexao.cursor()
    cursor.execute("select idUsuario, cpf, nome, email from usuario order by idUsuario asc")
    registros = cursor.fetchall()
    return [{"idUsuario": r[0], "cpf": r[1], "nome": r[2], "email": r[3]} for r in registros]

def consultar_usuario_por_id_bd(conexao, id):
    cursor = conexao.cursor()
    cursor.execute(
        "select idUsuario, cpf, nome, email from usuario where idUsuario = %s", (id,)
    )
    r = cursor.fetchone()
    if r is None:
        return None
    return {"idUsuario": r[0], "cpf": r[1], "nome": r[2], "email": r[3]}

def inserir_usuario_bd(conexao, cpf, nome, email, senha):
    cursor = conexao.cursor()
    cursor.execute(
        "insert into usuario (cpf, nome, email, senha) values (%s, %s, %s, %s)",
        (cpf, nome, email, senha)
    )
    conexao.commit()

def atualizar_usuario_bd(conexao, id, nome, email, senha):
    cursor = conexao.cursor()
    cursor.execute(
        "update usuario set nome=%s, email=%s, senha=%s where idUsuario=%s",
        (nome, email, senha, id)
    )
    conexao.commit()

def deletar_usuario_bd(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("delete from usuario where idUsuario = %s", (id,))
    conexao.commit()