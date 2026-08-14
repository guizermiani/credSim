from flask import jsonify, request, Blueprint
from conexao import conecta_db
from bd.banco import listar_bancos, consultar_banco_por_id, inserir_banco, atualizar_banco, deletar_banco

banco_bp = Blueprint("banco", __name__, url_prefix="/bancos")


@banco_bp.route("/", methods=["GET"])
def get_bancos():
    conexao = conecta_db()
    bancos = listar_bancos(conexao)
    return jsonify(bancos), 200


@banco_bp.route("/<int:id>", methods=["GET"])
def get_banco(id):
    conexao = conecta_db()
    banco = consultar_banco_por_id(conexao, id)
    if banco is None:
        return jsonify({"message": "Banco não encontrado"}), 404
    return jsonify(banco), 200


@banco_bp.route("/", methods=["POST"])
def salvar_banco():
    conexao = conecta_db()
    dados = request.get_json()
    inserir_banco(conexao, dados['nome'], dados['taxaPessoal'], dados['taxaConsignado'], dados['taxaImobiliario'])
    return jsonify({"message": "Banco salvo com sucesso!"}), 201


@banco_bp.route("/<int:id>", methods=["PUT"])
def editar_banco(id):
    conexao = conecta_db()
    dados = request.get_json()
    atualizar_banco(conexao, id, dados['nome'], dados['taxaPessoal'], dados['taxaConsignado'], dados['taxaImobiliario'])
    return jsonify({"message": "Banco atualizado com sucesso!"}), 200


@banco_bp.route("/<int:id>", methods=["DELETE"])
def remover_banco(id):
    conexao = conecta_db()
    deletar_banco(conexao, id)
    return jsonify({"message": "Banco deletado com sucesso!"}), 200