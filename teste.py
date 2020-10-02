# from numpy.core.records import record, records
from json import decoder
from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import unidecode

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
uf = "SP"
payload = {'UF':uf,'qtdrow':'100','pagini':'1','pagfim':'100'}
url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"
top10ranking = {}



html_content = requests.post(url,data=payload).content

# Parse HTML (Parsear o cont    eúdo HTML) - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.findAll(name='table')

# Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
df_full = pd.read_html(str(table),encoding="utf-8")[1]
df = df_full[['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']]

df.columns = ['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']
df1 = df.drop(['Situação', 'Tipo de Faixa'], axis=1)

# Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
df1 = df1.to_json(orient='records')

print(df1)

# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open(uf+'.json', 'w', encoding="utf-8") as jp:
    js = json.dumps(df1)
    jp.write(js)