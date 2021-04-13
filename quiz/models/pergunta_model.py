from . import db


class PerguntaModel(db.Model):
    __tablename__ = "perguntas"

    id = db.Column(db.Integer, primary_key=True)
    resposta = db.Column(db.String, nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
