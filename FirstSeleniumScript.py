from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def delayFechar(tempo):
    for ind in range(tempo, 0, -1):
        print("Browser fechando em " + str(ind) + " segundos")
        time.sleep(1)


def renomeador(links, palavra_chave):
    i = 1
    for link in links:
        nome_do_arquivo = link[38:]
        os.rename("PDFs/" + nome_do_arquivo, "PDFs/" + palavra_chave + " " + str(i) + ".pdf")
        i += 1


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
diretorio_pdf = diretorio_atual + '/PDFs'
diretorio_chromedriver = diretorio_atual + '/chromedriver'

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

download_links = []

for url in lista_de_urls:
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'PDF')))
    finally:
        lista_de_pdfs = driver.find_elements_by_partial_link_text("PDF")
        for pdf in lista_de_pdfs:
            download_links.append(pdf.get_attribute('href'))
            pdf.click()
delayFechar(3)
renomeador(download_links, palavras_chave)
driver.quit()
