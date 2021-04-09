from GUI import GUI
import os


class Main:
    def __init__(self):
        self.root_directory = os.getcwd()
        # start GUI
        self.gui = GUI(self.root_directory)
        self.gui.main_page()


if __name__ == "__main__":
    main = Main()