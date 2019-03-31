from appJar import gui


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
        self.app.setStretch('column')
        self.app.setSticky('we')
        self.app.addLabel('Label_Search', 'Enter your search phrase:', row=0)
        self.app.addEntry('Entry_Search', row=1)
        self.app.addLabel('label_space', '', row=2)
        self.app.addLabel('Label_Pages_Quantity', 'Select how many pages would you like to search:',
                          row=3)
        self.app.addScale('Quantity_scale', row=4)
        self.app.setScaleRange('Quantity_scale', 0, 200, 1)
        self.app.showScaleIntervals('Quantity_scale', 25)
        self.app.showScaleValue('Quantity_scale', True)

    def update_progress_bar(self):
        self.app.setMeter('progress_bar', self.progress_bar_percentage)

    def show_done_alert(self, time, quantity):
        self.app.infoBox('DONE', 'Search Completed in ' + str(time.seconds) + ' second(s) with ' +
                         quantity + ' articles successfully gathered.')

    def progress_bar(self):
        self.app.setStretch('column')
        self.app.setSticky('nwe')
        self.app.addLabel('progress_bar_label', 'Press "Start Search!"')
        self.app.setStretch('both')
        self.app.setSticky('nswe')
        self.app.addMeter('progress_bar', column=0, row=1)
        self.app.setMeterFill('progress_bar', 'gray')
        self.app.setSticky('')
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
        self.crawler.update_search_parameters(self.search_phrase, self.input_pages)
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
            self.app.setLabel('progress_bar_label', 'Getting Ready...')
            self.app.thread(self.create_crawler)
