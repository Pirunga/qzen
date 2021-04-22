from . import db


class AlternativaModel(db.Model):
    __tablename__ = "alternativas"

    id = db.Column(db.Integer, primary_key=True)
    alternativa1 = db.Column(db.String, nullable=False)
    alternativa2 = db.Column(db.String, nullable=False)
    alternativa3 = db.Column(db.String, nullable=False)

    pergunta_id = db.Column(db.Integer, db.ForeignKey("perguntas.id"), nullable=False)

    lista_pergunta = db.relationship(
        "PerguntaModel",
        lazy="joined",
        uselist=False,
        backref=db.backref("quetions", lazy="joined"),
    )
