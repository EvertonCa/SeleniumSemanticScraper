import ExcelExporter
import Gerenciador

gerenciador = Gerenciador.Gerenciador('AI')
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

leitor = ExcelExporter.ExcelExporter('AI')
print('Pronto')


