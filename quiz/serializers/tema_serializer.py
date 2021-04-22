from quiz.serializers.perguntas_serializer import serialize_pergunta


def serializer_temas(tema):
    serializer = {
            "pergunta_list": [serialize_pergunta(pergunta) for pergunta in tema.pergunta_list]
    }

    return serializer
