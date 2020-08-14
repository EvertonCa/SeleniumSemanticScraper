class Artigo:
    def __init__(self, titulo, autores, publicado, data, citacoes, link, cite, bibtex, synopsis):
        self.titulo = titulo
        self.autores = autores
        self.publicado_em = publicado
        self.data = data
        self.citacoes = citacoes
        self.data_relativa = 0
        self.citacoes_relativa = 0
        self.cite_label = 0
        self.total_factor = 0
        self.impact_factor = " "
        self.link = link
        self.cite = cite
        self.bibtex = bibtex
        self.synopsis = synopsis

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
