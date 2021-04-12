from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from quiz.models.pergunta_model import PerguntaModel
    from quiz.models.alternativa_model import AlternativaModel
    from quiz.models.pergunta_tema_model import PerguntaTemaModel
    from quiz.models.tema_model import TemaModel
    from quiz.models.user_model import UserModel
