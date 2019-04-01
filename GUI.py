from appJar import gui
from UniteArticles import Merger


class GUI:
    def __init__(self):
        self.app = gui('Semantic Scholar Crawler', '800x400')
        self.app.setGuiPadding(20, 20)
        self.app.setLocation('CENTER')
        self.app.setFont(16)
        self.search_phrase = ''
        self.input_pages = 0
        self.crawler = None
        self.alpha1 = 1
        self.alpha2 = 1
        self.alpha3 = 1
        self.folders_text = ''
        self.folders_list = []
        self.single_or_merge = False
        self.merger = None

    def menus_pressed(self, menu):
        if menu == 'New Search':
            pass

    def menus(self):
        file_menus = ["New Search", "-", "Close"]
        about_menus = ["Help", "About"]
        self.app.addMenuList("File", file_menus, self.menus_pressed)
        self.app.addMenuList("About", about_menus, self.menus_pressed)

    def main_search(self):
        self.app.setStretch('column')
        self.app.setSticky('we')
        self.app.addLabel('Label_Search', 'Enter your search phrase:', row=0)
        self.app.addEntry('Entry_Search', row=1)
        self.app.addLabel('label_space', '', row=2)
        self.app.addLabel('Label_Pages_Quantity', 'Select how many pages would you like to search:', row=3)
        self.app.addScale('Quantity_scale', row=4)
        self.app.setScaleRange('Quantity_scale', 0, 200, 1)
        self.app.showScaleIntervals('Quantity_scale', 25)
        self.app.showScaleValue('Quantity_scale', True)
        self.app.setStretch('both')
        self.app.setSticky('se')
        self.app.addNamedButton('Next', 'Next1', self.press)

    def show_search_done_alert(self, time, quantity):
        self.app.infoBox('DONE', 'Search Completed in ' + str(time.seconds) + ' second(s) with ' +
                         quantity + ' articles successfully gathered.')
        self.app.setButtonState('Next2', 'normal')

    def show_saved_alert(self, saved_path):
        self.app.infoBox('SAVED', 'Your search is saved at this location ' + saved_path)

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
        self.app.setStretch('both')
        self.app.setSticky('se')
        self.app.addNamedButton('Next', 'Next2', self.press)
        self.app.setButtonState('Next2', 'disabled')

    def save_menu(self):
        self.app.setStretch('column')
        self.app.setSticky('we')
        self.app.addLabel('Label_Save_options', 'How would you like your search to be ordered?')
        self.app.setSticky('w')
        self.app.addRadioButton('Save_option_radioButton', "Optimized Rating (RECOMMENDED)")
        self.app.addRadioButton('Save_option_radioButton', "Influence Factor")
        self.app.addRadioButton('Save_option_radioButton', "Citation Velocity")
        self.app.addRadioButton('Save_option_radioButton', "Newer Articles")
        self.app.addRadioButton('Save_option_radioButton', "Alphabetically, by Article's Title")
        self.app.setSticky('')
        self.app.addButton('Save!', self.press)

    def option_page(self):
        self.app.setStretch('column')
        self.app.addLabel('Label_Option_page', 'What would you like to do?')
        self.app.addLabel('spacing_label1', '')
        self.app.addLabel('spacing_label2', '')
        self.app.setSticky('nsew')
        self.app.addButton('New Search', self.press)
        self.app.addLabel('spacing_label3', '')
        self.app.addButton('Merge Old Searches', self.press)

    def alphas_selection(self):
        self.app.addLabel('Label_alphas_info', 'Your search will be saved using the equation below.')
        self.app.addImage('Alphas', 'Images/Alphas_Equation.gif')
        self.app.addLabel('Label_alphas_options',
                          'Enter the desired Alphas for your search. (For a basic order, enter 1 for all alphas)')
        self.app.addLabelEntry('Alpha1')
        self.app.addLabelEntry('Alpha2')
        self.app.addLabelEntry('Alpha3')
        self.app.addButton('OK!', self.press)

    def merge_searches(self):
        self.app.setStretch('both')
        self.app.setSticky('n')
        self.app.addLabel('Label_merge_searches',
                          'Select the searches directories you would like to merge.', colspan=2)
        self.app.setStretch('both')
        self.app.setSticky('nsew')
        self.app.addMessage('folders_merge', '', colspan=2)
        self.app.setMessageWidth('folders_merge', 600)
        self.app.setStretch('')
        self.app.setSticky('s')
        self.app.addButton('Select Folder', self.press, row=3, column=0)
        self.app.addButton('Merge Searches', self.press, row=3, column=1)

    def main_page(self):
        self.menus()

        self.app.startFrameStack("Pages")

        self.app.startFrame('Initial Option')
        self.option_page()
        self.app.stopFrame()

        self.app.startFrame('Search Menu')
        self.main_search()
        self.app.stopFrame()

        self.app.startFrame('Progress')
        self.progress_bar()
        self.app.stopFrame()

        self.app.startFrame('Saving Options')
        self.save_menu()
        self.app.stopFrame()

        self.app.startFrame('Merge Searches')
        self.merge_searches()
        self.app.stopFrame()

        self.app.stopFrameStack()

        self.app.firstFrame('Pages')
        self.app.go()

    def create_crawler(self):
        self.crawler.update_search_parameters(self.search_phrase, self.input_pages)
        self.crawler.start_search()

    def get_alphas_and_start(self):
        self.alpha1 = int(self.app.getEntry('Alpha1'))
        self.alpha2 = int(self.app.getEntry('Alpha2'))
        self.alpha3 = int(self.app.getEntry('Alpha3'))
        self.app.thread(self.crawler.saves_excel(self.app.getRadioButton('Save_option_radioButton')))
        self.app.destroySubWindow('Alphas')

    def press(self, btn):
        if btn == "Next1" or btn == "Next2":
            self.search_phrase = self.app.getEntry('Entry_Search')
            self.input_pages = self.app.getScale('Quantity_scale')
            if self.input_pages == 0:
                self.app.errorBox('Error!', 'Selecting 0 pages will end up with a empty search!')
            else:
                self.app.nextFrame("Pages")

        elif btn == "Start Search!":
            self.app.setLabel('progress_bar_label', 'Getting Ready...')
            self.app.setButtonState('Start Search!', 'disabled')
            self.app.thread(self.create_crawler)

        elif btn == 'Save!':
            if self.app.getRadioButton('Save_option_radioButton') == "Optimized Rating (RECOMMENDED)":
                self.app.startSubWindow('Alphas', 'Select Alphas', True, )
                self.app.showSubWindow('Alphas')
                self.alphas_selection()
                self.app.stopSubWindow()
            else:
                self.crawler.saves_excel(self.app.getRadioButton('Save_option_radioButton'), self.single_or_merge)

        elif btn == 'OK!':
            self.get_alphas_and_start()

        elif btn == 'New Search':
            self.app.selectFrame('Pages', 1)

        elif btn == 'Merge Old Searches':
            self.app.selectFrame('Pages', 4)

        elif btn == 'Select Folder':
            text = self.app.directoryBox('Select Folder')
            self.folders_list.append(text)
            self.folders_text += text + '\n'
            self.app.setMessage('folders_merge', self.folders_text)

        elif btn == 'Merge Searches':
            self.single_or_merge = True
            self.merger = Merger(self.folders_list)
            self.app.selectFrame('Pages', 3)

