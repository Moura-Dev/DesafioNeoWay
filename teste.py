from os import name
import requests
from bs4 import BeautifulSoup
from pprint import pprint


payload = {'UF':'SP','qtdrow':'100','pagini':'1','pagfim':'100'}
url = 'http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm'

#css_soup = BeautifulSoup('<p class="body"></p>')
#css_soup.p['class']

htmlResponse = requests.post(url,data=payload).content
soup = BeautifulSoup(htmlResponse, 'html.parser')
makediv = soup.find_all(["td","td", "class='tmptabela"])
for tag in makediv:
    todascidades= []
    for item in tag:
        if item == "Não codificada por logradouros" or item == "Total do município" or item=="Codificado por logradouros" or item=="Codificada por logradouros" or item=="Total do município" or item=="Exclusiva da sede urbana":
            pass
        else:
            todascidades.append(item.strip())
            #print(item)

    print(todascidades)