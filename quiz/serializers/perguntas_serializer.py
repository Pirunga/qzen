from quiz.models.alternativa_model import AlternativaModel


def serialize_perguntas(perguntas_list):
    serialized = []
    
    for pergunta in perguntas_list:
        
        alternativas = AlternativaModel.query.filter(AlternativaModel.pergunta_id == pergunta.id).first()

        serialized.append({
                "id": pergunta.id,
                "resposta": pergunta.resposta,
                "temas": [tema.tema for tema in pergunta.tema_list],
                "alternativas": {
                    "id": alternativas.id, 
                    "alternativa1": alternativas.alternativa1, 
                    "alternativa2": alternativas.alternativa2, 
                    "alternativa3": alternativas.alternativa3
                    }
            })
    
    return serialized


def serialize_pergunta(pergunta):
    alternativas = AlternativaModel.query.filter(AlternativaModel.pergunta_id == pergunta.id).first()

    serialized = {
                "id": pergunta.id,
                "resposta": pergunta.resposta,
                "temas": [tema.tema for tema in pergunta.tema_list],
                "alternativas": {
                    "id": alternativas.id, 
                    "alternativa1": alternativas.alternativa1, 
                    "alternativa2": alternativas.alternativa2, 
                    "alternativa3": alternativas.alternativa3
                    }
            }
    
    return serialized