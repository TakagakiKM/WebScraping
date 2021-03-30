# Imports
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Definindo a url
url = 'https://www.fundamentus.com.br/resultado.php'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                         'Chrome/76.0.3809.100 Safari/537.36'}

# Realizando o request:
try:
    request = Request(url, headers=headers)
    response = urlopen(request)
    print("Request realizado!")
    print(response.getcode())
    html = response.read()

# Tratando possíveis erros:
except HTTPError as e:
    print('HTTPError\n\n')
    print(response.getcode())
    print(e.reason)

except URLError as e:

    print('URLError\n\n')
    print(response.getcode())
    print(e.reason)


# Instanciando um objeto BeautifulSoup:
soup = BeautifulSoup(html, 'html.parser')

# Pegando os nomes das colunas da tabela
colunas_names = [col.getText() for col in soup.find('table', {'id': 'resultado'}).find('thead').findAll('th')]
colunas = {i: col.getText() for i, col in enumerate(soup.find('table', {'id': 'resultado'}).find('thead').findAll('th'))}

# Criando um DataFrame com os nomes das colunas
dados = pd.DataFrame(columns=colunas_names)

# Pegando os dados da tabela por linha
for i in range(len(soup.find('table', {'id': 'resultado'}).find('tbody').findAll('tr'))):
    linha = soup.find('table', {'id': 'resultado'}).find('tbody').findAll('tr')[i].getText().split('\n')[1:]
    inserir_linha = pd.DataFrame(linha).T.rename(columns=colunas)
    dados = pd.concat([dados, inserir_linha], ignore_index=True)

print(dados)