from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    usuario_pontos = db.Column(db.Integer, nullable=False)

    lista_perguntas = db.relationship(
        "PerguntaModel",
        lazy="joined",
        backref=db.backref("question", lazy="joined"),
    )

    @property
    def password(self):
        raise TypeError("A senha não pode ser acessada")

    @password.setter
    def password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
