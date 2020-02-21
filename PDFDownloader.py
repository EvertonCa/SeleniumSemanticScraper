import os
import shutil
import Timer
import pandas as pd
import platform
import time
from selenium import webdriver


class PDFDownloader:
    def __init__(self, current_directory):
        self.root_directory = current_directory
        self.list_articles = None
        #self.gui = gui
        self.downloaded_files_quant = 0

        # saves pdf download directory
        self.pdf_directory = os.path.join(self.root_directory, 'Results', 'Merged Search', 'PDFs')

        self.temp_folder = os.path.join(self.root_directory, 'Results', 'Merged Search', 'Temp')

        os.chdir(os.path.join(self.root_directory, 'Results', 'Merged Search'))

        if os.path.exists(self.pdf_directory):
            pass
        else:
            os.mkdir('PDFs')

        if os.path.exists(self.temp_folder):
            pass
        else:
            os.mkdir('Temp')

        self.current_platform = platform.system()
        if self.current_platform == 'Darwin':
            self.directory_chromedriver = os.path.join(self.root_directory, 'ChromeDriver', 'ChromeDriverMac')
        elif self.current_platform == 'Windows':
            self.directory_chromedriver = os.path.join(self.root_directory, 'ChromeDriver', 'ChromeDriverWin.exe')
        else:
            self.directory_chromedriver = os.path.join(self.root_directory, 'ChromeDriver', 'ChromeDriverLin')

        self.options = webdriver.ChromeOptions()

        self.options.add_experimental_option("prefs", {
            "download.default_directory": self.temp_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(self.directory_chromedriver, options=self.options)

    def rename_and_move(self, old, new):
        os.rename(os.path.join(self.temp_folder, old), os.path.join(self.temp_folder, new))
        shutil.move(os.path.join(self.temp_folder, new), os.path.join(self.pdf_directory, new))

    def download_file(self, url):
        self.driver.get(url)

        if 'pdf' in url:
            return True
        else:
            try:
                # if the site is IEEE, it can download if in the right network
                new_link = self.driver.find_element_by_xpath("//iframe[contains(@src,'pdf')]").get_attribute("src")
                self.driver.get(new_link)
                return True
            except:
                return False

    def check_downloaded(self):
        name = os.listdir(self.temp_folder)
        while True:
            if len(name) == 0:
                time.sleep(1)
                name = os.listdir(self.temp_folder)
            else:
                break
        name = name[0]
        while True:
            if os.path.exists(os.path.join(self.temp_folder, name)) is False:
                file_name = os.listdir(self.temp_folder)
                file_name = file_name[0]
                return file_name
            time.sleep(1)

    def iterate_articles(self):
        start_time = Timer.timeNow()
        index_progress_bar = 1

        excel = pd.read_excel('Download.xlsx', sheet_name='ARTICLES')

        titles = excel['Title']
        authors = excel['Authors']
        links = excel['Article Link']
        year = excel['Publication Year']
        size_list = excel['Title'].size

        for temp in titles:
            file = open('DownloadLog.txt', 'a')
            #self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar2', ((100 * index_progress_bar) / size_list))
            new_name = str(year[index_progress_bar - 1]) + '-' + (((str(authors[index_progress_bar - 1])
                            .split(', '))[0]).split(' '))[-1] + '-' + ((str(titles[index_progress_bar - 1])
                            .replace('A', '').replace('a', '').replace('An', '').replace('an', '').replace('The', '')
                            .replace('the', '').replace('\'', '').replace('-', ' ')).split(' '))[0]
            link = str(links[index_progress_bar - 1])
            index_progress_bar += 1

            resp = self.download_file(link)

            if resp is False:
                file.write(new_name + 'FAILED TO DOWNLOAD: '
                           + 'Link: ' + link + '\n')
            else:
                old_name = self.check_downloaded()
                self.downloaded_files_quant += 1
                self.rename_and_move(old_name, new_name + '.pdf')
                file.write(str(self.downloaded_files_quant) + ' ' + new_name + 'SUCCESSFULLY DOWNLOADED' + '\n')
            file.close()

        shutil.rmtree(self.temp_folder)
        self.driver.quit()
        end_time = Timer.timeNow()
        #self.gui.show_download_done_alert(Timer.totalTime(start_time, end_time), str(self.downloaded_files_quant))

    def start(self):
        self.gui.app.queueFunction(self.gui.app.setLabel, 'progress_bar_2_label', 'Downloading available .pdf files')
        self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar2', 0)

        self.iterate_articles()


if __name__ == "__main__":
    down = PDFDownloader(os.getcwd())
    down.iterate_articles()
