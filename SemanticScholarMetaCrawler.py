from selenium import webdriver
import Gerenciador
import Autor
import Artigo
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import platform
import ExcelExporter
import sys

sys.setrecursionlimit(5000)


def delayFechar(tempo):
    for ind in range(tempo, 0, -1):
        print("Browser fechando em " + str(ind) + " segundos")
        time.sleep(1)


def delay(tempo):
    time.sleep(tempo)


def retornaListaAutores(autores):
    lista = autores.split(',')
    return lista


options = Options()

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

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')

pesquisa = str(input("Entre com sua pesquisa:\n"))
paginas = int(input("Quantas páginas gostaria de pesquisar? Cada página retorna por volta de 30 resultados.\n"))

gerenciador = Gerenciador.Gerenciador(pesquisa)
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()
normal = False
lastFiveYears = False
litReviews = False

driver = webdriver.Chrome(diretorio_chromedriver, chrome_options=options)
for k in range(0, 3):
    driver.get('https://www.semanticscholar.org/')

    try:
        waitelement = WebDriverWait(driver, 20).\
            until(EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Field of study filter']")))
    except TimeoutError:
        print("PAGINA NÃO CARREGOU!")

    driver.find_element_by_name('q').send_keys(pesquisa)
    driver.find_element_by_name('q').send_keys(Keys.ENTER)

    try:
        waitelement = WebDriverWait(driver, 20).\
            until(EC.presence_of_element_located((By.XPATH, "//button[@data-selenium-selector='more-search-filters']")))
    except TimeoutError:
        print("PAGINA NÃO CARREGOU!")

    if normal is False:
        normal = True
    else:
        if lastFiveYears is False:
            element = driver.find_element_by_xpath("//button[@data-selenium-selector='last-five-years-filter-button']")
            driver.execute_script('arguments[0].click()', element)
            lastFiveYears = True
        else:
            if litReviews is False:
                element = driver.find_element_by_xpath("//button[@data-selenium-selector='reviews-filter-button']")
                driver.execute_script('arguments[0].click()', element)
                litReviews = True
            else:
                pass

    for pag in range(0, paginas):
        while True:
            try:
                element = driver.find_element_by_xpath("//div[@class='result-page is-filtering']")
            except:
                break

        listaDeArtigos = driver.find_elements_by_xpath("//article[@class='search-result']")

        for item in listaDeArtigos:
            titulo = item.find_element_by_xpath(".//a[@data-selenium-selector='title-link']").text

            listaDeAutoresHTML = item.find_elements_by_xpath(
                ".//a[@class='author-list__link author-list__author-name']")

            autoresSemLink = None
            try:
                autoresSemLink = item.find_elements_by_xpath(".//span[@class='author-list__author-name']")
            except:
                pass

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
                        if autor[0] < i.nome[0]:
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

            if autoresSemLink is not None:
                for temp in autoresSemLink:
                    autor = temp.text
                    if len(lista_autores) == 0:
                        temp = Autor.Autor(autor, None)
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
                            if autor[0] < i.nome[0]:
                                temp = Autor.Autor(autor, None)
                                lista_autores_artigo.append(temp)
                                lista_autores_artigo.sort()
                                lista_autores.append(temp)
                                lista_autores.sort()
                                criei = True
                                break
                        if criei is False:
                            temp = Autor.Autor(autor, None)
                            lista_autores_artigo.append(temp)
                            lista_autores_artigo.sort()
                            lista_autores.append(temp)
                            lista_autores.sort()

            origem = '-'
            try:
                origem = item.find_element_by_xpath(".//li[@data-selenium-selector='venue-metadata']").text
            except:
                print('Artigo ' + titulo + " não possui dados de origem.")

            data = '-'
            try:
                data = item.find_element_by_xpath(".//li[@data-selenium-selector='paper-year']").text
            except:
                print('Artigo ' + titulo + " não possui dados de data de publicação.")

            influencia = '0'
            try:
                influencia = item.find_element_by_xpath(
                    ".//li[@data-selenium-selector='search-result-influential-citations']").text
            except:
                print('Artigo ' + titulo + " não possui dados de influencia.")

            velocidade = '0'
            try:
                velocidade = item.find_element_by_xpath(
                    ".//li[@data-selenium-selector='search-result-citation-velocity']").text
            except:
                print('Artigo ' + titulo + " não possui dados de velocidade de citação.")

            link = '-'
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
                    if novoArtigo.link == i.link and novoArtigo.titulo == i.titulo:
                        artigoRepetido = True
                        break
                    if novoArtigo.titulo[0] < i.titulo[0]:
                        lista_artigos.append(novoArtigo)
                        lista_artigos.sort()
                        criei = True
                        break
                if criei is False and artigoRepetido is False:
                    lista_artigos.append(novoArtigo)
                    lista_artigos.sort()

            if artigoRepetido is False:
                for autorTemp in lista_autores_artigo:
                    autorTemp.addArtigo(novoArtigo)

        print('~~~~ PÁGINA ' + str(pag+1) + ' FINALIZADA COM SUCESSO ~~~~')

        try:
            element = driver.find_element_by_xpath("//a[@data-selenium-selector='next-page']")
            driver.execute_script('arguments[0].click()', element)
        except:
            print("ASSUNTO NÃO POSSUI MAIS PAGINAS DE PESQUISA!")
            break

print('~~~~ PESQUISA FINALIZADA COM SUCESSO ~~~~')
gerenciador.saveArtigos(lista_artigos)
gerenciador.saveAutores(lista_autores)
driver.quit()
os.chdir(diretorio_atual)
excelExporter = ExcelExporter.ExcelExporter(pesquisa)
print('~~~~ EXCEL SALVO COM SUCESSO ~~~~')
