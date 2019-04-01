from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import Gerenciador
import Autor
import Artigo
import os
import platform
import ExcelExporter
import sys
import Timer


class Crawler:
    def __init__(self):
        # increase the recursion limit to handle very large searches
        sys.setrecursionlimit(5000)

        # options handler for Google Chrome
        self.options = Options()

        # saves current directory in a string
        self.current_directory = os.getcwd()

        # saves current platform in a string
        self.current_platform = platform.system()

        self.directory_chromedriver = ''
        if self.current_platform == 'Darwin':
            self.directory_chromedriver = self.current_directory + '/ChromeDriver/ChromeDriverMac'
        elif self.current_platform == 'Windows':
            self.directory_chromedriver = self.current_directory + '/ChromeDriver/ChromeDriverWin.exe'
        else:
            self.directory_chromedriver = self.current_directory + '/ChromeDriver/ChromeDriverLin'

        # sets Chrome to run Headless (without showing the navigator window while running)
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')

        self.start_time = Timer.timeNow()
        self.end_time = Timer.timeNow()

        self.manager = None
        self.list_authors = []
        self.list_articles = []

        self.input_search = ''
        self.input_pages = ''

        self.gui = None

        self.index_progress_bar = 1

    def update_search_parameters(self, input_search, input_pages):
        self.input_search = input_search
        self.input_pages = input_pages

    # extract the type of the article from the BibText cite text and returns it as a single word string
    def return_type_cite(self, string_cite):
        list_cite = string_cite.split('{')
        type_cite = list_cite[0][1:]
        return type_cite

    def start_search(self):
        self.start_time = Timer.timeNow()

        # loads files for the inputted search if they exist, otherwise, the files are created
        self.manager = Gerenciador.Gerenciador(self.input_search)
        self.list_authors = self.manager.loadAutores()
        self.list_articles = self.manager.loadArtigos()

        # booleans for setting the type of search
        normal = False
        lastFiveYears = False
        litReviews = False

        # creates a webdriver instance
        driver = webdriver.Chrome(self.directory_chromedriver, chrome_options=self.options)

        # runs the following code 3 times, one for each type os search
        for k in range(0, 3):
            # label gui
            self.gui.app.queueFunction(self.gui.app.setLabel, 'progress_bar_label', 'Crawling with '
                                       + str(k+1) + '/3 parameter...')
            self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar', 0)

            # access Semantic Scholar main page
            driver.get('https://www.semanticscholar.org/')

            # waits for the page to load, searching for the Field of Study filter to be enabled
            try:
                waitelement = WebDriverWait(driver, 20). \
                    until(EC.presence_of_element_located((By.XPATH, "//select[@aria-label='Field of study filter']")))
            except TimeoutError:
                print("~~~~ PAGE DID NOT LOAD! ~~~~")

            # dismiss the popup that asks to allow cookies, if it shows up
            try:
                driver.find_element_by_xpath(
                    "//div[@class='copyright-banner__dismiss-btn button button--secondary']").click()
            except:
                pass

            # input the desired search phrase in the input box and hits ENTER
            driver.find_element_by_name('q').send_keys(self.input_search)
            driver.find_element_by_name('q').send_keys(Keys.ENTER)

            # waits for the page to load
            try:
                waitelement = WebDriverWait(driver, 20). \
                    until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@data-selenium-selector='more-search-filters']")))
            except TimeoutError:
                print("~~~~ PAGE DID NOT LOAD! ~~~~")

            # tests which type of search has been done and sets the correct one
            if normal is False:
                normal = True
            else:
                if lastFiveYears is False:
                    element = driver.find_element_by_xpath(
                        "//button[@data-selenium-selector='last-five-years-filter-button']")
                    driver.execute_script('arguments[0].click()', element)
                    lastFiveYears = True
                else:
                    if litReviews is False:
                        element = driver.find_element_by_xpath(
                            "//button[@data-selenium-selector='reviews-filter-button']")
                        driver.execute_script('arguments[0].click()', element)
                        litReviews = True
                    else:
                        pass

            # runs the code for the amount of pages desired
            self.index_progress_bar = 1
            for pag in range(0, self.input_pages):
                # progress bar
                self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar',
                                           (100 * self.index_progress_bar)/self.input_pages)

                self.index_progress_bar += 1

                # waits for the page to load
                while True:
                    try:
                        element = driver.find_element_by_xpath("//div[@class='result-page is-filtering']")
                    except:
                        break

                # searches for the articles in the page and saves them in a list
                list_articles_in_page = driver.find_elements_by_xpath("//article[@class='search-result']")

                # iterates over each article in the articles list
                for item in list_articles_in_page:
                    # saves the article title as a string
                    title = item.find_element_by_xpath(".//a[@data-selenium-selector='title-link']").text

                    # saves all authors with a html link to their pages in a list
                    list_authors_html_link = item.find_elements_by_xpath(
                        ".//a[@class='author-list__link author-list__author-name']")

                    # saves all authors without a html link to their pages in a list
                    list_authors_without_html_link = None
                    try:
                        list_authors_without_html_link = item.find_elements_by_xpath(
                            ".//span[@class='author-list__author-name']")
                    except:
                        pass

                    # creates a list of the authors for the article
                    list_authors_in_article = []

                    # iterates over each author in the list with html link
                    for temp in list_authors_html_link:
                        # saves the author name as a string
                        author = temp.text
                        # saves the author page html link as a string
                        link = temp.get_attribute('href')
                        # checks it the author already exists and if not, creates it and adds it to the authors list
                        if len(self.list_authors) == 0:
                            temp = Autor.Autor(author, link)
                            list_authors_in_article.append(temp)
                            self.list_authors.append(temp)
                        else:
                            created = False
                            for i in self.list_authors:
                                if author == i.nome:
                                    list_authors_in_article.append(i)
                                    list_authors_in_article.sort()
                                    created = True
                                    break
                                if author[0] < i.nome[0]:
                                    temp = Autor.Autor(author, link)
                                    list_authors_in_article.append(temp)
                                    list_authors_in_article.sort()
                                    self.list_authors.append(temp)
                                    self.list_authors.sort()
                                    created = True
                                    break
                            if created is False:
                                temp = Autor.Autor(author, link)
                                list_authors_in_article.append(temp)
                                list_authors_in_article.sort()
                                self.list_authors.append(temp)
                                self.list_authors.sort()

                    # iterates over each author in the list without html link, if the list is not empty
                    if list_authors_without_html_link is not None:
                        for temp in list_authors_without_html_link:
                            # saves the author name as a string
                            author = temp.text
                            # checks it the author already exists and if not, creates it and adds it to the authors list
                            if len(self.list_authors) == 0:
                                temp = Autor.Autor(author, None)
                                list_authors_in_article.append(temp)
                                self.list_authors.append(temp)
                            else:
                                created = False
                                for i in self.list_authors:
                                    if author == i.nome:
                                        list_authors_in_article.append(i)
                                        list_authors_in_article.sort()
                                        created = True
                                        break
                                    if author[0] < i.nome[0]:
                                        temp = Autor.Autor(author, None)
                                        list_authors_in_article.append(temp)
                                        list_authors_in_article.sort()
                                        self.list_authors.append(temp)
                                        self.list_authors.sort()
                                        created = True
                                        break
                                if created is False:
                                    temp = Autor.Autor(author, None)
                                    list_authors_in_article.append(temp)
                                    list_authors_in_article.sort()
                                    self.list_authors.append(temp)
                                    self.list_authors.sort()

                    # saves the article origin as a string
                    origin = '-'
                    try:
                        origin = item.find_element_by_xpath(".//li[@data-selenium-selector='venue-metadata']").text
                    except:
                        pass

                    # saves the article date as a string
                    date = '0'
                    try:
                        date = item.find_element_by_xpath(".//li[@data-selenium-selector='paper-year']").text
                    except:
                        pass

                    # saves the article influence factor as a string
                    influence = '0'
                    try:
                        influence = item.find_element_by_xpath(
                            ".//li[@data-selenium-selector='search-result-influential-citations']").text
                        influence = influence.replace(',', '')
                    except:
                        pass

                    # saves the article citation velocity as a string
                    velocity = '0'
                    try:
                        velocity = item.find_element_by_xpath(
                            ".//li[@data-selenium-selector='search-result-citation-velocity']").text
                        velocity = velocity.replace(',', '')
                    except:
                        pass

                    # saves the article html link as a string
                    link = '-'
                    try:
                        link = item.find_element_by_xpath(".//a[@data-selenium-selector='paper-link']").get_attribute(
                            'href')
                    except:
                        pass

                    # saves the article type as a string
                    cite = '-'
                    bibtex = '-'
                    try:
                        item.find_element_by_xpath(".//button[@data-selenium-selector='cite-link']").click()
                        try:
                            waitelement = WebDriverWait(driver, 20). \
                                until(EC.presence_of_element_located(
                                (By.XPATH, "//cite[@class='formatted-citation formatted-citation--style-bibtex']")))
                        except TimeoutError:
                            print("~~~~ PAGE DID NOT LOAD! ~~~~")

                        cite = driver.find_element_by_xpath(
                            "//cite[@class='formatted-citation formatted-citation--style-bibtex']").text
                        driver.find_element_by_xpath(
                            "//cite[@class='formatted-citation formatted-citation--style-bibtex']").send_keys(
                            Keys.ESCAPE)
                        bibtex = cite
                        cite = self.return_type_cite(cite)
                    except:
                        pass

                    # creates a new instance of a Article object
                    new_article = Artigo.Artigo(title, list_authors_in_article, origin, date,
                                                influence, velocity, link, cite, bibtex)

                    # checks if the article already exists, and if not, adds it to the articles list
                    repeated_article = False
                    if len(self.list_articles) == 0:
                        self.list_articles.append(new_article)
                    else:
                        created = False
                        for i in self.list_articles:
                            if new_article.link == i.link and new_article.titulo == i.titulo:
                                repeated_article = True
                                break
                            if new_article.titulo[0] < i.titulo[0]:
                                self.list_articles.append(new_article)
                                self.list_articles.sort()
                                created = True
                                break
                        if created is False and repeated_article is False:
                            self.list_articles.append(new_article)
                            self.list_articles.sort()

                    if repeated_article is False:
                        for autorTemp in list_authors_in_article:
                            autorTemp.addArtigo(new_article)

                    # feedback to user
                    # print('Article ' + title + " obtained with success.")

                # print('~~~~ PAGE ' + str(pag+1) + ' COMPLETED SUCCESSFULLY ~~~~')

                # tries to go to the next page, if exists
                try:
                    element = driver.find_element_by_xpath("//a[@data-selenium-selector='next-page']")
                    driver.execute_script('arguments[0].click()', element)
                except:
                    print("SUBJECT HAS NO MORE SEARCH PAGES!")
                    break

        self.end_time = Timer.timeNow()

        # closes the Google Chrome
        driver.quit()

        # saves the list of articles and authors as .pkl files
        self.manager.saveArtigos(self.list_articles)
        self.manager.saveAutores(self.list_authors)

        self.gui.show_search_done_alert(Timer.totalTime(self.start_time, self.end_time), str(len(self.list_articles)))

    def saves_excel(self, parameter):
        # creates the excel file
        os.chdir(self.current_directory)
        excelExporter = ExcelExporter.ExcelExporter(self.input_search)
        excelExporter.gui = self.gui
        excelExporter.order_type(parameter)





