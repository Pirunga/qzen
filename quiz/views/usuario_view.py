from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from http import HTTPStatus

from quiz.models.pergunta_model import PerguntaModel
from quiz.models.alternativa_model import AlternativaModel
from quiz.models.pergunta_tema_model import PerguntaTemaModel
from quiz.models.tema_model import TemaModel
from quiz.models.user_model import UserModel
from quiz.serializers.user_serializer import UserSerializer


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
    
    user_serializer = UserSerializer(usuario.id)

    return user_serializer, HTTPStatus.CREATED

@bp_usuario.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("senha")

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
    
    user_serializer = UserSerializer(usuario_id)
    
    if not user_serializer:
        
        return {'msg': 'Usuário não encontrado'}, HTTPStatus.NOT_FOUND
    
    else:
        
        name = user_serializer.get('nome')
        questions = user_serializer.get('perguntas')
        
        return { 'nome': name, 'perguntas': questions }, HTTPStatus.OK


@bp_usuario.route("/", methods=["DELETE"])
@jwt_required(refresh=True)
def deletar_usuario():
    session = current_app.db

    id_user = get_jwt_identity()
    found_user = UserModel.query.get(id_user)

    id_user = get_jwt_identity()
    found_user = UserModel.query.get(id_user)
    
    session.delete(found_user)
    session.commit()

    return {"msg": "Usuário deletado"}, HTTPStatus.OK


@bp_usuario.route("/", methods=["PATCH", "PUT"])
@jwt_required()
def atualizar_usuario():
    
    session = current_app.db.session
    
    id_user = get_jwt_identity()
    user = UserModel.query.get(id_user)
    
    if not user:
        
        return { 'msg': 'Usuário não encontrado' }, HTTPStatus.NOT_FOUND

    else:
         
        body = request.get_json()
        user_name = body.get('nome')
        user_email = body.get('email')
        user_score = body.get('usuario_pontos')
        
        if not user_name and not user_email and not user_score:
            
            return { 'msg': 'Atributos inválidos' }, HTTPStatus.BAD_REQUEST
                    
        if user_name:
            user.nome = user_name
            
        if user_email:
            user.email = user_email
            
        if user_score:
            user.usuario_pontos = user_score       
        
        session.add(user)
        session.commit()
        
        return { 'msg': 'Usuário atualizado com sucesso' }, HTTPStatus.OK
        
