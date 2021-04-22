from flask import Blueprint, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from quiz.models.tema_model import TemaModel
from quiz.serializers.tema_serializer import serializer_temas

bp_tema = Blueprint("tema_view", __name__, url_prefix="/tema")


@bp_tema.route("/<string:tema>", methods=["GET"])
def pergunta_do_tema(tema):
    select = TemaModel.query.filter_by(tema=tema).first()

    if not select:
        return {'msg': 'Theme not found'}, HTTPStatus.NOT_FOUND

    lista = serializer_temas(select)[0]

    if len(lista["pergunta_list"]) > 0:
        return {lista["pergunta_list"]}, HTTPStatus.FOUND

    return {"msg": "Questions not found"}, HTTPStatus.NOT_FOUND


@bp_tema.route("/", methods=["POST"])
@jwt_required()
def novo_tema():
    session = current_app.db.session

    user_id = get_jwt_identity()

    if not user_id:
        return {'msg': 'User not found'}, HTTPStatus.NOT_FOUND

    body = request.get_json()

    new_tema = body.get('tema')

    if not new_tema:
        return {'msg': 'Verify body request'}, HTTPStatus.BAD_REQUEST

    table_theme = TemaModel(tema=new_tema, usuario_id=user_id)

    session.add(table_theme)
    session.commit()

    return {"msg": "Theme created"}, HTTPStatus.CREATED


@bp_tema.route('/<int:tema_id>', methods=['PATCH, PUT'])
@jwt_required()
def atualizar_tema(tema_id):
    session = current_app.db.session
    usuario_id = get_jwt_identity()

    if not usuario_id:
        return {'msg': 'User not found'}, HTTPStatus.UNAUTHORIZED

    body = request.get_json()

    new_tema = body.get('tema')

    if not new_tema:
        return {'msg': 'Verify body request'}, HTTPStatus.BAD_REQUEST

    found_tema: TemaModel = TemaModel.query.get(tema_id)

    if not found_tema:
        return {'msg': 'Tema not found'}, HTTPStatus.NOT_FOUND

    if usuario_id != found_tema.usuario_id:
        return {'msg': 'Unauthorized user'}, HTTPStatus.UNAUTHORIZED

    found_tema.tema = new_tema

    session.add(found_tema)
    session.commit()

    return {'tema': found_tema.tema}, HTTPStatus.OK


@bp_tema.route('/<int:tema_id>', methods=['DELETE'])
@jwt_required()
def delete_tema(tema_id):
    session = current_app.db.session

    usuario_id = get_jwt_identity()

    if not usuario_id:
        return {'msg': 'User not found'}, HTTPStatus.UNAUTHORIZED

    found_tema: TemaModel = TemaModel.query.get(tema_id)

    if not found_tema:
        return {'msg': 'Tema not found'}, HTTPStatus.NOT_FOUND

    if usuario_id != found_tema.usuario_id:
        return {'msg': 'User Unauthorized'}, HTTPStatus.UNAUTHORIZED

    session.delete(found_tema)
    session.commit()

    return {'msg': 'Tema deleted'}, HTTPStatus.OK
