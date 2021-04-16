from flask import Blueprint, request, current_app
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from http import HTTPStatus

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


@bp_tema.route('/<int:tema_id>', methods=['PATCH, PUT'])
@jwt_required()
def atualizar_tema(tema_id):
    session = current_app.db.session
    usuario_id = get_jwt_identity()

    body = request.get_json()

    found_tema: TemaModel = TemaModel.query.get(tema_id)

    if not found_tema:
        return {'msg': 'Tema not found'}, HTTPStatus.NOT_FOUND

    if usuario_id != found_tema.usuario_id:
        return {'msg': 'Unauthorized user'}, HTTPStatus.UNAUTHORIZED

    for key, value in body.items():
        if value and key != 'id':
            found_tema[key] = value

    session.add(found_tema)
    session.commit()

    return {'tema': found_tema.tema}, HTTPStatus.OK


@bp_tema.route('/<int:tema_id>', methods=['DELETE'])
@jwt_required()
def delete_tema(tema_id):
    session = current_app.db.session

    usuario_id = get_jwt_identity()

    found_tema: TemaModel = TemaModel.query.get(tema_id)

    if not found_tema:
        return {'msg': 'Tema not found'}, HTTPStatus.NOT_FOUND

    if usuario_id != found_tema.usuario_id:
        return {'msg': 'User Unauthorized'}, HTTPStatus.UNAUTHORIZED

    session.delete(found_tema)
    session.commit()

    return {'msg': 'Tema deleted'}, HTTPStatus.OK
