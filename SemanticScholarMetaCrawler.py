from selenium import webdriver
import Gerenciador
import Autor
import Artigo
from selenium.webdriver.common.keys import Keys
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


def delay(tempo):
    time.sleep(tempo)


def retornaListaAutores(autores):
    lista = autores.split(',')
    return lista


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

pesquisa = str(input("Entre com sua pesquisa\n"))

driver.set_page_load_timeout('10')
driver.get('https://www.semanticscholar.org/')
driver.find_element_by_name('q').send_keys(pesquisa)
driver.find_element_by_name('q').send_keys(Keys.ENTER)
delay(1)
listaDeArtigos = driver.find_elements_by_xpath("//article[@class='search-result']")
gerenciador = Gerenciador.Gerenciador(pesquisa)
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

for item in listaDeArtigos:
    titulo = item.find_element_by_xpath(".//a[@data-selenium-selector='title-link']").text

    listaDeAutoresHTML = item.find_elements_by_xpath(".//a[@class='author-list__link author-list__author-name']")
    lista_autores_artigo = []
    for temp in listaDeAutoresHTML:
        autor = temp.text
        link = temp.get_attribute('href')
        if len(lista_autores) == 0:
            temp = Autor.Autor(autor, link)
            lista_autores_artigo.append(temp)
            lista_autores.append(temp)
        else:
            criei = False
            for i in lista_autores:
                if autor == i.nome:
                    lista_autores_artigo.append(i)
                    lista_autores_artigo.sort()
                    criei = True
                    break
                if autor[0] > i.nome[0]:
                    temp = Autor.Autor(autor, link)
                    lista_autores_artigo.append(temp)
                    lista_autores_artigo.sort()
                    lista_autores.append(temp)
                    lista_autores.sort()
                    criei = True
                    break
            if criei is False:
                temp = Autor.Autor(autor, link)
                lista_autores_artigo.append(temp)
                lista_autores_artigo.sort()
                lista_autores.append(temp)
                lista_autores.sort()

    origem = None
    try:
        origem = item.find_element_by_xpath(".//li[@data-selenium-selector='venue-metadata']").text
    except:
        print('Artigo ' + titulo + " não possui dados de origem.")

    data = None
    try:
        data = item.find_element_by_xpath(".//li[@data-selenium-selector='paper-year']").text
    except:
        print('Artigo ' + titulo + " não possui dados de data de publicação.")

    influencia = None
    try:
        influencia = item.find_element_by_xpath(".//li[@data-selenium-selector='search-result-influential-citations']").text
    except:
        print('Artigo ' + titulo + " não possui dados de influencia.")

    velocidade = None
    try:
        velocidade = item.find_element_by_xpath(".//li[@data-selenium-selector='search-result-citation-velocity']").text
    except:
        print('Artigo ' + titulo + " não possui dados de velocidade de citação.")

    link = None
    try:
        link = item.find_element_by_xpath(".//a[@data-selenium-selector='paper-link']").get_attribute('href')
    except:
        print('Artigo ' + titulo + " não possui link.")

    novoArtigo = Artigo.Artigo(titulo, lista_autores_artigo, origem, data, influencia, velocidade, link)

    artigoRepetido = False
    if len(lista_artigos) == 0:
        lista_artigos.append(novoArtigo)
    else:
        criei = False
        for i in lista_artigos:
            if novoArtigo == i and novoArtigo.autores == i.autores:
                artigoRepetido = True
                break
            if novoArtigo.titulo[0] > i.titulo[0]:
                lista_artigos.append(novoArtigo)
                criei = True
                break
        if criei is False:
            lista_artigos.append(novoArtigo)

    if artigoRepetido is False:
        for autorTemp in lista_autores_artigo:
            autorTemp.addArtigo(novoArtigo)

gerenciador.saveArtigos(lista_artigos)
gerenciador.saveAutores(lista_autores)

delayFechar(3)
driver.quit()
