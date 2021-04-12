from flask import Blueprint, request, current_app

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel


bp_tema = Blueprint("tema_view", __name__, url_prefix="/tema")


@bp_tema.route("/<string:tema>", methods=["GET"])
def pergunta_aletoria(tema):
    ...


@bp_tema.route("/", methods=["POST"])
def novo_tema():
    ...
