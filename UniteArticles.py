import os
import pickle
import ExcelExporter


class Merger:
    def __init__(self, folder_list):
        # saves current directory in a string
        current_directory = os.getcwd()

        # saves the Files directory in a string
        directory_files = current_directory + '/Results/Merged Search/'

        # check if the Files folder exists and creates it if not
        if os.path.exists(directory_files):
            pass
        else:
            os.chdir(current_directory + '/Results/')
            os.mkdir('Merged Search')

        # return to root folder
        os.chdir(current_directory)

        # merge all files into one
        self.articles_list = []
        self.authors_list = []

        # repeated_article = False
        # if len(self.list_articles) == 0:
        #     self.list_articles.append(new_article)
        # else:
        #     created = False
        #     for i in self.list_articles:
        #         if new_article.link == i.link and new_article.titulo == i.titulo:
        #             repeated_article = True
        #             break
        #         if new_article.titulo[0] < i.titulo[0]:
        #             self.list_articles.append(new_article)
        #             self.list_articles.sort()
        #             created = True
        #             break
        #     if created is False and repeated_article is False:
        #         self.list_articles.append(new_article)
        #         self.list_articles.sort()
        #
        # if repeated_article is False:
        #     for autorTemp in list_authors_in_article:
        #         autorTemp.addArtigo(new_article)

        for i in folder_list:
            file_name_article = i + '/Articles.pkl'
            file_name_author = i + '/Authors.pkl'
            with open(file_name_article, 'rb') as file_input:
                articles_temp_list = pickle.load(file_input)
            for article in articles_temp_list:
                self.articles_list.append(article)
            with open(file_name_author, 'rb') as file_input:
                authors_temp_list = pickle.load(file_input)
            for author in authors_temp_list:
                self.authors_list.append(author)

