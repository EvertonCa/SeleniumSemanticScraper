import os
import pickle
from pathlib import Path


class Gerenciador:
    def __init__(self, palavraChave):
        self.diretorio_atual = os.getcwd()
        self.diretorio_files = self.diretorio_atual + '/Files/'
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
            os.mkdir('Files')
        diretorio_com_palavra_chave = self.diretorio_files + palavraChave + '/'
        if os.path.exists(diretorio_com_palavra_chave):
            pass
        else:
            os.chdir(self.diretorio_files)
            os.mkdir(palavraChave)
        self.arquivo_autores = diretorio_com_palavra_chave + 'Autores.pkl'
        self.arquivo_artigos = diretorio_com_palavra_chave + 'Artigos.pkl'
        caminho_autores = Path(diretorio_com_palavra_chave + 'Autores.pkl')
        caminho_artigos = Path(diretorio_com_palavra_chave + 'Artigos.pkl')
        if caminho_artigos.is_file() is False:
            self.inicializaArtigos()
            print('Arquivo Artigos.pkl criado!')
        if caminho_autores.is_file() is False:
            self.inicializaAutores()
            print('Arquivo Autores.pkl criado!')

