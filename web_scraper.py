import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.edge.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

EXECUTAVEL = 'C:/Users/teste/OneDrive/Documentos/'

NADA_CONSTA = 'Não existem informações disponíveis para os parâmetros informados.'
CONSTA01 = 'Processos encontrados'
CONSTA02 = 'Audiências'

def carregar_site(filtro, documento):
    service = Service(executable_path=EXECUTAVEL + "msedgedriver.exe")
    options = Options()
    options.add_argument("-headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Edge(service=service, options=options)

    browser.get("https://esaj.tjsp.jus.br/cpopg/open.do")

    try:
        select_el = browser.find_element('xpath', '//*[@id="cbPesquisa"]')
        select_ob = Select(select_el)

        if filtro in [0, 1, 3]:
            select_ob.select_by_value('DOCPARTE')
            browser.find_element('xpath', '//*[@id="campo_DOCPARTE"]').send_keys(documento)
        elif filtro == 2:
            select_ob.select_by_value('NMPARTE')
            browser.find_element('xpath', '//*[@id="pesquisarPorNomeCompleto"]').click()
            browser.find_element('xpath', '//*[@id="campo_NMPARTE"]').send_keys(documento)

        browser.find_element('xpath', '//*[@id="botaoConsultarProcessos"]').click()
    except:
        time.sleep(120)
        raise RuntimeError("Erro ao carregar o site.")

    return browser.page_source
