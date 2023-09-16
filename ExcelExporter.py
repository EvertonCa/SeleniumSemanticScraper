import xlsxwriter
import Gerenciador
import os


class ExcelExporter:
    def __init__(self, search, single_or_merge, root_directory):
        self.root_directory = root_directory
        self.articles_list = []
        self.authors_list = []
        self.search_parameter = search
        self.ordered_date_articles_list = []
        self.ordered_citations_articles_list = []
        self.ordered_optimized_list = []
        self.gui = None
        self.single_or_merge = single_or_merge

    def set_list(self, articles_list, authors_list):
        self.articles_list = articles_list
        self.authors_list = authors_list

    def order_type(self, parameter):
        if self.single_or_merge:
            self.articles_list = self.gui.merger.articles_list
            self.authors_list = self.gui.merger.authors_list

            if parameter == 'Importance Rate (RECOMMENDED)':
                self.merge_creator(1)
            elif parameter == "Number of Citations":
                self.merge_creator(2)
            elif parameter == "Newer Articles":
                self.merge_creator(3)
            elif parameter == "Alphabetically, by Article's Title":
                self.merge_creator(4)
        else:
            if parameter == 'Importance Rate (RECOMMENDED)':
                self.single_creator(1)
            elif parameter == "Number of Citations":
                self.single_creator(2)
            elif parameter == "Newer Articles":
                self.single_creator(3)
            elif parameter == "Alphabetically, by Article's Title":
                self.single_creator(4)

    def order_optimized(self, articles_list):
        newer_date = 0

        for article in articles_list:
            if int(article.data) > newer_date:
                newer_date = int(article.data)

        for article in articles_list:
            article.data_relativa = int(article.data) / (newer_date if newer_date > 0 else 1)

            # put a score based on number of citations
            if int(article.citacoes) > 100:
                article.citacoes_relativa = 1
            elif 20 < int(article.citacoes) <= 100:
                article.citacoes_relativa = 0.5
            else:
                article.citacoes_relativa = 0


            qualis_dict = {'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4, 'B1': 5, 'B2': 6, 'B3': 7, 'B4': 8, 'B5': 9, 'C': 10, 'NF': 10}
            qualis_score = (10 - qualis_dict[article.qualis])/9
            
            # put a score based on article's type
            #label = float(self.article_label(article))
            #article.cite_label = (4 - label)/3

            article.total_factor = 0.2*article.data_relativa + 0.3*article.citacoes_relativa + 0.5*qualis_score

        self.ordered_optimized_list = articles_list
        self.ordered_optimized_list.sort(key=lambda model: model.total_factor, reverse=True)

    def order_articles(self, articles_list, order_type):
        max_citations = 0
        newer_date = 0
        for article in articles_list:
            if int(article.data) > newer_date:
                newer_date = int(article.data)
            if int(article.citacoes) > max_citations:
                max_citations = int(article.citacoes)

        for article in articles_list:
            article.data_relativa = int(article.data) / (newer_date if newer_date > 0 else 1)
            article.citacoes_relativa = int(article.citacoes) / (max_citations if max_citations > 0 else 1)

        self.ordered_date_articles_list = articles_list
        self.ordered_citations_articles_list = articles_list

        if order_type == 1:
            self.ordered_citations_articles_list.sort(key=lambda model: model.citacoes_relativa, reverse=True)
        else:
            self.ordered_date_articles_list.sort(key=lambda model: model.data_relativa, reverse=True)

    def merge_creator(self, search_type):
        os.chdir(os.path.join(self.root_directory, 'Results', 'Merged Search'))
        diretorio_excel = os.path.join(self.root_directory, 'Results', 'Merged Search')

        workbook = xlsxwriter.Workbook(os.path.join(diretorio_excel, 'Merged.xlsx'))

        os.chdir(self.root_directory)

        worksheet_artigos = workbook.add_worksheet('ARTICLES')
        worksheet_autores = workbook.add_worksheet('AUTHORS')

        indice = 0
        #type = 1
        titulo = 1
        autores = 2
        publicado = 3
        data = 4
        citacoes = 5
        qualis = 6
        optimized = 7
        link = 8
        bibtex = 9
        synopsis = 10
        linha = 0

        """label_comment = 'Label NUMBER: 1 -> article\n' \
                        'Label NUMBER: 2 -> conference, inproceedings, proceedings or phdthesis\n' \
                        'Label NUMBER: 3 -> mastersthesis, book, inbook, Incollection or techreport\n' \
                        'Label NUMBER: 4 -> manual, misc or unpublished'
        """

        primeiraLinha_format = workbook.add_format({'bold': True,
                                                    'font_size': '16',
                                                    'align': 'center',
                                                    'bg_color': '#757A79',
                                                    'font_color': 'white',
                                                    'border': 1})

        one_line_format = workbook.add_format({'bg_color': "#B5E9FF",
                                               'align': 'center',
                                               'border': 1})

        autor_format = workbook.add_format({'bg_color': "#B5E9FF",
                                            'align': 'center',
                                            'border': 1,
                                            'underline': True,
                                            'font_color': 'blue'})

        merge_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': "#B5E9FF",
            'border': 1
        })

        worksheet_artigos.write(linha, indice, 'Index', primeiraLinha_format)
        #worksheet_artigos.write(linha, type, 'Article Type', primeiraLinha_format)
        #worksheet_artigos.write_comment(linha, type, label_comment)
        worksheet_artigos.write(linha, titulo, 'Title', primeiraLinha_format)
        worksheet_artigos.write(linha, autores, 'Authors', primeiraLinha_format)
        worksheet_artigos.write(linha, publicado, 'Publication Source', primeiraLinha_format)
        worksheet_artigos.write(linha, data, 'Publication Year', primeiraLinha_format)
        worksheet_artigos.write(linha, citacoes, 'Citations', primeiraLinha_format)
        worksheet_artigos.write(linha, qualis, 'Qualis Score', primeiraLinha_format)
        worksheet_artigos.write(linha, optimized, 'Importance Rate', primeiraLinha_format)
        worksheet_artigos.write(linha, link, 'Article Link', primeiraLinha_format)
        worksheet_artigos.write(linha, bibtex, 'BibTex', primeiraLinha_format)
        worksheet_artigos.write(linha, synopsis, 'Synopsis', primeiraLinha_format)
        linha += 1

        if search_type == 1:
            self.order_optimized(self.articles_list)
            self.articles_list = self.ordered_optimized_list
        elif search_type == 2:
            self.order_articles(self.articles_list, 1)
            self.articles_list = self.ordered_citations_articles_list
        elif search_type == 3:
            self.order_articles(self.articles_list, 3)
            self.articles_list = self.ordered_date_articles_list
        elif search_type == 4:
            pass

        numeroDoArtigo = 1

        for artigo in self.articles_list:
            primeiraLinha = linha
            worksheet_artigos.write(linha, indice, str(numeroDoArtigo), one_line_format)

            #articleLabel = self.article_label(artigo)

            #worksheet_artigos.write(linha, type, articleLabel, one_line_format)
            worksheet_artigos.write(linha, titulo, artigo.titulo, one_line_format)
            worksheet_artigos.write(linha, publicado, artigo.publicado_em, one_line_format)
            worksheet_artigos.write(linha, data, artigo.data, one_line_format)
            worksheet_artigos.write(linha, citacoes, artigo.citacoes, one_line_format)
            worksheet_artigos.write(linha, qualis, artigo.qualis, one_line_format)
            worksheet_artigos.write(linha, optimized, artigo.total_factor, one_line_format)
            worksheet_artigos.write(linha, link, artigo.link, one_line_format)
            worksheet_artigos.write(linha, bibtex, artigo.bibtex, one_line_format)
            worksheet_artigos.write(linha, synopsis, artigo.synopsis, one_line_format)
            authors = ''

            for autor in artigo.autores:
                authors += autor.nome + ', '
            authors = authors[:-2]
            worksheet_artigos.write(linha, autores, authors, one_line_format)

            numeroDoArtigo += 1
            linha += 1

        nome_autor = 0
        link_autor = 1
        artigos_autor = 2
        linha = 0

        worksheet_autores.write(linha, nome_autor, 'Author Name', primeiraLinha_format)
        worksheet_autores.write(linha, link_autor, 'Author Page', primeiraLinha_format)
        worksheet_autores.write(linha, artigos_autor, 'Related Published Articles', primeiraLinha_format)
        linha += 1

        for autor in self.authors_list:
            primeiraLinha = linha
            worksheet_autores.write(linha, nome_autor, autor.nome, one_line_format)
            worksheet_autores.write(linha, link_autor, autor.link, one_line_format)
            for artigos in autor.artigos:
                try:
                    worksheet_autores.write_url(linha, artigos_autor, artigos.link, autor_format, string=artigos.titulo)
                except:
                    worksheet_autores.write(linha, artigos_autor, artigos.titulo, one_line_format)
                finally:
                    linha += 1
            if primeiraLinha != linha - 1:
                worksheet_autores.merge_range(primeiraLinha, nome_autor, linha - 1, nome_autor, autor.nome,
                                              merge_format)
                worksheet_autores.merge_range(primeiraLinha, link_autor, linha - 1, link_autor, autor.link,
                                              merge_format)

        workbook.close()

        self.gui.show_saved_alert(diretorio_excel)

    def single_creator(self, search_type):
        os.chdir(os.path.join(self.root_directory, 'Results', self.search_parameter))
        diretorio_excel = os.path.join(self.root_directory, 'Results', self.search_parameter)

        workbook = xlsxwriter.Workbook(os.path.join(diretorio_excel, self.search_parameter + '.xlsx'))

        os.chdir(self.root_directory)

        worksheet_artigos = workbook.add_worksheet('ARTICLES')
        worksheet_autores = workbook.add_worksheet('AUTHORS')

        indice = 0
        #type = 1
        titulo = 1
        autores = 2
        publicado = 3
        data = 4
        citacoes = 5
        qualis = 6
        optimized = 7
        link = 8
        bibtex = 9
        synopsis = 10
        linha = 0

        """label_comment = 'Label NUMBER: 1 -> Journal Article\n' \
                        'Label NUMBER: 2 -> Conference, CaseReport\n' \
                        'Label NUMBER: 3 -> Book, BookSection, News, Study\n' \
                        'Label NUMBER: 4 -> Others'
        """

        primeiraLinha_format = workbook.add_format({'bold': True,
                                                    'font_size': '16',
                                                    'align': 'center',
                                                    'bg_color': '#757A79',
                                                    'font_color': 'white',
                                                    'border': 1})

        one_line_format = workbook.add_format({'bg_color': "#B5E9FF",
                                               'align': 'center',
                                               'border': 1})

        autor_format = workbook.add_format({'bg_color': "#B5E9FF",
                                            'align': 'center',
                                            'border': 1,
                                            'underline': True,
                                            'font_color': 'blue'})

        merge_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': "#B5E9FF",
            'border': 1
        })

        worksheet_artigos.write(linha, indice, 'Index', primeiraLinha_format)
        #worksheet_artigos.write(linha, type, 'Article Type', primeiraLinha_format)
        #worksheet_artigos.write_comment(linha, type, label_comment)
        worksheet_artigos.write(linha, titulo, 'Title', primeiraLinha_format)
        worksheet_artigos.write(linha, autores, 'Authors', primeiraLinha_format)
        worksheet_artigos.write(linha, publicado, 'Publication Source', primeiraLinha_format)
        worksheet_artigos.write(linha, data, 'Publication Year', primeiraLinha_format)
        worksheet_artigos.write(linha, citacoes, 'Citations', primeiraLinha_format)
        worksheet_artigos.write(linha, qualis, 'Qualis Score', primeiraLinha_format)
        worksheet_artigos.write(linha, optimized, 'Importance Rate', primeiraLinha_format)
        worksheet_artigos.write(linha, link, 'Article Link', primeiraLinha_format)
        worksheet_artigos.write(linha, bibtex, 'BibTex', primeiraLinha_format)
        worksheet_artigos.write(linha, synopsis, 'Synopsis', primeiraLinha_format)
        linha += 1

        gerenciador = Gerenciador.Gerenciador(self.search_parameter, self.root_directory)
        listaDeArtigos = gerenciador.loadArtigos()
        listaDeAutores = gerenciador.loadAutores()

        if search_type == 1:
            self.order_optimized(listaDeArtigos)
            listaDeArtigos = self.ordered_optimized_list
        elif search_type == 2:
            self.order_articles(listaDeArtigos, 1)
            listaDeArtigos = self.ordered_citations_articles_list
        elif search_type == 3:
            self.order_articles(listaDeArtigos, 2)
            listaDeArtigos = self.ordered_date_articles_list
        elif search_type == 4:
            pass

        numeroDoArtigo = 1

        for artigo in listaDeArtigos:
            primeiraLinha = linha
            worksheet_artigos.write(linha, indice, str(numeroDoArtigo), one_line_format)

            #articleLabel = self.article_label(artigo)

            #worksheet_artigos.write(linha, type, articleLabel, one_line_format)
            worksheet_artigos.write(linha, titulo, artigo.titulo, one_line_format)
            worksheet_artigos.write(linha, publicado, artigo.publicado_em, one_line_format)
            worksheet_artigos.write(linha, data, artigo.data, one_line_format)
            worksheet_artigos.write(linha, citacoes, artigo.citacoes, one_line_format)
            worksheet_artigos.write(linha, qualis, artigo.qualis, one_line_format)
            worksheet_artigos.write(linha, optimized, artigo.total_factor, one_line_format)
            worksheet_artigos.write(linha, link, artigo.link, one_line_format)
            worksheet_artigos.write(linha, bibtex, artigo.bibtex, one_line_format)
            worksheet_artigos.write(linha, synopsis, artigo.synopsis, one_line_format)
            authors = ''

            for autor in artigo.autores:
                authors += autor.nome + ', '
            authors = authors[:-2]
            worksheet_artigos.write(linha, autores, authors, one_line_format)

            numeroDoArtigo += 1
            linha += 1

        nome_autor = 0
        link_autor = 1
        artigos_autor = 2
        linha = 0

        worksheet_autores.write(linha, nome_autor, 'Author Name', primeiraLinha_format)
        worksheet_autores.write(linha, link_autor, 'Author Page', primeiraLinha_format)
        worksheet_autores.write(linha, artigos_autor, 'Related Published Articles', primeiraLinha_format)
        linha += 1

        for autor in listaDeAutores:
            if len(autor.artigos) > 0:
                primeiraLinha = linha
                worksheet_autores.write(linha, nome_autor, autor.nome, one_line_format)
                worksheet_autores.write(linha, link_autor, autor.link, one_line_format)
                for artigos in autor.artigos:
                    try:
                        worksheet_autores.write_url(linha, artigos_autor, artigos.link, autor_format, string=artigos.titulo)
                    except:
                        worksheet_autores.write(linha, artigos_autor, artigos.titulo, one_line_format)
                    finally:
                        linha += 1
                if primeiraLinha != linha - 1:
                    worksheet_autores.merge_range(primeiraLinha, nome_autor, linha - 1, nome_autor, autor.nome,
                                                  merge_format)
                    worksheet_autores.merge_range(primeiraLinha, link_autor, linha - 1, link_autor, autor.link,
                                                  merge_format)

        workbook.close()

        self.gui.show_saved_alert(diretorio_excel)

    def article_label(self, artigo):
        if 'Conference' in artigo.cite or 'CaseReport' in artigo.cite:
            article_label = '2'
        elif 'JournalArticle' in artigo.cite or 'Review' in artigo.cite:
            article_label = '1'
        elif 'Book' in artigo.cite or 'BookSection' in artigo.cite or 'News' in artigo.cite or 'Study' in artigo.cite:
            article_label = '3'
        else:
            article_label = '4'

        return article_label