import os
import requests


class PDFDownloader:
    def __init__(self, search, link, current_directory):
        self.search = search
        self.link = link
        self.current_directory = current_directory

        # saves pdf download directory
        self.pdf_directory = self.current_directory + '/Results/' + self.search + '/PDFs'

        os.chdir(self.current_directory + '/Results/' + self.search)

        if os.path.exists(self.pdf_directory):
            pass
        else:
            os.mkdir('PDFs')

        os.chdir(self.current_directory)

        self.download_file(self.link, self.pdf_directory)

    def download_file(self, url, pdf_directory):
        local_filename = 'Teste.pdf'
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(pdf_directory + '/' + local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return local_filename


teste = PDFDownloader('neural networks', "https://pdfs.semanticscholar.org/4b80/89bc9b49f84de43acc2eb8900035f7d492b2."
                                         "pdf?_ga=2.82862294.1789955955.1571429546-391360297.1571429546", os.getcwd())
