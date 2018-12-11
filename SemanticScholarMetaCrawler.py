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

# xpath para a div com todos os resultados //*[@id="main-content"]/div[1]/div
# xpath para o primeiro resultado //*[@id="main-content"]/div[1]/div/article[1]
# xpath para o titulo do primeiro resultado //*[@id="main-content"]/div[1]/div/article[1]/header/div
# xpath para os autores do primeiro resultado //*[@id="main-content"]/div[1]/div/article[1]/header/ul/li[1]
# xpath para o ano do primeiro resultado //*[@id="main-content"]/div[1]/div/article[1]/header/ul/li[3]
# xpath para a origem do primeiro resultado //*[@id="main-content"]/div[1]/div/article[1]/header/ul/li[2]
# xpath para nivel de citacoes //*[@id="main-content"]/div[1]/div/article[1]/footer/div[1]/li[1]
# xpath para velocidade de citacoes //*[@id="main-content"]/div[1]/div/article[1]/footer/div[1]/li[2]


def delayFechar(tempo):
    for ind in range(tempo, 0, -1):
        print("Browser fechando em " + str(ind) + " segundos")
        time.sleep(1)


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

url = str(input("Entre com o link\n"))

driver.get(url)
delayFechar(3)
teste = driver.find_element_by_class_name('search-result-title').get_attribute('href')
print(teste)

delayFechar(3)
driver.quit()
