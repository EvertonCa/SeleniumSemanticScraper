from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import platform

# sort por relevancia = https://www.semanticscholar.org/search?q=example&sort=relevance
# sort por ano = https://www.semanticscholar.org/search?q=example&sort=year
# sort de intervalo de ano https://www.semanticscholar.org/search?year%5B0%5D=1983&year%5B1%5D=2019&q=example&sort=relevance
# sort by Journal Article = https://www.semanticscholar.org/search?publicationType%5B0%5D=JournalArticle&q=example&sort=relevance
# sort by Review = https://www.semanticscholar.org/search?publicationType%5B0%5D=Reviews&q=example&sort=relevance
# sort by Lit Reviews = https://www.semanticscholar.org/search?publicationType%5B0%5D=Reviews&q=machine%20learning&sort=relevance
# sort by Review e Journal Article = https://www.semanticscholar.org/search?publicationType%5B0%5D=Reviews&publicationType%5B1%5D=JournalArticle&q=example&sort=relevance
# possiveis sorts de Publication Type: Journal Article, Review, Conference, Study, Letters and Comments, Editorial, Case Report, Clinical Trial, Meta Analysis, News.


def delayFechar(tempo):
    for ind in range(tempo, 0, -1):
        print("Browser fechando em " + str(ind) + " segundos")
        time.sleep(1)


print("Entre com as palavras chave para a pesquisa:")
palavras_chave = str(input())

print("Quantas paginas de resultados deseja fazer o download?")
paginas = int(input())

inicio_link = 'https://www.semanticscholar.org/search?q='
fim_link = '&sort=relevance&pdf=true'
fim_link_outras_comeco = '&sort=relevance&page='
fim_link_outras_fim = '&pdf=true'
meio_link = ''
palavras_separadas = palavras_chave.split()

for palavra in palavras_separadas:
    meio_link += palavra
    if palavra is not palavras_separadas[-1]:
        meio_link += '%20'

url1 = inicio_link + meio_link + fim_link
lista_de_urls = [url1]

for i in range(2, paginas+1):
    temp = inicio_link + meio_link + fim_link_outras_comeco + str(i) + fim_link_outras_fim
    lista_de_urls.append(temp)

options = webdriver.ChromeOptions()

diretorio_atual = os.getcwd()

plataforma = platform.system()
if plataforma == 'Darwin':
    diretorio_chromedriver = diretorio_atual + '/ChromeDriver/ChromeDriverMac'
elif plataforma == 'Windows':
    diretorio_chromedriver = diretorio_atual + '/ChromeDriver/ChromeDriverWin.exe'
else:
    diretorio_chromedriver = diretorio_atual + '/ChromeDriver/ChromeDriverLin'

diretorio_pdf = diretorio_atual + '/PDFs'

if os.path.exists(diretorio_pdf):
    pass
else:
    os.mkdir('PDFs')

options.add_experimental_option("prefs", {
  "download.default_directory": diretorio_pdf,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "plugins.always_open_pdf_externally": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(diretorio_chromedriver, chrome_options=options)

nomes_artigos = []

for url in lista_de_urls:
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'PDF')))
    finally:
        lista_de_artigos = driver.find_elements_by_class_name('search-result-title')
        print(len(lista_de_artigos))
        for artigo in lista_de_artigos:
            link = artigo.get_attribute('aria-label')
            print("Link: " + str(link))

delayFechar(3)
driver.quit()
