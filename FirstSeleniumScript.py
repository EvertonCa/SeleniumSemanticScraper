from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

print("Entre com as palavras chave para a pesquisa:")
palavras_chave = str(input())
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
for i in range(2, 11):
    temp = inicio_link + meio_link + fim_link_outras_comeco + str(i) + fim_link_outras_fim
    lista_de_urls.append(temp)

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": r"/Users/evertoncardoso/Developer/PycharmProjects/SeleniumSemantic/pdfs",
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "plugins.always_open_pdf_externally": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome('/Users/evertoncardoso/Developer/PycharmProjects/SeleniumSemantic/chromedriver', chrome_options=options)

for url in lista_de_urls:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(50)
    lista_de_pdfs = driver.find_elements_by_partial_link_text("PDF")
    for pdf in lista_de_pdfs:
        pdf.click()
driver.quit()
