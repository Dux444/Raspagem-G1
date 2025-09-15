import requests
from bs4 import BeautifulSoup
import csv

url = "https://g1.globo.com/"

print(f"Baixando a página: {url}")

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar a página: {e}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

all_links = soup.find_all('a')

dados_extraidos = []

print(f"Buscando notícias entre {len(all_links)} links...")


for link in all_links:
    titulo = ''
    url_noticia = link.get('href')

    titulo_tag = link.find('h2') or link.find('h3') or link.find('p')
        
    if titulo_tag:
        titulo = titulo_tag.get_text(strip=True)
        
        if len(titulo) > 20 and 'globo.com' in url_noticia:
            dados_extraidos.append({'titulo': titulo, 'url': url_noticia})

# SALVAMENTO
csv_filename = 'Relatorio.csv'
try:
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['titulo', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados_extraidos)

    print(f"Dados salvos com sucesso no arquivo '{csv_filename}'.")
    if not dados_extraidos:
        print("Aviso: O arquivo foi criado, mas não contém manchetes.")

except Exception as e:
    print(f"\nErro ao salvar o arquivo: {e}")