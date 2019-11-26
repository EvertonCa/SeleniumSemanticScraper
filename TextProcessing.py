import pickle
import os


class TextProcessing:
    def __init__(self, nome):
        os.chdir(os.path.join(os.getcwd(), 'Results/Neural Networks/PDFs/PDFsToText'))
        with open(nome + '.pkl', 'rb') as file_input:
            self.pdf = pickle.load(file_input)
        self.pdf_text = ''
        self.refactored_pdf_text = ''
        self.phrases = []

    def pdf_to_text(self):
        for page in self.pdf.pages:
            self.pdf_text = self.pdf_text + page

    def refactor(self):
        self.refactored_pdf_text = self.pdf_text.replace('\n', ' ').replace('- ', '')
        self.phrases = self.refactored_pdf_text.split('. ')

teste = TextProcessing('Artificial Neural Networks- A Tutorial')
teste.pdf_to_text()
teste.refactor()
print('Done')