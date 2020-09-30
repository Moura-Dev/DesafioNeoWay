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
makediv = soup.find_all(["td", "class='tmptabela"])
for tag in makediv:
    todascidades= []
    cidade = ""
    cidades = [tag.text]
    for item in tag:
        todascidades.append(item)
        #print(item)
    print(todascidades)




#print(makediv)