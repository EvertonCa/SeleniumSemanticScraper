import Gerenciador


class Leitor():
    def __init__(self, palavraChave):
        gerenciador = Gerenciador.Gerenciador(palavraChave)
        self.listaDeArtigos = gerenciador.loadArtigos()
        self.listaDeAutores = gerenciador.loadAutores()


leitor = Leitor('Machine Learning')
print('Pronto')

