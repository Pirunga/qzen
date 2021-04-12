from . import db


class PerguntaTemaModel(db.Model):
    __tablename__ = "pergunta_temas"

    id = db.Column(db.Integer, primary_key=True)

    pergunta_id = db.Column(
        db.Integer,
        db.ForeignKey("perguntas.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    tema_id = db.Column(
        db.Integer,
        db.ForeignKey("temas.id", opudate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
