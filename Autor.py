class Autor:
    def __init__(self, nome, link):
        self.nome = nome
        self.artigos = []
        self.link = link

    def addArtigo(self, artigo):
        self.artigos.append(artigo)
        self.artigos.sort()

    def __lt__(self, other):
        return self.nome < other

    def __le__(self, other):
        if isinstance(other, Autor):
            return self.nome <= other.nome
        elif isinstance(other, (int, float, str)):
            return self.nome <= other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Autor):
            return self.nome >= other.nome
        elif isinstance(other, (int, float, str)):
            return self.nome >= other
        else:
            return NotImplemented

    def __eq__(self, other):
        return self.nome == other

    def __ne__(self, other):
        return self.nome != other

    def __gt__(self, other):
        return self.nome > other