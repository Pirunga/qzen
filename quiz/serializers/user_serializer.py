from quiz.models.user_model import UserModel
from googlesearch import search


def user_serializer(user_id: int):
    user = UserModel.query.get(user_id)
    
    if not user:
        return False
    
    lista_perguntas = user.lista_perguntas
    
    return {
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'pontuação': user.usuario_pontos,
        'perguntas': [
            {
            'id': p.id,
            'pergunta': p.pergunta,
            'resposta': p.resposta,
            'google_links': search(p.pergunta, num_results=3, lang='pt')
            } for p in lista_perguntas
        ]
    }
