from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from datetime import timedelta
from http import HTTPStatus

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel


bp_usuario = Blueprint("usuario_view", __name__, url_prefix="/usuario")


@bp_usuario.route("/register", methods=["POST"])
def novo_usuario():
    session = current_app.db.session

    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    password = data.get("senha")

    usuario = UserModel(nome=nome, email=email, usuario_pontos=0)
    usuario.password = password

    access_token = create_access_token(
        identity=usuario.id, expires_delta=timedelta(days=5)
    )
    fresh_token = create_refresh_token(
        identity=usuario.id, expires_delta=timedelta(days=15)
    )

    session.add(usuario)
    session.commit()

    return {
        "usuario": usuario.nome,
        "email": usuario.email,
        "access_token": access_token,
        "fresh_token": fresh_token,
    }, HTTPStatus.CREATED


@bp_usuario.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    found_user: UserModel = UserModel.query.filter_by(email=email).first()

    if not found_user or not found_user.check_password(password):
        return {"msg": "Usuário não encontrado."}, HTTPStatus.BAD_REQUEST

    access_token = create_access_token(
        identity=found_user.id, expires_delta=timedelta(days=5)
    )
    fresh_token = create_access_token(
        identity=found_user.id, fresh=True, expires_delta=timedelta(days=15)
    )

    return {"access_token": access_token, "fresh_token": fresh_token}


@bp_usuario.route("/<int:usuario_id>", methods=["GET"])
def perguntas_do_usuario(usuario_id):
    ...


@bp_usuario.route("/<int:usuario_id>", methods=["DELETE"])
@jwt_required(refresh=True)
def deletar_usuario(usuario_id):
    session = current_app.db

    found_user = UserModel.querry.get(usuario_id)
    UserModel.delete(found_user)


    session.commit()

    return {"msg": "Usuário deletado"}, HTTPStatus.OK


@bp_usuario.route("/<int:usuario_id>", methods=["PATCH", "PUT"])
def atualizar_usuario(usuario_id):
    ...
