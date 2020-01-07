import os
import pickle
import ExcelExporter


class Merger:
    def __init__(self, folder_list):
        # saves current directory in a string
        current_directory = os.getcwd()

        # saves the Files directory in a string
        directory_files = os.path.join(current_directory, 'Results', 'Merged Search')

        # check if the Files folder exists and creates it if not
        if os.path.exists(directory_files):
            pass
        else:
            os.chdir(os.path.join(current_directory, 'Results'))
            os.mkdir('Merged Search')

        # return to root folder
        os.chdir(current_directory)

        # merge all files into one
        self.articles_list = []
        self.authors_list = []

        for i in folder_list:
            file_name_article = os.path.join(i, 'Articles.pkl')
            file_name_author = os.path.join(i, 'Authors.pkl')

            with open(file_name_article, 'rb') as file_input:
                articles_temp_list = pickle.load(file_input)

            for article in articles_temp_list:
                self.articles_list.append(article)

            with open(file_name_author, 'rb') as file_input:
                authors_temp_list = pickle.load(file_input)

            for author in authors_temp_list:
                self.authors_list.append(author)

        set_articles = set(self.articles_list)
        set_authors = set(self.authors_list)

        self.articles_list = list(set_articles)
        self.authors_list = list(set_authors)

