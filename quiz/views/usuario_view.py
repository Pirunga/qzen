from flask import Blueprint, request, current_app

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel


bp_usuario = Blueprint("usuario_view", __name__, url_prefix="/usuario")


@bp_usuario.route("/", methods=["POST"])
def novo_usuario():
    ...


@bp_usuario.route("/<int:usuario_id>", methods=["GET"])
def perguntas_do_usuario(usuario_id):
    ...


@bp_usuario.route("/<int:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    ...


@bp_usuario.route("/<int:usuario_id>", methods=["PATCH", "PUT"])
def atualizar_usuario(usuario_id):
    ...
