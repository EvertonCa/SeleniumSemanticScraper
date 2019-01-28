import ExcelExporter
import Gerenciador

gerenciador = Gerenciador.Gerenciador('Artificial Inteligence')
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

leitor = ExcelExporter.ExcelExporter('Artificial Inteligence')
print('Pronto')


