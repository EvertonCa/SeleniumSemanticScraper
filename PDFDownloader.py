import os
import shutil
import Timer
import pandas as pd
import platform
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
            if self.check_download_started():
                return True
            else:
                return False
        else:
            try:
                # wait to check it the site is IEEE, then tries to download it
                waitelement = WebDriverWait(self.driver, 2). \
                    until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'ieeexplore')]")))

                new_link = self.driver.find_element_by_xpath("//iframe[contains(@src,'ieeexplore')]").get_attribute("src")

                self.driver.get(new_link)

                if self.check_download_started():
                    return True
                else:
                    return False

            except:
                return False

    # waits 3 seconds to see if any download has started. If yes, returns True.
    def check_download_started(self):
        name = os.listdir(self.temp_folder)

        for i in range(3):
            if len(name) == 0:
                name = os.listdir(self.temp_folder)
                print(name)
                print(' FOR')
                time.sleep(1)
            else:
                return True

        return False

    def check_downloaded(self):
        # items in temp folder
        name = os.listdir(self.temp_folder)

        # loop until folder is not empty
        while True:
            if len(name) == 0:
                name = os.listdir(self.temp_folder)
            else:
                break
        print(name)
        print('entre')
        # loop until .crdownload temp file appears
        while True:
            if name[0].endswith('.crdownload'):
                name = name[0]
                break
            else:
                name = os.listdir(self.temp_folder)

        print(name)

        # loop until .crdownload file is replaced with the finished .pdf file
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

        for _ in titles:
            file = open('DownloadLog.txt', 'a')
            #self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar2', ((100 * index_progress_bar) / size_list))
            short_article_name = (str(titles[index_progress_bar - 1]).replace('\'', '').replace('-', ' ')
                                  .replace(':', '').replace(';', '')).split(' ')
            if short_article_name[0] != 'A' and short_article_name[0] != 'a' and short_article_name[0] != 'An' and \
            short_article_name[0] != 'an' and short_article_name[0] != 'The' and short_article_name[0] != 'the':
                short_article_name = short_article_name[0]
            else:
                short_article_name = short_article_name[1]

            new_name = str(year[index_progress_bar - 1]) + '-' + (((str(authors[index_progress_bar - 1])
                        .split(', '))[0]).split(' '))[-1] + '-' + short_article_name

            link = str(links[index_progress_bar - 1])
            index_progress_bar += 1

            resp = self.download_file(link)

            if resp is False:
                file.write('FAILED TO DOWNLOAD: ' + new_name
                           + ' Link: ' + link + '\n')
            else:
                old_name = self.check_downloaded()
                self.downloaded_files_quant += 1
                self.rename_and_move(old_name, new_name + '.pdf')
                file.write(str(self.downloaded_files_quant) + ' SUCCESSFULLY DOWNLOADED: ' + new_name + '\n')
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
