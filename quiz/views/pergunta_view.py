from flask import Blueprint, request, current_app

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel


bp_pergunta = Blueprint("pergunta_view", __name__, url_prefix="/pergunta")


@bp_pergunta.route("/", methods=["GET"])
def todas_pergutnas():
    ...


@bp_pergunta.route("/aleatoria", methods=["GET"])
def pergunta_aleatoria():
    ...


@bp_pergunta.route("/<int:pergunta_id>", methods=["GET"])
def pergunta_por_id(pergunta_id):
    ...


@bp_pergunta.route("/", methods=["POST"])
def criar_pergunta_nova():
    ...


@bp_pergunta.route("/<int:pergunta_id>", methods=["DELETE"])
def deletar_pergunta(pergunta_id):
    ...


@bp_pergunta.route("/<int:pergunta_id>", methods=["PATCH", "PUT"])
def atualizar_pergunta(pergunta_id):
    ...
