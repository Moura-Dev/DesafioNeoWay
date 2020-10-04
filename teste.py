# from numpy.core.records import record, records
from json import decoder
from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import unidecode

uf = "SP"
payload = {'UF':uf,'qtdrow':'100','pagini':'1','pagfim':'100'}
payload2= {'UF':uf,'qtdrow':'100','pagini':'101','pagfim':'200'}
url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
top10ranking = {}


def main():
    soup = makeSoup(url,uf,payload)
    soup2 = makeSoup2(url,uf,payload2)
    dfdata = dataStructure(soup)
    #dfdata2 = dataStructure2(soup2)
    DumpJson(dfdata)
    #DumpJson2(dfdata2)

# (Pegar conteúdo HTML a partir da URL)
def makeSoup(url,uf,payload):

    html_content = requests.post(url,data=payload).content
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.findAll(name='table')
    return table

def makeSoup2(url,uf,payload2):

    html_content = requests.post(url,data=payload2).content
    soup = BeautifulSoup(html_content, 'html.parser')
    table2 = soup.findAll(name='table')
    return table2


def dataStructure(table):

    #(Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table),encoding="utf-8")[1]
    df = df_full[['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']]

    df.columns = ['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']
    df1 = df.drop(['Situação', 'Tipo de Faixa'], axis=1)

    #(Transformar os Dados em um Dicionário de dados próprio)
    df1 = df1.to_json(orient='records', force_ascii=False)

    return df1

def dataStructure2(table2):

    #Conversion (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table2),encoding="utf-8")[0]
    df = df_full[['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']]

    df.columns = ['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']
    df2 = df.drop(['Situação', 'Tipo de Faixa'], axis=1)

    # (Transformar os Dados em um Dicionário de dados próprio)
    df2 = df2.to_json(orient='records', force_ascii=False)

    return df2

# (Converter e salvar em um arquivo JSON)
def DumpJson(df1):
    with open(uf+'.json', 'w', encoding="utf-8") as jp:
        js = json.dumps(df1,ensure_ascii=False)
        jp.write(js)

# def DumpJson2(df2):
#     with open(uf+'.json', 'a', encoding="utf-8") as jp:
#         js = json.dumps(df2,ensure_ascii=False)
#         jp.write(js)
