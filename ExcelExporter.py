import xlsxwriter
import Gerenciador
import os


class ExcelExporter:
    def __init__(self, search):
        self.search_parameter = search
        self.ordered_date_articles_list = []
        self.ordered_influence_articles_list = []
        self.ordered_velocity_articles_list = []
        self.ordered_optimized_list = []
        self.alpha1 = 1
        self.alpha2 = 1
        self.alpha3 = 1
        self.gui = None

    def order_type(self, parameter):
        if parameter == 'Optimized Rating (RECOMMENDED)':
            self.single_creator(1)
        elif parameter == "Influence Factor":
            self.single_creator(2)
        elif parameter == "Citation Velocity":
            self.single_creator(3)
        elif parameter == "Newer Articles":
            self.single_creator(4)
        elif parameter == "Alphabetically, by Article's Title":
            self.single_creator(5)

    def define_alphas(self):
        self.alpha1 = self.gui.alpha1
        self.alpha2 = self.gui.alpha2
        self.alpha3 = self.gui.alpha3

    def order_optimized(self, articles_list):
        max_influence = 0
        max_velocity = 0
        newer_date = 0
        for article in articles_list:
            if int(article.data) > newer_date:
                newer_date = int(article.data)
            if int(article.influencia) > max_influence:
                max_influence = int(article.influencia)
            if int(article.velocidade) > max_velocity:
                max_velocity = int(article.velocidade)

        for article in articles_list:
            article.data_relativa = int(article.data) / newer_date
            article.influencia_relativa = int(article.influencia) / max_influence
            article.velocidade_relativa = int(article.velocidade) / max_velocity
            article.total_factor = \
                (((self.alpha1 / (self.alpha1 + self.alpha2 + self.alpha3)) * article.velocidade_relativa) +
                 ((self.alpha2 / (self.alpha1 + self.alpha2 + self.alpha3)) * article.influencia_relativa) +
                 ((self.alpha3 / (self.alpha1 + self.alpha2 + self.alpha3)) * article.data_relativa))

        self.ordered_optimized_list = articles_list
        self.ordered_optimized_list.sort(key=lambda model: model.total_factor, reverse=True)

    def order_articles(self, articles_list, order_type):
        max_influence = 0
        max_velocity = 0
        newer_date = 0
        for article in articles_list:
            if int(article.data) > newer_date:
                newer_date = int(article.data)
            if int(article.influencia) > max_influence:
                max_influence = int(article.influencia)
            if int(article.velocidade) > max_velocity:
                max_velocity = int(article.velocidade)

        for article in articles_list:
            article.data_relativa = int(article.data) / newer_date
            article.influencia_relativa = int(article.influencia) / max_influence
            article.velocidade_relativa = int(article.velocidade) / max_velocity

        self.ordered_date_articles_list = articles_list
        self.ordered_influence_articles_list = articles_list
        self.ordered_velocity_articles_list = articles_list

        if order_type == 1:
            self.ordered_influence_articles_list.sort(key=lambda model: model.influencia_relativa, reverse=True)
        elif order_type == 2:
            self.ordered_velocity_articles_list.sort(key=lambda model: model.velocidade_relativa, reverse=True)
        else:
            self.ordered_date_articles_list.sort(key=lambda model: model.data_relativa, reverse=True)

    def merge_creator(self, articles_list, authors_list):
        diretorio_original = os.getcwd()

        os.chdir(diretorio_original + '/Files/Unite/')
        diretorio_excel = diretorio_original + '/Files/Unite/'

        workbook = xlsxwriter.Workbook(diretorio_excel + 'Merged.xlsx')

        os.chdir(diretorio_original)

        worksheet_artigos = workbook.add_worksheet('ARTICLES')
        worksheet_autores = workbook.add_worksheet('AUTHORS')

        indice = 0
        type = 1
        titulo = 2
        autores = 3
        publicado = 4
        data = 5
        influencia = 6
        velocidade = 7
        link = 8
        bibtex = 9
        linha = 0

        label_comment = 'Label NUMBER: 1 -> article\n' \
                        'Label NUMBER: 2 -> conference, inproceedings, proceedings or phdthesis\n' \
                        'Label NUMBER: 3 -> mastersthesis, book, inbook, Incollection or techreport\n' \
                        'Label NUMBER: 4 -> manual, misc or unpublished'

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
        worksheet_artigos.write(linha, type, 'Article Type', primeiraLinha_format)
        worksheet_artigos.write_comment(linha, type, label_comment)
        worksheet_artigos.write(linha, titulo, 'Title', primeiraLinha_format)
        worksheet_artigos.write(linha, autores, 'Authors', primeiraLinha_format)
        worksheet_artigos.write(linha, publicado, 'Publication Source', primeiraLinha_format)
        worksheet_artigos.write(linha, data, 'Publication Year', primeiraLinha_format)
        worksheet_artigos.write(linha, influencia, 'Influence Factor', primeiraLinha_format)
        worksheet_artigos.write(linha, velocidade, 'Citation Velocity', primeiraLinha_format)
        worksheet_artigos.write(linha, link, 'Article Link', primeiraLinha_format)
        worksheet_artigos.write(linha, bibtex, 'BibTex', primeiraLinha_format)
        linha += 1

        numeroDoArtigo = 1

        for artigo in articles_list:
            primeiraLinha = linha
            worksheet_artigos.write(linha, indice, str(numeroDoArtigo), one_line_format)

            article_label = ''
            if artigo.cite == 'article':
                article_label = '1'
            elif artigo.cite == 'conference' or artigo.cite == 'inproceedings' or artigo.cite == 'proceedings' or \
                    artigo.cite == 'phdthesis':
                article_label = '2'
            elif artigo.cite == 'mastersthesis' or artigo.cite == 'book' or artigo.cite == 'inbook' or \
                    artigo.cite == 'Incollection' or artigo.cite == 'techreport':
                article_label = '3'
            else:
                article_label = '4'

            worksheet_artigos.write(linha, type, article_label, one_line_format)
            worksheet_artigos.write(linha, titulo, artigo.titulo, one_line_format)
            worksheet_artigos.write(linha, publicado, artigo.publicado_em, one_line_format)
            worksheet_artigos.write(linha, data, artigo.data, one_line_format)
            worksheet_artigos.write(linha, influencia, artigo.influencia, one_line_format)
            worksheet_artigos.write(linha, velocidade, artigo.velocidade, one_line_format)
            worksheet_artigos.write(linha, link, artigo.link, one_line_format)
            worksheet_artigos.write(linha, bibtex, artigo.bibtex, one_line_format)
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

        for autor in authors_list:
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

    def single_creator(self, search_type):
        diretorio_original = os.getcwd()

        os.chdir(diretorio_original + '/Files/' + self.search_parameter + '/')
        diretorio_excel = diretorio_original + '/Files/' + self.search_parameter + '/'

        workbook = xlsxwriter.Workbook(diretorio_excel + self.search_parameter + '.xlsx')

        os.chdir(diretorio_original)

        worksheet_artigos = workbook.add_worksheet('ARTICLES')
        worksheet_autores = workbook.add_worksheet('AUTHORS')

        indice = 0
        type = 1
        titulo = 2
        autores = 3
        publicado = 4
        data = 5
        influencia = 6
        velocidade = 7
        optimized = 8
        link = 9
        bibtex = 10
        linha = 0

        label_comment = 'Label NUMBER: 1 -> article\n' \
                        'Label NUMBER: 2 -> conference, inproceedings, proceedings or phdthesis\n' \
                        'Label NUMBER: 3 -> mastersthesis, book, inbook, Incollection or techreport\n' \
                        'Label NUMBER: 4 -> manual, misc or unpublished'

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
        worksheet_artigos.write(linha, type, 'Article Type', primeiraLinha_format)
        worksheet_artigos.write_comment(linha, type, label_comment)
        worksheet_artigos.write(linha, titulo, 'Title', primeiraLinha_format)
        worksheet_artigos.write(linha, autores, 'Authors', primeiraLinha_format)
        worksheet_artigos.write(linha, publicado, 'Publication Source', primeiraLinha_format)
        worksheet_artigos.write(linha, data, 'Publication Year', primeiraLinha_format)
        worksheet_artigos.write(linha, influencia, 'Influence Factor', primeiraLinha_format)
        worksheet_artigos.write(linha, velocidade, 'Citation Velocity', primeiraLinha_format)
        worksheet_artigos.write(linha, link, 'Article Link', primeiraLinha_format)
        worksheet_artigos.write(linha, bibtex, 'BibTex', primeiraLinha_format)
        worksheet_artigos.write(linha, optimized, 'Optimized Factor', primeiraLinha_format)
        linha += 1

        gerenciador = Gerenciador.Gerenciador(self.search_parameter)
        listaDeArtigos = gerenciador.loadArtigos()
        listaDeAutores = gerenciador.loadAutores()

        if search_type == 1:
            self.define_alphas()
            self.order_optimized(listaDeArtigos)
            listaDeArtigos = self.ordered_optimized_list
        elif search_type == 2:
            self.order_articles(listaDeArtigos, 1)
            listaDeArtigos = self.ordered_influence_articles_list
        elif search_type == 3:
            self.order_articles(listaDeArtigos, 2)
            listaDeArtigos = self.ordered_velocity_articles_list
        elif search_type == 4:
            self.order_articles(listaDeArtigos, 3)
            listaDeArtigos = self.ordered_date_articles_list
        elif search_type == 5:
            pass

        numeroDoArtigo = 1

        for artigo in listaDeArtigos:
            primeiraLinha = linha
            worksheet_artigos.write(linha, indice, str(numeroDoArtigo), one_line_format)

            article_label = ''
            if artigo.cite == 'article':
                article_label = '1'
            elif artigo.cite == 'conference' or artigo.cite == 'inproceedings' or artigo.cite == 'proceedings' or \
                    artigo.cite == 'phdthesis':
                article_label = '2'
            elif artigo.cite == 'mastersthesis' or artigo.cite == 'book' or artigo.cite == 'inbook' or \
                    artigo.cite == 'Incollection' or artigo.cite == 'techreport':
                article_label = '3'
            else:
                article_label = '4'

            worksheet_artigos.write(linha, type, article_label, one_line_format)
            worksheet_artigos.write(linha, titulo, artigo.titulo, one_line_format)
            worksheet_artigos.write(linha, publicado, artigo.publicado_em, one_line_format)
            worksheet_artigos.write(linha, data, artigo.data, one_line_format)
            worksheet_artigos.write(linha, influencia, artigo.influencia, one_line_format)
            worksheet_artigos.write(linha, velocidade, artigo.velocidade, one_line_format)
            worksheet_artigos.write(linha, optimized, artigo.total_factor, one_line_format)
            worksheet_artigos.write(linha, link, artigo.link, one_line_format)
            worksheet_artigos.write(linha, bibtex, artigo.bibtex, one_line_format)
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
