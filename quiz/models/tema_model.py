from . import db


class TemaModel(db.Model):
    __tablename__ = "temas"

    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String, nullable=False)

    pergunta_list = db.relationship(
        "PerguntaModel",
        lazy="joined",
        backref=db.backref("tema_list", lazy="joined"),
        secondary="pergunta_temas",
    )
