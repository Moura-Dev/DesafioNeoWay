import json
import re
import requests
from bs4 import BeautifulSoup

url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'
UFs = (
    "AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT","PA","PB","PE","PI",
    "PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"
    )
inícios = (1, 100)
fins = (100, 200)
cidade = []
cidades = {}

ignorar = (
    "Não codificada por logradouros", "Total do município",
    "Codificado por logradouros", "Codificada por logradouros",
    "Total do município", "Exclusiva da sede urbana"
    )


def makeSoup(url, UF, inifim):
    payload = {'UF': UF, 'pagini': inifim[0], 'pagfim': inifim[1]}
    htmlResponse = requests.post(url, data=payload).content
    soup = BeautifulSoup(htmlResponse, 'html.parser')
    if not soup.find_all(string=re.compile("developer")):
        # if soup.findAll(text="developer"):
        make = soup.find_all(["td"])
        for tds in make:
            for td in tds:
                if td not in ignorar:
                    cidade.append(td.strip())


def DumpJson(cidade, cidades, UF):
    cidades = {cidade[i]: cidade[i + 1] for i in range(0, len(cidade), 2)}
    with open(UF+'.json', 'w', encoding="utf-8") as jp:
        js = json.dumps(cidades, ensure_ascii=False)
        jp.write(js)


for UF in UFs:
    for inifim in inícios, fins:
        makeSoup(url, UF, inifim)
    DumpJson(cidade, cidades, UF)
    cidade = []
    cidades.clear