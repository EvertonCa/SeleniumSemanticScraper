import ExcelExporter
import Gerenciador
import os

search = str(input('Search Phrase: '))
gerenciador = Gerenciador.Gerenciador(search, os.getcwd())
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

leitor = ExcelExporter.ExcelExporter(search, True, os.getcwd())
print('Done')


