from flask import Blueprint, request, current_app

# from quiz.models.pergunta_model import PerguntaModel
# from quiz.models.alternativa_model import AlternativaModel
# from quiz.models.pergunta_tema_model import PerguntaTemaModel
# from quiz.models.tema_model import TemaModel
from qzen.quiz.models.user_model import bd_query_post_users, bd_query_delete_id_user


bp_usuario = Blueprint("usuario_view", __name__, url_prefix="/usuario")


@bp_usuario.route("/", methods=["POST"])
def novo_usuario():
    data = request.get_json()
    response = bd_query_post_users(data["name"], data["email"], data["password"])
    return response


@bp_usuario.route("/<int:usuario_id>", methods=["GET"])
def perguntas_do_usuario(usuario_id):
    ...


@bp_usuario.route("/<int:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    response = bd_query_delete_id_user(usuario_id)
    return response


@bp_usuario.route("/<int:usuario_id>", methods=["PATCH", "PUT"])
def atualizar_usuario(usuario_id):
    ...
