# main.py

import time
import sys
import datetime
from tqdm import tqdm
import argparse

from database import buscar_pesquisas, salvar_resultado
from web_scraper import carregar_site
from utils import checa_resultado

def executa_pesquisa(filtro):
    pesquisas = buscar_pesquisas(filtro)
    if not pesquisas:
        print(f"[Filtro {filtro}] Nenhuma pesquisa encontrada.")
        return False

    tempo_inicio = datetime.datetime.now()

    for dados in tqdm(pesquisas, desc=f"Filtro {filtro}"):
        cod_cliente, cod_pesquisa, uf, data_entrada, nome, cpf, rg, nascimento, mae, anexo, resultado, spv_tipo = dados

        documento = cpf if filtro == 0 else rg if filtro in [1, 3] else nome
        if not documento:
            continue

        try:
            page = carregar_site(filtro, documento)
            result_code = checa_resultado(page)
            salvar_resultado(cod_pesquisa, result_code, filtro)
        except Exception as e:
            print(f"Erro na pesquisa {cod_pesquisa}: {e}")
            continue

        tempo_fim = datetime.datetime.now()
        if (tempo_fim - tempo_inicio).total_seconds() >= 600:
            print("Tempo limite atingido.")
            return False

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filtro', type=int, default=0, help='Filtro a ser utilizado (0 a 3)')
    args = parser.parse_args()

    filtro = args.filtro
    tentativas = 0

    while filtro <= 3:
        print(f"Iniciando filtro {filtro}...")
        sucesso = executa_pesquisa(filtro)

        if not sucesso:
            tentativas += 1
            if tentativas >= 3:
                print("Muitas tentativas sem sucesso. Aguardando 1 hora.")
                time.sleep(3600)
                tentativas = 0
            else:
                print("Aguardando para recomeçar...")
                time.sleep(60)
        else:
            filtro += 1

    print("Processo finalizado.")

if __name__ == "__main__":
    main()
