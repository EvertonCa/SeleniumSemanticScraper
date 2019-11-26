import pickle
import os


class TextProcessing:
    def __init__(self, nome, root_directory, search_directory, pdfs_text_directory):
        self.root_directory = root_directory
        self.search_directory = search_directory
        self.pdfs_text_directory = pdfs_text_directory

        os.chdir(self.pdfs_text_directory)

        with open(nome + '.pkl', 'rb') as file_input:
            self.pdf = pickle.load(file_input)

        self.pdf_text = ''
        self.refactored_pdf_text = ''
        self.phrases = []

        self.pdf_to_text()
        self.refactor()

        os.chdir(self.root_directory)

    def pdf_to_text(self):
        for page in self.pdf.pages:
            self.pdf_text = self.pdf_text + page

    def refactor(self):
        self.refactored_pdf_text = self.pdf_text.replace('\n', ' ').replace('- ', '')
        self.phrases = self.refactored_pdf_text.split('. ')
