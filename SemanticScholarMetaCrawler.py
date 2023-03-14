import os
import re
import requests
import sys
from typing import List,Set
import datetime

from Artigo import Artigo
from Autor import Autor
from ExcelExporter import ExcelExporter
from Gerenciador import Gerenciador
import Timer


class Crawler:
    def __init__(self, root_directory):
        # saves current directory in a string
        self.root_directory = root_directory

        self.start_time = Timer.timeNow()
        self.end_time = Timer.timeNow()

        self.manager = None
        self.list_authors: List[Autor] = []
        self.list_articles: List[Artigo] = []

        self.input_search = ''
        self.input_pages = 0

        self.gui = None

        self.index_progress_bar = 1

    def update_search_parameters(self, input_search, input_pages):
        self.input_search = input_search
        self.input_pages = input_pages

    # extract the type of the article from the BibText cite text and returns it as a single word string
    # TODO: extract it from "publicationTypes" attribute
    def return_type_cite(self, string_cite):
        list_cite = string_cite.split('{')
        type_cite = list_cite[0][1:]
        return type_cite

    def start_search(self):
        self.start_time = Timer.timeNow()

        # loads files for the inputted search if they exist, otherwise, the files are created
        self.manager = Gerenciador(self.input_search, self.root_directory)
        self.list_authors = self.manager.loadAutores()
        self.list_articles = set(self.manager.loadArtigos())

        # runs the following code 3 times, one for each type os search
        # for k in range(0, 2):
        # TODO: replicate old functionality with API,
        # i.e., search in different ways.

        for k in range(0,2):
            # label gui
            self.gui.app.queueFunction(self.gui.app.setLabel, 'progress_bar_label', 'Crawling with '
                                        + str(k+1) + '/2 parameter...')
                                        # + str(k+1) + '/3 parameter...')
            #self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar', 0)

            # access switched to api calls,
            # input now sent directly via request url,
            # with extra whitespace striped
            _search_query = re.sub(r"\s+", " ", self.input_search.strip())
            _article_count = self.input_pages
            _articles_query_params = {
                "query": _search_query,
                "fields": "abstract,authors,citationCount,citationStyles,title,url,venue,year",
                "offset": 0,
                "limit": _article_count
            }

            if k == 1:
                _articles_query_params["year"] = str(datetime.date.today().year - 5) + '-' 

            # TODO: model expected JSON object types
            # e.g., search :: String -> [Paper]
            # Paper :: { title: String, Author: Author, ...}
            _articles_endpoint = 'https://api.semanticscholar.org/graph/v1/paper/search'
            
            with requests.get(_articles_endpoint, params=_articles_query_params) as articles_res:
                _articles_res = articles_res.json()

                # search for now happens only once
                # TODO: mimic the old behavior,
                # i.e., searching with different filters applied:
                # results from the last five years;
                # results with Reviews marked.

                # runs the code for the amount of articles desired
                self.index_progress_bar = 1

                # no need for pagination yet,
                # as number of articles is explicitly set,
                # in API request.
                # TODO: sync progress bar to other inputs,
                # previously was number of pages crawled.
                # for pag in range(0, self.input_pages):
                    # progress bar
                    # self.gui.app.queueFunction(self.gui.app.setMeter, 'progress_bar',
                    #                             (100 * self.index_progress_bar)/self.input_pages)
                    # self.index_progress_bar += 1

                # from API response,
                # iterates over each article in the articles list
                if "data" in _articles_res.keys():
                    for item in _articles_res["data"]:
                        # now takes it directly from JSON
                        # saves the article title as a string
                        title = item["title"]

                        # now authors field is present in API response
                        _paper_authors = item["authors"]
                        # TODO: get html links for authors who have it,
                        # probably will require another API call.

                        # creates a set list of the authors for the article
                        list_authors_in_article: Set[Autor] = set()
                        self.list_authors = set(self.list_authors)

                        # iterates over each author in the list.
                        for temp in _paper_authors:
                            # author name now comes in "name" field
                            name = temp["name"]

                            # saves the author name as a string

                            # no link comes with author from Papers API
                            # TODO: fetch their link somehow.
                            link = None
                            # saves the author page html link as a string
                            # creates temporary author
                            author = Autor(name, link)

                            # adds new authors to the set lists
                            self.list_authors.add(author)
                            list_authors_in_article.add(author)

                        self.list_authors = list(self.list_authors)
                        self.list_authors.sort()
                        list_authors_in_article = list(list_authors_in_article)
                        list_authors_in_article.sort()

                        # origin comes as "venue" in API response.
                        _venue = item["venue"]
                        origin = _venue if _venue else "-"
                        # saves the article origin as a string
                        # TODO: log when field comes empty,
                        # print paper id, field name and its value.

                        # date comes as "year" in API response.
                        _year = item["year"]
                        # TODO: log when field comes empty,
                        # print paper id, field name and its value.
                        date = str(_year) if _year else "0"
                        # saves the article date as a string

                        # citationCount comes as a number in API response.
                        _citationCount = item["citationCount"]
                        citationCount = str(int(_citationCount if _citationCount else "0"))
                        # saves the article total citations as a string
                        # TODO: log when field comes empty,
                        # print paper id, field name and its value.

                        # link comes as "url" in API response.
                        _url = item["url"]
                        link = _url if _url else "-"
                        # saves the article html link as a string
                        # TODO: log when field comes empty,
                        # print paper id, field name and its value.

                        # currently no type comes in API response.
                        _citationStyles = item["citationStyles"]
                        _bibtex = _citationStyles["bibtex"] if _citationStyles else _citationStyles
                        bibtex = '-'
                        cite = '-'
                        if _bibtex:
                            bibtex = _bibtex
                            # TODO: format bibtex,
                            # it comes in a weird list-like style,
                            # e.g., @["Journal Article", "Review"]{...}

                            cite = self.return_type_cite(bibtex)
                            # saves the article type as a string
                            # TODO: get type from "publicationTypes" field.

                        # synopsis comes as "abstract" in API response.
                        _abstract = item["abstract"]
                        synopsis = _abstract.replace(" Expand", "") if _abstract else "No synopsis"
                        synopsis = synopsis.replace("TLDR\n", "")

                        # creates a new instance of a Article object
                        new_article = Artigo(title, list_authors_in_article, origin, date,
                                                    citationCount, link, cite, bibtex, synopsis)

                        # adds new article to set list (set list does not allow duplicates)
                        before = len(self.list_articles)
                        self.list_articles.add(new_article)
                        after = len(self.list_articles)

                        # add article to the author's article list if the article is not repeated
                        if before is not after:
                            for autorTemp in list_authors_in_article:
                                autorTemp.addArtigo(new_article)

                        # no need to switch pages when using API.
                        # TODO: add pagination to API calls.
                else:
                    print("From Semantic Scholar API:", file=sys.stderr)
                    for k in _articles_res.keys():
                        print(k, ": ", _articles_res[k], sep="", file=sys.stderr)

        self.end_time = Timer.timeNow()

        self.list_articles = list(self.list_articles)

        # saves the list of articles and authors as .pkl files
        self.list_authors = list(self.list_authors)

        self.manager.saveArtigos(self.list_articles)
        self.manager.saveAutores(self.list_authors)

        self.gui.show_search_done_alert(Timer.totalTime(self.start_time, self.end_time), str(len(self.list_articles)))

    def saves_excel(self, parameter):
        # creates the excel file
        os.chdir(self.root_directory)
        excelExporter = ExcelExporter(self.input_search, self.gui.single_or_merge, self.root_directory)
        excelExporter.gui = self.gui
        excelExporter.order_type(parameter)