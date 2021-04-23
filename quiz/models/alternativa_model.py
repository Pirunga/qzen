from . import db


class AlternativaModel(db.Model):
    __tablename__ = "alternativas"

    id = db.Column(db.Integer, primary_key=True)
    alternativa1 = db.Column(db.String, nullable=False)
    alternativa2 = db.Column(db.String, nullable=False)
    alternativa3 = db.Column(db.String, nullable=False)

    pergunta_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "perguntas.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
