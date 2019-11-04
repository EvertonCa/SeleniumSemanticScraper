import os
import requests
from Gerenciador import Gerenciador


class PDFDownloader:
    def __init__(self, search, current_directory):
        self.search = search
        self.root_directory = current_directory
        self.manager = Gerenciador(self.search)
        self.list_articles = self.manager.loadArtigos()

        # saves pdf download directory
        self.pdf_directory = self.root_directory + '/Results/' + self.search + '/PDFs'

        os.chdir(self.root_directory + '/Results/' + self.search)

        if os.path.exists(self.pdf_directory):
            pass
        else:
            os.mkdir('PDFs')

        os.chdir(self.root_directory)

    def download_file(self, url, pdf_directory, name):
        local_filename = name + '.pdf'
        print('Downloading ' + local_filename + '\n')
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf_directory + '/' + local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return local_filename

    def iterate_articles(self):
        for article in self.list_articles:
            name = article.titulo
            link = article.link
            if 'pdf' in link:
                self.download_file(link, self.pdf_directory, name)
            else:
                pass

