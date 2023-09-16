from appJar import gui
from UniteArticles import Merger
from SemanticScholarMetaCrawler import Crawler
from PDFDownloader import PDFDownloader
import os
import sys


def restart_program():
    """Restarts the current program."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


class GUI:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.app = gui('Semantic Scholar Crawler', '800x400')
        self.app.setGuiPadding(20, 20)
        self.app.setLocation('CENTER')
        self.app.setFont(16)
        self.search_phrase = ''
        self.input_pages = 0
        self.crawler = Crawler(self.root_directory)
        self.folders_text = ''
        self.folders_list = []
        self.single_or_merge = False
        self.merger = None

        self.crawler.gui = self

    def menus_pressed(self, menu):
        if menu == 'New Search':
            restart_program()
        if menu == "Close":
            self.app.stop()
        if menu == "Help":
            self.app.startSubWindow('Help', 'Help', True, )
            self.app.showSubWindow('Help')
            self.help_screen()
            self.app.stopSubWindow()
        if menu == "About":
            self.app.startSubWindow('About', 'About this program', True, )
            self.app.showSubWindow('About')
            self.about_screen()
            self.app.stopSubWindow()

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
        self.app.addLabel('Label_Pages_Quantity', 'Select how many articles you would like to search:', row=3)
        self.app.addScale('Quantity_scale', row=4)
        self.app.setScaleRange('Quantity_scale', 0, 100, 100)
        self.app.showScaleIntervals('Quantity_scale', 5)
        self.app.showScaleValue('Quantity_scale', True)
        self.app.setStretch('both')
        self.app.setSticky('se')
        self.app.addNamedButton('Next', 'Next1', self.press)

    def show_search_done_alert(self, time, quantity):
        self.app.stopAnimation('loading')
        self.app.hideImage('loading')
        self.app.infoBox('DONE', 'Search Completed in ' + str(time.seconds) + ' second(s) with ' +
                         quantity + ' articles successfully gathered.')
        self.app.setButtonState('Next2', 'normal')

    def show_download_done_alert(self, time, quantity):
        self.app.infoBox('DONE', 'Downloads Completed in ' + str(time.seconds) + ' second(s) with ' +
                         quantity + ' articles successfully downloaded.')
        self.app.setButtonState('Next3', 'normal')

    def show_saved_alert(self, saved_path):
        answer = self.app.yesNoBox('SAVED', 'Your search is saved at this location ' + saved_path +
                                   '.\nWould you like to end the program?')
        if answer:
            self.app.stop()

    def progress_bar(self):
        self.app.setStretch('column')
        self.app.setSticky('nwe')
        self.app.addLabel('progress_bar_label', 'Press "Start Search!"')
        self.app.setStretch('both')
        self.app.setSticky('nswe')
        
        self.app.setSticky('')

        self.app.addButton('Start Search!', self.press, column=0, row=2)
        self.app.setStretch('both')

        self.app.addImage("loading", "Images/book.gif")
        self.app.setAnimationSpeed("loading", 100)
        self.app.stopAnimation("loading")
        self.app.hideImage('loading')

        self.app.setSticky('se')
        self.app.addNamedButton('Next', 'Next2', self.press)
        self.app.setButtonState('Next2', 'disabled')

    def progress_bar2(self):
        self.app.setStretch('column')
        self.app.setSticky('nwe')
        self.app.addLabel('progress_bar_2_label', 'Press "Start Downloads!"')
        self.app.setStretch('both')
        self.app.setSticky('nswe')
        self.app.addMeter('progress_bar2', column=0, row=1)
        self.app.setMeterFill('progress_bar2', 'blue')
        self.app.setSticky('')
        self.app.addButton('Start Downloads!', self.press, column=0, row=2)
        self.app.setStretch('both')
        self.app.setSticky('se')
        self.app.addNamedButton('Skip', 'Skip_download', self.press, row=3)
        self.app.addNamedButton('Next', 'Next3', self.press, row=4)
        self.app.setButtonState('Next3', 'disabled')

    def save_menu(self):
        self.app.setStretch('column')
        self.app.setSticky('we')
        self.app.addLabel('Label_Save_options', 'How would you like your search to be ordered?')
        self.app.setSticky('w')
        self.app.addRadioButton('Save_option_radioButton', "Importance Rate (RECOMMENDED)")
        self.app.addRadioButton('Save_option_radioButton', "Number of Citations")
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

    def external_folders(self, list_folder):
        folders = list_folder.split("} {")

        for text_folder in folders:
            folder = text_folder.strip("{}")
            self.app.addListItem("folders_list", folder)
            self.folders_list.append(folder)

    def merge_searches(self):
        self.app.setStretch('both')
        self.app.setSticky('n')
        self.app.addLabel('Label_merge_searches',
                          'Drag and drop directories you would like to merge.', colspan=2)

        self.app.addListBox("folders_list", colspan=2)
        self.app.setListBoxDropTarget("folders_list", self.external_folders)
        self.app.setListBoxWidth("folders_list", 50)
        self.app.setStretch('both')
        self.app.setSticky('nsew')
        self.app.setStretch('')
        self.app.setSticky('s')

        self.app.addButton('Merge Searches', self.press, row=3)

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

        #self.app.startFrame('Downloading Progress')
        #self.progress_bar2()
        #self.app.stopFrame()

        self.app.startFrame('Saving Options')
        self.save_menu()
        self.app.stopFrame()

        self.app.startFrame('Merge Searches')
        self.merge_searches()
        self.app.stopFrame()

        self.app.stopFrameStack()

        self.app.firstFrame('Pages')
        self.app.go()

    def about_screen(self):
        self.app.addImage('Alphas', os.path.join(self.root_directory, 'Images', 'About.gif'))
        self.app.setSticky('n')
        self.app.addButton('Close', self.press)

    def help_screen(self):
        self.app.addWebLink('GitHub link for help!', 'https://github.com/EvertonCa/SeleniumSemanticScraper')
        self.app.addButton('Close!', self.press)

    def create_crawler(self):
        self.crawler.update_search_parameters(self.search_phrase, self.input_pages)
        self.crawler.start_search()

    def start_downloads(self):
        downloader = PDFDownloader(self.search_phrase, self.root_directory, self)
        downloader.start()

    def press(self, btn):
        if btn == "Next1" or btn == "Next2":
            self.search_phrase = self.app.getEntry('Entry_Search')
            self.input_pages = self.app.getScale('Quantity_scale')
            if self.input_pages == 0:
                self.app.errorBox('Error!', 'Selecting 0 articles will end up with a empty search!')
            else:
                self.app.nextFrame("Pages")

        elif btn == 'Next3':
            self.app.nextFrame("Pages")

        elif btn == 'Skip_download':
            self.app.nextFrame("Pages")

        elif btn == "Start Search!":
            self.app.setLabel('progress_bar_label', 'Getting Ready...')
            self.app.setButtonState('Start Search!', 'disabled')
            self.app.showImage('loading')
            self.app.startAnimation('loading')
            self.app.thread(self.create_crawler)

        elif btn == "Start Downloads!":
            self.app.setLabel('progress_bar_2_label', 'Getting Ready...')
            self.app.setButtonState('Start Downloads!', 'disabled')
            self.app.setButtonState('Skip_download', 'disabled')
            self.app.thread(self.start_downloads)

        elif btn == 'Save!':
            self.crawler.saves_excel(self.app.getRadioButton('Save_option_radioButton'))

        elif btn == 'New Search':
            self.app.selectFrame('Pages', 1)

        elif btn == 'Merge Old Searches':
            self.app.selectFrame('Pages', 4)

        elif btn == 'Merge Searches':
            self.single_or_merge = True
            self.merger = Merger(self.folders_list)
            self.app.selectFrame('Pages', 3)

        elif btn == 'Close':
            self.app.destroySubWindow('About')

        elif btn == 'Close!':
            self.app.destroySubWindow('Help')