class Artigo:
    def __init__(self, titulo, autores, publicado, data, influencia, velocidade, link, cite, bibtex):
        self.titulo = titulo
        self.autores = autores
        self.publicado_em = publicado
        self.data = data
        self.influencia = influencia
        self.velocidade = velocidade
        self.data_relativa = 0
        self.influencia_relativa = 0
        self.velocidade_relativa = 0
        self.total_factor = 0
        self.link = link
        self.cite = cite
        self.bibtex = bibtex

    def __lt__(self, other):
        return self.titulo < other

    def __le__(self, other):
        if isinstance(other, Artigo):
            return self.titulo <= other.titulo
        elif isinstance(other, (int, float, str)):
            return self.titulo <= other
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Artigo):
            return self.titulo >= other.titulo
        elif isinstance(other, (int, float, str)):
            return self.titulo >= other
        else:
            return NotImplemented

    def __eq__(self, other):
        return hash((self.titulo, self.link)) == hash((other.titulo, other.link))

    def __ne__(self, other):
        return self.titulo != other

    def __gt__(self, other):
        return self.titulo > other

    def __hash__(self):
        return hash((self.titulo, self.link))
