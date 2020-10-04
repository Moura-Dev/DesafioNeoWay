from pandas.io import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
cidade = "SP"
payload = {'UF':cidade,'qtdrow':'100','pagini':'1','pagfim':'100'}
url = "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm"

html_content = requests.post(url,data=payload).text

# Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.findAll(name='table')

# Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
df_full = pd.read_html(str(table))[1]
# df = df_full[['Localidade', 'Faixa de CEP',]]

# df_full.columns = ['Localidade', 'Faixa de CEP','Situação', 'Tipo de Faixa']

df1 = df_full.drop(['Situação', 'Tipo de Faixa'], axis=1)
# df1 = df[['Localidade', 'Faixa de CEP']]
# print(df1)

# df1.encoding = ''

# Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
# df1.to_dict('records')
print(df1)
df1 = df1.to_json(orient="records", force_ascii=False)


# # Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open('ranking.json', 'w') as jp:
    js = json.dumps(df1, indent=4, ensure_ascii=False)
    jp.write(js)