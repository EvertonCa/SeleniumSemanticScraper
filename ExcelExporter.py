import xlsxwriter
import Gerenciador
import os


class ExcelExporter:
    def __init__(self, pesquisa):
        diretorio_original = os.getcwd()

        os.chdir(diretorio_original + '/Files/' + pesquisa + '/')
        diretorio_excel = diretorio_original + '/Files/' + pesquisa + '/'

        workbook = xlsxwriter.Workbook(diretorio_excel + pesquisa + '.xlsx')

        os.chdir(diretorio_original)

        worksheet_artigos = workbook.add_worksheet('ARTIGOS')
        worksheet_autores = workbook.add_worksheet('AUTORES')

        titulo = 0
        autores = 1
        publicado = 2
        data = 3
        influencia = 4
        velocidade = 5
        link = 6
        linha = 0

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

        worksheet_artigos.write(linha, titulo, 'Título do Artigo', primeiraLinha_format)
        worksheet_artigos.write(linha, autores, 'Autores', primeiraLinha_format)
        worksheet_artigos.write(linha, publicado, 'Origem da Publicação', primeiraLinha_format)
        worksheet_artigos.write(linha, data, 'Ano de Publicação', primeiraLinha_format)
        worksheet_artigos.write(linha, influencia, 'Fator de Influência', primeiraLinha_format)
        worksheet_artigos.write(linha, velocidade, 'Velocidade de Citação', primeiraLinha_format)
        worksheet_artigos.write(linha, link, 'Link do artigo', primeiraLinha_format)
        linha += 1

        gerenciador = Gerenciador.Gerenciador(pesquisa)
        listaDeArtigos = gerenciador.loadArtigos()
        listaDeAutores = gerenciador.loadAutores()

        for artigo in listaDeArtigos:
            primeiraLinha = linha
            worksheet_artigos.write(linha, titulo, artigo.titulo, one_line_format)
            worksheet_artigos.write(linha, publicado, artigo.publicado_em, one_line_format)
            worksheet_artigos.write(linha, data, artigo.data, one_line_format)
            worksheet_artigos.write(linha, influencia, artigo.influencia, one_line_format)
            worksheet_artigos.write(linha, velocidade, artigo.velocidade, one_line_format)
            worksheet_artigos.write(linha, link, artigo.link, one_line_format)
            for autor in artigo.autores:
                if autor.link is not None:
                    worksheet_artigos.write_url(linha, autores, autor.link, autor_format, string=autor.nome)
                else:
                    worksheet_artigos.write_url(linha, autores, '', autor_format, string=autor.nome)
                linha += 1
            if primeiraLinha != linha - 1:
                worksheet_artigos.merge_range(primeiraLinha, titulo, linha - 1, titulo, artigo.titulo, merge_format)
                worksheet_artigos.merge_range(primeiraLinha, publicado, linha - 1, publicado, artigo.publicado_em,
                                              merge_format)
                worksheet_artigos.merge_range(primeiraLinha, data, linha - 1, data, artigo.data, merge_format)
                worksheet_artigos.merge_range(primeiraLinha, influencia, linha - 1, influencia, artigo.influencia,
                                              merge_format)
                worksheet_artigos.merge_range(primeiraLinha, velocidade, linha - 1, velocidade, artigo.velocidade,
                                              merge_format)
                worksheet_artigos.merge_range(primeiraLinha, link, linha - 1, link, artigo.link, merge_format)

        nome_autor = 0
        link_autor = 1
        artigos_autor = 2
        linha = 0

        worksheet_autores.write(linha, nome_autor, 'Nome do Autor', primeiraLinha_format)
        worksheet_autores.write(linha, link_autor, 'Pagina do Autor', primeiraLinha_format)
        worksheet_autores.write(linha, artigos_autor, 'Artigos publicados relacionados', primeiraLinha_format)
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
