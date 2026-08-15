from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token
from conexao import conecta_db
from bd.usuario import listar_usuario_bd, inserir_usuario_bd, atualizar_usuario_bd, deletar_usuario_bd, consultar_usuario_por_id_bd, login_bd

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")

@usuario_bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuario():
    conexao = conecta_db()
    return jsonify(listar_usuario_bd(conexao))

@usuario_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def consultar_usuario(id):
    conexao = conecta_db()
    usuario = consultar_usuario_por_id_bd(conexao, id)
    if usuario is None:
        return jsonify({"message": "Usuário não encontrado"}), 404
    return jsonify(usuario)



@usuario_bp.route("/", methods=["POST"])
def salvar_usuario():
    conexao = conecta_db()
    dados = request.get_json()
    inserir_usuario_bd(conexao, dados['cpf'], dados['nome'], dados['email'], dados['senha'])
    return jsonify({"message": "Usuário salvo com sucesso!"}), 201




@usuario_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(id):
    conexao = conecta_db()
    dados = request.get_json()
    atualizar_usuario_bd(conexao, id, dados['nome'], dados['email'], dados['senha'])
    return jsonify({"message": "Usuário atualizado com sucesso!"})




@usuario_bp.route("/xxx", methods=["DELETE"])
@jwt_required()
def deletar_usuario(id):
    conexao = conecta_db()
    deletar_usuario_bd(conexao, id)
    return jsonify({"message": "Usuário deletado com sucesso!"})




@usuario_bp.route("/login", methods=["POST"])
def login_usuario():
    conexao = conecta_db()
    dados = request.get_json()
    registro = login_bd(conexao, dados['cpf'], dados['senha'])
    if registro is None:
        return jsonify({"message": "CPF ou senha inválidos"}), 401
    token = create_access_token(identity=str(registro[0]))
    return jsonify({"token": token, "nome": registro[1]})