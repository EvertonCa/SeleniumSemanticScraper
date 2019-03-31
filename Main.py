from GUI import GUI
from SemanticScholarMetaCrawler import Crawler

# start Crawler
crawler = Crawler()

# start GUI
gui = GUI()
gui.crawler = crawler
crawler.gui = gui
gui.main_page()