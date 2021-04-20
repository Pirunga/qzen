from . import db


class TemaModel(db.Model):
    __tablename__ = "temas"

    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String, nullable=False, unique=True)
    # usuario_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey(
    #         "usuarios.id",
    #         onupdate="CASCADE",
    #         ondelete="CASCADE",
    #     ),
    # )

    pergunta_list = db.relationship(
        "PerguntaModel",
        lazy="joined",
        backref=db.backref("tema_list", lazy="joined"),
        secondary="pergunta_temas",
    )
