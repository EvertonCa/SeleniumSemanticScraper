import ExcelExporter
import Gerenciador

search = str(input('Search Phrase:'))
gerenciador = Gerenciador.Gerenciador(search)
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

leitor = ExcelExporter.ExcelExporter(search, True)
print('Done')


