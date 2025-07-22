# utils.py

NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
CONSTA01 = 'Processos encontrados'
CONSTA02 = 'Audiências'

def checa_resultado(page_source: str) -> int:
    """
    Verifica o resultado da pesquisa com base no conteúdo HTML retornado.
    Retorna:
    - 1: Nada Consta
    - 2: Consta Criminal
    - 5: Consta Cível
    - 7: Resultado Desconhecido
    """
    final_result = 7

    if NADA_CONSTA in page_source:
        final_result = 1
    elif (CONSTA01 in page_source or CONSTA02 in page_source):
        if 'Criminal' in page_source or 'criminal' in page_source:
            final_result = 2
        else:
            final_result = 5

    return final_result
