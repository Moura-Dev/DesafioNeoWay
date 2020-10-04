from os import name
import json
from typing import ValuesView
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import unidecode
uf = "GO"
payload = {'UF':uf,'qtdrow':'100','pagini':'1','pagfim':'100'}
payload2 = {'UF':uf,'qtdrow':'100','pagini':'101','pagfim':'200'}
url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
todascidades= []
todascidades2=[]
todascidadesConcatenadas = []
todasUF = {}
todasUF2 = {}
todasUFConcatenadas = {}

def main():
    soup = makeSoup(url,payload)
    soup2 = makeSoup2(url,payload2)
    merge = mergeDict(soup,soup2)
    DumpJson(merge)


def makeSoup(url,payload):
    htmlResponse = requests.post(url,data=payload).content.decode('iso-8859-1')
    soup = BeautifulSoup(htmlResponse, 'html.parser')
    makediv = soup.find_all(["td", 'class=tmptabela'])
       
    for tag in makediv:
        for item in tag:
            if item == "Não codificada por logradouros" or item == "Total do município" or item=="Codificado por logradouros" or item=="Codificada por logradouros" or item=="Total do município" or item=="Exclusiva da sede urbana":
                pass
            else:
                item = unidecode.unidecode(item)
                todascidades.append(item.strip())

    todasUF = {todascidades[i]: todascidades[i + 1] for i in range(0, len(todascidades), 2)}
    return todascidades


def makeSoup2(url,payload2):
    htmlResponse = requests.post(url,data=payload2).content.decode('iso-8859-1')
    soup = BeautifulSoup(htmlResponse, 'html.parser')
    makediv = soup.find_all(["td", 'class=tmptabela'])
       
    for tag in makediv:
        for item in tag:
            if item == "Não codificada por logradouros" or item == "Total do município" or item=="Codificado por logradouros" or item=="Codificada por logradouros" or item=="Total do município" or item=="Exclusiva da sede urbana":
                pass
            else:
                item = unidecode.unidecode(item)
                todascidades2.append(item.strip())

    todasUF2 = {todascidades2[i]: todascidades2[i + 1] for i in range(0, len(todascidades2), 2)}
    return todascidades2


#Mesclar dicionários e adicionar valores de chaves comuns em uma lista
def mergeDict(todascidades,todascidades2):
    for d in todascidades2:
        todascidades.append(d)
    todascidadesConcatenadas = todascidades
    todasUFConcatenadas = {todascidadesConcatenadas[i]: todascidadesConcatenadas[i + 1] for i in range(0, len(todascidadesConcatenadas), 2)}
    return todasUFConcatenadas

def DumpJson(todasUFConcatenadas):
    documento = json.dumps(todasUFConcatenadas)
    arquivo = open(uf+'.json', 'w')
    arquivo.write(documento)
    arquivo.close()


main()


if __name__ == "__main__":
    pass