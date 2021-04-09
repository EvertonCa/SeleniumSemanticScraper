import os
import pickle
from pathlib import Path


class Gerenciador:
    def __init__(self, palavraChave, root_directory):
        self.root_directory = root_directory
        self.diretorio_files = os.path.join(self.root_directory, 'Results')
        self.arquivo_autores = ''
        self.arquivo_artigos = ''
        self.inicializaPrograma(palavraChave)

    def loadAutores(self):
        with open(self.arquivo_autores, 'rb') as file_input:
            lista_autores = pickle.load(file_input)
        return lista_autores

    def loadArtigos(self):
        with open(self.arquivo_artigos, 'rb') as file_input:
            lista_artigos = pickle.load(file_input)
        return lista_artigos

    def saveAutores(self, lista_autores):
        lista_autores.sort()
        with open(self.arquivo_autores, 'wb') as file_output:
            pickle.dump(lista_autores, file_output, -1)

    def saveArtigos(self, lista_artigos):
        lista_artigos.sort()
        with open(self.arquivo_artigos, 'wb') as file_output:
            pickle.dump(lista_artigos, file_output, -1)

    def inicializaAutores(self):
        lista_autores = []
        with open(self.arquivo_autores, 'wb') as file_output:
            pickle.dump(lista_autores, file_output, -1)

    def inicializaArtigos(self):
        lista_artigos = []
        with open(self.arquivo_artigos, 'wb') as file_output:
            pickle.dump(lista_artigos, file_output, -1)

    def inicializaPrograma(self, palavraChave):
        if os.path.exists(self.diretorio_files):
            pass
        else:
            os.mkdir('Results')
        diretorio_com_palavra_chave = os.path.join(self.diretorio_files, palavraChave)
        if os.path.exists(diretorio_com_palavra_chave):
            pass
        else:
            os.chdir(self.diretorio_files)
            os.mkdir(palavraChave)
        self.arquivo_autores = os.path.join(diretorio_com_palavra_chave, 'Authors.pkl')
        self.arquivo_artigos = os.path.join(diretorio_com_palavra_chave, 'Articles.pkl')
        caminho_autores = Path(self.arquivo_autores)
        caminho_artigos = Path(self.arquivo_artigos)
        if caminho_artigos.is_file() is False:
            self.inicializaArtigos()
        if caminho_autores.is_file() is False:
            self.inicializaAutores()