from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from conexao import conecta_db
from bd.simulacao import listar_simulacoes, consultar_simulacao_por_id, inserir_simulacao, atualizar_simulacao, deletar_simulacao

simulacao_bp = Blueprint("simulacao", __name__, url_prefix="/simulacoes")


@simulacao_bp.route("/", methods=["GET"])
@jwt_required()
def get_simulacoes():
    conexao = conecta_db()
    simulacoes = listar_simulacoes(conexao)
    return jsonify(simulacoes), 200


@simulacao_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_simulacao(id):
    conexao = conecta_db()
    simulacao = consultar_simulacao_por_id(conexao, id)
    if simulacao is None:
        return jsonify({"message": "Simulação não encontrada"}), 404
    return jsonify(simulacao), 200


@simulacao_bp.route("/", methods=["POST"])
@jwt_required()
def salvar_simulacao():
    conexao = conecta_db()
    dados = request.get_json()
    idUsuario = int(get_jwt_identity())  # vem do token, nunca do front
    valorParcela = inserir_simulacao(
        conexao,
        idUsuario,
        dados['tipoCredito'],
        dados['valorCredito'],
        dados['prazoMeses'],
        dados['taxaJuros'],
        dados['valorRenda'],
        dados['idBanco']
    )
    return jsonify({
        "message": "Simulação salva com sucesso!",
        "valorParcela": valorParcela
    }), 201


@simulacao_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def editar_simulacao(id):
    conexao = conecta_db()
    dados = request.get_json()
    valorParcela = atualizar_simulacao(
        conexao,
        id,
        dados['tipoCredito'],
        dados['valorCredito'],
        dados['prazoMeses'],
        dados['taxaJuros'],
        dados['valorRenda']
    )
    return jsonify({
        "message": "Simulação atualizada com sucesso!",
        "valorParcela": valorParcela
    }), 200


@simulacao_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def remover_simulacao(id):
    conexao = conecta_db()
    deletar_simulacao(conexao, id)
    return jsonify({"message": "Simulação deletada com sucesso!"}), 200