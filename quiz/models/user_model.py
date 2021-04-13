from . import db


class UserModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)

    lista_perguntas = db.relationship(
        "PerguntaModel",
        lazy="joined",
        backref=db.backref("question", lazy="joined"),
    )
