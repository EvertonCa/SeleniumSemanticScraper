from appJar import gui


class GUI:
    def __init__(self):
        self.app = gui('Semantic Scholar Crawler', '800x400')
        self.app.setGuiPadding(20, 20)
        self.app.setLocation('CENTER')
        self.app.setFont(16)

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
        self.app.addScale('Quantity', column=1, row=1)
        self.app.setScaleRange('Quantity', 0, 200, 10)
        self.app.showScaleIntervals('Quantity', 25)
        self.app.showScaleValue('Quantity', True)

    def main_page(self):
        self.menus()

        self.app.startFrameStack("Pages")

        self.app.startFrame('Search Menu')
        self.main_search()
        self.app.stopFrame()

        self.app.startFrame('Progress')
        for i in range(5):
            self.app.addEntry("e" + str(i))
        self.app.stopFrame()

        self.app.startFrame('Saving Options')
        for i in range(5):
            self.app.addButton(str(i), None)
        self.app.stopFrame()

        self.app.stopFrameStack()

        self.app.setSticky('e')
        self.app.addButtons(['Next'], self.press)
        self.app.firstFrame('Pages')
        self.app.go()

    def press(self, btn):
        if btn == "FIRST":
            self.app.firstFrame("Pages")
        elif btn == "NEXT":
            self.app.nextFrame("Pages")
        elif btn == "PREV":
            self.app.prevFrame("Pages")
        elif btn == "LAST":
            self.app.lastFrame("Pages")


gui = GUI()
gui.main_page()
