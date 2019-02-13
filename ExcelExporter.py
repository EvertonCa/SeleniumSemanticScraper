import xlsxwriter
import Gerenciador
import os


class ExcelExporter:
    def __init__(self):
        pass

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

    def single_creator(self, pesquisa):
        diretorio_original = os.getcwd()

        os.chdir(diretorio_original + '/Files/' + pesquisa + '/')
        diretorio_excel = diretorio_original + '/Files/' + pesquisa + '/'

        workbook = xlsxwriter.Workbook(diretorio_excel + pesquisa + '.xlsx')

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

        gerenciador = Gerenciador.Gerenciador(pesquisa)
        listaDeArtigos = gerenciador.loadArtigos()
        listaDeAutores = gerenciador.loadAutores()

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
