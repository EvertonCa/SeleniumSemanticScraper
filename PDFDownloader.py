import os
import requests
from Gerenciador import Gerenciador
import Timer


class PDFDownloader:
    def __init__(self, search, current_directory, gui):
        self.search = search
        self.root_directory = current_directory
        self.manager = Gerenciador(self.search, self.root_directory)
        self.list_articles = self.manager.loadArtigos()
        self.gui = gui
        self.downloaded_files_quant = 0

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
        start_time = Timer.timeNow()
        index_progress_bar = 1
        size_list = len(self.list_articles)
        for article in self.list_articles:
            self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar2', ((100 * index_progress_bar) / size_list))
            index_progress_bar += 1
            name = article.titulo
            link = article.link
            if 'pdf' in link:
                self.download_file(link, self.pdf_directory, name)
                self.downloaded_files_quant += 1
            else:
                pass

        end_time = Timer.timeNow()
        self.gui.show_download_done_alert(Timer.totalTime(start_time, end_time), str(self.downloaded_files_quant))

    def start(self):
        self.gui.app.queueFunction(self.gui.app.setLabel, 'progress_bar_2_label', 'Downloading Available PDFs Files ')
        self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar2', 0)

        self.iterate_articles()
