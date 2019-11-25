class PDF:
    def __init__(self, name):
        self.pages = []
        self.name = name

    def add_page(self, page):
        self.pages.append(page)
