import datetime
import psycopg2
import sys
import os
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from tqdm import tqdm

NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
CONSTA01 = 'Processos encontrados'
CONSTA02 = 'Audiências'
EXECUTAVEL = 'C:/Users/teste/OneDrive/Documentos/'  # Caminho do WebDriver

class SPVAutomatico:

    def __init__(self, filtro=0):
        self.filtro = filtro

    def conectaBD(self):
        try:
            con = psycopg2.connect(
                host='10.0.270.18', 
                user='usr_teste', 
                password='teste', 
                database='db_teste'
            )

            cursor = con.cursor()

            cond = ' AND rg <> \'\' ' if self.filtro in (1, 3) else ''

            sql = f'''
            SELECT DISTINCT 
                p.Cod_Cliente, p.Cod_Pesquisa, e.UF, p.Data_Entrada,
                COALESCE(p.nome_corrigido, p.nome) AS Nome,
                p.CPF, COALESCE(p.rg_corrigido, p.rg) AS RG,
                p.Nascimento, COALESCE(p.mae_corrigido, p.mae) AS Mae,
                p.anexo AS Anexo, ps.Resultado, ps.cod_spv_tipo
            FROM pesquisa p
            INNER JOIN servico s ON p.Cod_Servico = s.Cod_Servico
            LEFT JOIN lote_pesquisa lp ON p.Cod_Pesquisa = lp.Cod_Pesquisa
            LEFT JOIN lote l ON l.cod_lote = lp.cod_lote
            LEFT JOIN estado e ON e.Cod_UF = p.Cod_UF
            LEFT JOIN pesquisa_spv ps ON ps.Cod_Pesquisa = p.Cod_Pesquisa
                AND ps.Cod_SPV = 1 AND ps.filtro = %s
            WHERE p.Data_Conclusao IS NULL
              AND ps.resultado IS NULL
              AND p.tipo = 0
              AND p.cpf <> ''
              {cond}
              AND (e.UF = 'SP' OR p.Cod_UF_Nascimento = 26 OR p.Cod_UF_RG = 26)
            GROUP BY p.cod_pesquisa
            ORDER BY nome ASC, resultado DESC
            LIMIT 210
            '''
            cursor.execute(sql, (self.filtro,))
            resultados = cursor.fetchall()
            cursor.close()
            con.close()
            return resultados

        except psycopg2.Error as e:
            print(f"[ERRO BD] {e}")
            return []


    def pesquisa(self):
        inicio = datetime.datetime.now()
        registros = self.conectaBD()

        if registros:
            for dados in tqdm(registros):
                cod_cliente, cod_pesquisa, uf, data_entrada, nome, cpf, rg, nascimento, mae, anexo, resultado, spv_tipo = dados
                self.executaPesquisa(nome, cpf, rg, cod_pesquisa, spv_tipo)

                tempo_gasto = (datetime.datetime.now() - inicio).total_seconds()
                if tempo_gasto >= 600:
                    print("[INFO] Tempo limite alcançado, finalizando ciclo.")
                    return

            if self.filtro < 3:
                print(f"[INFO] Reiniciando com filtro {self.filtro + 1}")
                SPVAutomatico(self.filtro + 1).pesquisa()
            else:
                print("[INFO] Recomeçando do início...")
                self.restarta_programa()

        else:
            print("[INFO] Nenhuma pesquisa encontrada. Aguardando...")
            time.sleep(60)
            self.restarta_programa()

    def executaPesquisa(self, nome, cpf, rg, cod_pesquisa, spv_tipo):
        documento = None
        if self.filtro == 0 and cpf:
            documento = cpf
        elif self.filtro in (1, 3) and rg:
            documento = rg
        elif self.filtro == 2 and nome:
            documento = nome

        if not documento:
            print(f"[AVISO] Documento inválido para filtro {self.filtro}. Ignorando...")
            return

        site = self.carregaSite(documento)
        resultado = self.checaResultado(site)

        try:
            con = psycopg2.connect(
                host='localhost',
                user='seu_usuario',
                password='sua_senha',
                dbname='seu_banco'
            )
            cursor = con.cursor()
            sql = '''
                INSERT INTO pesquisa_spv 
                (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id)
                VALUES (%s, 1, 36, NULL, %s, -1, %s, 1)
            '''
            cursor.execute(sql, (cod_pesquisa, resultado, self.filtro))
            con.commit()
            cursor.close()
            con.close()

        except psycopg2.Error as e:
            print(f"[ERRO INSERT] {e}")


    def carregaSite(self, documento):
        service = Service(executable_path=EXECUTAVEL + "msedgedriver.exe")
        options = Options()
        options.add_argument("-headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Edge(service=service, options=options)
        browser.get("https://esaj.tjsp.jus.br/cpopg/open.do")

        try:
            select_el = browser.find_element('xpath', '//*[@id="cbPesquisa"]')
            select = Select(select_el)

            if self.filtro in (0, 1, 3):
                select.select_by_value('DOCPARTE')
                browser.find_element('xpath', '//*[@id="campo_DOCPARTE"]').send_keys(documento)

            elif self.filtro == 2:
                select.select_by_value('NMPARTE')
                browser.find_element('xpath', '//*[@id="pesquisarPorNomeCompleto"]').click()
                browser.find_element('xpath', '//*[@id="campo_NMPARTE"]').send_keys(documento)

            browser.find_element('xpath', '//*[@id="botaoConsultarProcessos"]').click()
            time.sleep(2)  # Espera mínima
        except Exception as e:
            print(f"[ERRO SELENIUM] {e}")
            browser.quit()
            time.sleep(120)
            self.restarta_programa()

        html = browser.page_source
        browser.quit()
        return html

    def checaResultado(self, site):
        if NADA_CONSTA in site:
            return 1
        elif (CONSTA01 in site or CONSTA02 in site) and ('Criminal' in site or 'criminal' in site):
            return 2
        elif CONSTA01 in site or CONSTA02 in site:
            return 5
        else:
            return 7

    def restarta_programa(self):
        print("[INFO] Reiniciando o programa...")
        time.sleep(5)
        self.__init__(0)
        self.pesquisa()


if __name__ == "__main__":
    p = SPVAutomatico(0)
    p.pesquisa()
