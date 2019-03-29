import requests
import json
from bs4 import BeautifulSoup as bs
import base64
import posixpath
from urllib.parse import urljoin

BASE_URL = 'http://www.gnre.pe.gov.br/gnre/v/tabelas/'
URL_CON_RECEITA = 'consultarReceitas'
URL_CON_DET_RECEITA = 'consultarDetReceitas'
URL_CON_PRODUTOS = 'consultarProdutos'
URL_CON_DOCUMENTOS = 'consultarDocumentos'
URL_CON_CAMPOS = 'consultarCampos'

def tabela_gnre(url):
    with requests.session() as session:
        ## CONSULTA RECEITAS ##
        consultar_tabela = session.get(url=url)
        json_data = json.loads(consultar_tabela.text)
        tabela = json_data['content']
        soup = bs(tabela, 'lxml')
        colunas = soup.thead
        linhas = soup.tbody
        a = []
        for linha in linhas.children:
            linha = linha(text=True)
            for coluna in colunas:
                coluna = coluna(text=True)
                dictio = dict(zip(coluna, linha))
                a.append(dictio)
        return a

def make_url(URL, PARAM):
    path = posixpath.join(URL, PARAM)
    return urljoin(BASE_URL, path)

def consultar_receita(param):
    return tabela_gnre(make_url(URL_CON_RECEITA, param))

def consultar_det_receita(param):
    return tabela_gnre(make_url(URL_CON_DET_RECEITA, param))

def consultar_produtos(param):
    return tabela_gnre(make_url(URL_CON_PRODUTOS, param))

def consultar_documentos(param):
    return tabela_gnre(make_url(URL_CON_DOCUMENTOS, param))

def consultar_campos(param):
    return tabela_gnre(make_url(URL_CON_CAMPOS, param))


def arquivo_json(event, context):
    param = event['queryStringParameters']['uf']
    arquivo_json = {
        'receita': consultar_receita(param),
        'det_receita': consultar_receita(param),
        'produtos': consultar_produtos(param),
        'documentos': consultar_documentos(param),
        'campos': consultar_campos(param) ## CAMPOS NÃO RECEBE PARAMÊTRO '0' ##
    }

    arquivo_json = str(arquivo_json)
    arquivo_json = bytes(arquivo_json, 'utf-8')
    return base64.b64encode(arquivo_json)


