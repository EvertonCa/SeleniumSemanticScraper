from GUI import GUI
from SemanticScholarMetaCrawler import Crawler


class Main:
    def __init__(self):
        # start Crawler
        self.crawler = Crawler()

        # start GUI
        self.gui = GUI()
        self.gui.crawler = self.crawler
        self.crawler.gui = self.gui
        self.gui.main_page()



main = Main()

