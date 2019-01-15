import ExcelExporter
import Gerenciador

gerenciador = Gerenciador.Gerenciador('Texture Analysis Methods')
lista_autores = gerenciador.loadAutores()
lista_artigos = gerenciador.loadArtigos()

# leitor = ExcelExporter.ExcelExporter('CNN Object Detection')
print('Pronto')


