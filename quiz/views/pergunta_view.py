from flask import Blueprint, request, current_app
from http import HTTPStatus
import random
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    jwt_required,
)

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel


bp_pergunta = Blueprint("pergunta_view", __name__, url_prefix="/pergunta")


@bp_pergunta.route("/", methods=["GET"])
def todas_pergutnas():
    try:
        perguntas = PerguntaModel.query.all()

        response = [
            {
                "id": pergunta.id,
                "resposta": pergunta.resposta,
                "temas": [tema.nome for tema in pergunta.tema_list],
            }
            for pergunta in perguntas
        ]

        return {"data": response}, HTTPStatus.OK

    except:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/aleatoria", methods=["GET"])
def pergunta_aleatoria():
    try:
        given_tema = request.args.get("tema")

        if given_tema:

            session = current_app.db.session
            found_tema = TemaModel.query.filter(TemaModel.nome == given_tema).first()

            if not found_tema:
                return {"msg": "This 'tema' doesn't exist."}, HTTPStatus.BAD_REQUEST

            pergunta = random.choice(
                session.query(PerguntaModel)
                .join(PerguntaTemaModel)
                .filter(PerguntaTemaModel.tema_id == found_tema.id)
                .all()
            )
            response = {
                "id": pergunta.id,
                "resposta": pergunta.resposta,
                "temas": [tema.nome for tema in pergunta.tema_list],
            }

            return {"data": response}, HTTPStatus.OK

        pergunta = random.choice(PerguntaModel.query.all())
        response = {
            "id": pergunta.id,
            "resposta": pergunta.resposta,
            "temas": [tema.nome for tema in pergunta.tema_list],
        }

        return {"data": response}, HTTPStatus.OK

    except:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/<int:pergunta_id>", methods=["GET"])
def pergunta_por_id(pergunta_id):
    try:
        pergunta = PerguntaModel.query.get(pergunta_id)

        response = {
            "id": pergunta.id,
            "resposta": pergunta.resposta,
            "temas": pergunta.tema_list,
        }

        return {"data": response}, HTTPStatus.OK

    except AttributeError:

        return {"msg": "This 'pergunta' doesn't exist."}, HTTPStatus.BAD_REQUEST

    except Exception:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/<int:pergunta_id>", methods=["POST"])
def criar_pergunta_nova(pergunta_id):
    body = request.get_json()


@bp_pergunta.route("/<int:pergunta_id>", methods=["DELETE"])
def deletar_pergunta(pergunta_id):
    ...


@bp_pergunta.route("/<int:pergunta_id>", methods=["PATCH", "PUT"])
def atualizar_pergunta(pergunta_id):
    ...
