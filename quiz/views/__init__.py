from flask import Flask


def init_app(app: Flask):
    from quiz.views.pergunta_view import bp_pergunta

    app.register_blueprint(bp_pergunta)

    from quiz.views.tema_view import bp_tema

    app.register_blueprint(bp_tema)

    from quiz.views.usuario_view import bp_usuario

    app.register_blueprint(bp_usuario)
