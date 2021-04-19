from flask import Blueprint, request, current_app
from http import HTTPStatus
import random
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel

from quiz.serializers.perguntas_serializer import serialize_perguntas, serialize_pergunta


bp_pergunta = Blueprint("pergunta_view", __name__, url_prefix="/pergunta")


@bp_pergunta.route("/", methods=["GET"])
def todas_pergutnas():
    try:
        given_tema = request.args.get("tema")

        if given_tema:

            session = current_app.db.session
            found_tema = TemaModel.query.filter(TemaModel.tema == given_tema).first()

            if not found_tema:
                return {"msg": "This 'tema' doesn't exist."}, HTTPStatus.BAD_REQUEST
            
            perguntas = session.query(PerguntaModel).join(PerguntaTemaModel).filter(PerguntaTemaModel.tema_id == found_tema.id).all()
            
            response = response = serialize_perguntas(perguntas)

            return {"data": response}, HTTPStatus.OK

        perguntas = PerguntaModel.query.all()

        response = serialize_perguntas(perguntas)
        
        return {"data": response}, HTTPStatus.OK

    except:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/aleatoria", methods=["GET"])
def pergunta_aleatoria():
    try:
        given_tema = request.args.get("tema")

        if given_tema:

            session = current_app.db.session
            found_tema = TemaModel.query.filter(TemaModel.tema == given_tema).first()

            if not found_tema:
                return {"msg": "This 'tema' doesn't exist."}, HTTPStatus.BAD_REQUEST

            pergunta = random.choice(
                session.query(PerguntaModel)
                .join(PerguntaTemaModel)
                .filter(PerguntaTemaModel.tema_id == found_tema.id)
                .all()
            )

            response = serialize_pergunta(pergunta)

            return {"data": response}, HTTPStatus.OK

        pergunta = random.choice(PerguntaModel.query.all())

        response = serialize_pergunta(pergunta)

        return {"data": response}, HTTPStatus.OK

    except:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/<int:pergunta_id>", methods=["GET"])
def pergunta_por_id(pergunta_id):
    try:
        pergunta = PerguntaModel.query.get(pergunta_id)

        response = serialize_pergunta(pergunta)

        return {"data": response}, HTTPStatus.OK

    except AttributeError:

        return {"msg": "This 'pergunta' doesn't exist."}, HTTPStatus.BAD_REQUEST

    except Exception:

        return {"msg": "Something went wrong."}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp_pergunta.route("/", methods=["POST"])
@jwt_required()
def criar_pergunta_nova():
    session = current_app.db.session
    body = request.get_json()

    usuario_id = get_jwt_identity()

    try:
        pergunta = body.get('pergunta')
        resposta = body.get('resposta')
        tema = body.get('tema')

        nova_pergunta: PerguntaModel = PerguntaModel(pergunta=pergunta, resposta=resposta, usuario_id=usuario_id)
        session.add(nova_pergunta)

        found_tema: TemaModel = TemaModel.query.get(tema)

        if not found_tema:
            return {'msg': 'Tema not found'}, HTTPStatus.NOT_FOUND

        pergunta_tema: PerguntaTemaModel = PerguntaTemaModel(pergunta_id=nova_pergunta.id, tema_id=found_tema.id)

        session.add_all([nova_pergunta, pergunta_tema])

        session.commit()

        alternativas = body.get('alternativas')

        alternativas["pergunta_id"] = nova_pergunta.id

        nova_alternativas: AlternativaModel = AlternativaModel(**alternativas)

        session.add(nova_alternativas)
        session.commit()

        return {"msg": "Created question"}, HTTPStatus.CREATED

    except AttributeError:
        return {"msg": "Verify body request"}, HTTPStatus.BAD_REQUEST

@bp_pergunta.route("/<int:pergunta_id>", methods=["DELETE"])
@jwt_required()
def deletar_pergunta(pergunta_id):
    session = current_app.db.session

    usuario_id = get_jwt_identity()

    pergunta: PerguntaModel = PerguntaModel.query.get(pergunta_id)

    if usuario_id != pergunta.usuario_id:
        return {'msg': 'Unauthorized user'}, HTTPStatus.UNAUTHORIZED

    if not pergunta:
        return {'msg': 'Question not found'}, HTTPStatus.NOT_FOUND

    session.delete(pergunta)
    session.commit()

    return {'msg': 'Question deleted'}, HTTPStatus.OK


@bp_pergunta.route("/<int:pergunta_id>", methods=["PATCH", "PUT"])
@jwt_required()
def atualizar_pergunta(pergunta_id):
    try:
        session = current_app.db.session
        body = request.get_json()

        usuario_id = get_jwt_identity()

        pergunta: PerguntaModel = PerguntaModel.query.get(pergunta_id)

        if not pergunta:
            return {'msg': 'Question not found'}, HTTPStatus.NOT_FOUND

        if usuario_id != pergunta.usuario_id:
            return {'msg': 'Unauthorized user'}, HTTPStatus.UNAUTHORIZED

        for key, value in body.items():
            if value and key != 'id':
                pergunta[key] = value

        session.add(pergunta)
        session.commit()

        response = serialize_pergunta(pergunta)

        return {"data": response}, HTTPStatus.OK

    except KeyError:
        return {'msg': 'Verify the request body'}, HTTPStatus.BAD_REQUEST

