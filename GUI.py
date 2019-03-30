from appJar import gui
from SemanticScholarMetaCrawler import Crawler


class GUI:
    def __init__(self):
        self.app = gui('Semantic Scholar Crawler', '800x400')
        self.app.setGuiPadding(20, 20)
        self.app.setLocation('CENTER')
        self.app.setFont(16)
        self.search_phrase = ''
        self.input_pages = 0
        self.progress_bar_percentage = 0
        self.crawler = None

    def menus_pressed(self):
        pass

    def menus(self):
        file_menus = ["Open Search", "Save Search", "-", "Close"]
        about_menus = ["Help", "About"]
        self.app.addMenuList("File", file_menus, self.menus_pressed())
        self.app.addMenuList("About", about_menus, self.menus_pressed())

    def main_search(self):
        self.app.setStretch('none')
        self.app.setSticky('e')
        self.app.addLabel('Label_Search', 'Please enter your search phrase:', 0, 0)
        self.app.setSticky('we')
        self.app.setStretch('column')
        self.app.addEntry('Entry_Search', 0, 1)
        self.app.setStretch('none')
        self.app.setSticky('e')
        self.app.addLabel('Label_Pages_Quantity', 'Please select how many pages would you like to search:', 1, 0)
        self.app.setSticky('we')
        self.app.setStretch('column')
        self.app.addScale('Quantity_scale', column=1, row=1)
        self.app.setScaleRange('Quantity_scale', 0, 200, 10)
        self.app.showScaleIntervals('Quantity_scale', 25)
        self.app.showScaleValue('Quantity_scale', True)

    def update_progress_bar(self):
        self.app.setMeter('progress_bar', self.progress_bar_percentage)

    def show_done_alert(self):
        self.app.infoBox('DONE', 'Done!')

    def progress_bar(self):
        self.app.setStretch('column')
        self.app.setSticky('nwe')
        self.app.addLabel('progress_bar_label', 'Crawling...')
        self.app.setStretch('both')
        self.app.setSticky('nswe')
        self.app.addMeter('progress_bar', column=0, row=1)
        self.app.setMeterFill('progress_bar', 'blue')
        self.app.addButton('Start Search!', self.press, column=0, row=2)

    def main_page(self):
        self.menus()

        self.app.startFrameStack("Pages")

        self.app.startFrame('Search Menu')
        self.main_search()
        self.app.stopFrame()

        self.app.startFrame('Progress')
        self.progress_bar()
        self.app.stopFrame()

        self.app.startFrame('Saving Options')
        for i in range(5):
            self.app.addButton(str(i), None)
        self.app.stopFrame()

        self.app.stopFrameStack()

        self.app.setSticky('se')
        self.app.addButton('Next', self.press)
        self.app.firstFrame('Pages')
        self.app.go()

    def create_crawler(self):
        self.crawler = Crawler(self.search_phrase, self.input_pages)
        self.crawler.start_search()
        self.crawler.saves_excel()

    def press(self, btn):
        if btn == "Next":
            self.search_phrase = self.app.getEntry('Entry_Search')
            self.input_pages = self.app.getScale('Quantity_scale')
            if self.input_pages == 0:
                self.app.errorBox('Erro!', 'Selecting 0 pages will end up with a empty search!')
            else:
                self.app.nextFrame("Pages")

        elif btn == "Start Search!":
            self.create_crawler()
