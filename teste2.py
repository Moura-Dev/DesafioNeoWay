from os import name
import json
from typing import ValuesView
import requests
from bs4 import BeautifulSoup
from pprint import pprint

cidade = "SP"
payload = {'UF':cidade,'qtdrow':'100','pagini':'1','pagfim':'100'}
url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'


htmlResponse = requests.post(url,data=payload).content.decode('iso-8859-1')
soup = BeautifulSoup(htmlResponse, 'html.parser')
makediv = soup.find_all(["td", 'class=tmptabela"'])
todascidades= []
todasUF = {}

teste = {makediv[i]: makediv[i + 1] for i in range(0, len(makediv), 2)}

for tag in makediv:
    for item in tag:
        if item == "Não codificada por logradouros" or item == "Total do município" or item=="Codificado por logradouros" or item=="Codificada por logradouros" or item=="Total do município" or item=="Exclusiva da sede urbana":
            pass
        else:
            todascidades.append(item.strip())

todasUF = {todascidades[i]: todascidades[i + 1] for i in range(0, len(todascidades), 2)}

print(teste)
# documento = json.dumps(todasUF)

# arquivo = open(cidade+'.json', 'w')
# arquivo.write(documento)
# arquivo.close()