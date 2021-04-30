from quiz.models.alternativa_model import AlternativaModel
from googlesearch import search


def serialize_perguntas(perguntas_list):
    serialized = []

    for pergunta in perguntas_list:

        alternativas = AlternativaModel.query.filter(
            AlternativaModel.pergunta_id == pergunta.id
        ).first()

        serialized.append(
            {
                "id": pergunta.id,
                "pergunta": pergunta.pergunta,
                "resposta": pergunta.resposta,
                "temas": [tema.tema for tema in pergunta.tema_list],
                "google_links": search(pergunta.pergunta, num_results=3, lang="pt"),
                "alternativas": {
                    "id": alternativas.id,
                    "alternativa1": alternativas.alternativa1,
                    "alternativa2": alternativas.alternativa2,
                    "alternativa3": alternativas.alternativa3,
                },
            }
        )

    return serialized


def serialize_pergunta(pergunta):
    alternativas = AlternativaModel.query.filter(
        AlternativaModel.pergunta_id == pergunta.id
    ).first()

    serialized = {
        "id": pergunta.id,
        "pergunta": pergunta.pergunta,
        "resposta": pergunta.resposta,
        "temas": [tema.tema for tema in pergunta.tema_list],
        "google_links": search(pergunta.pergunta, num_results=3, lang="pt"),
        "alternativas": {
            "id": alternativas.id,
            "alternativa1": alternativas.alternativa1,
            "alternativa2": alternativas.alternativa2,
            "alternativa3": alternativas.alternativa3,
        },
    }

    return serialized
