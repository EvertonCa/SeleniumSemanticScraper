import xlsxwriter
import Gerenciador

workbook = xlsxwriter.Workbook('Snake Algorithm.xlsx')
worksheet = workbook.add_worksheet()

titulo = 0
autores = 1
paginaDoAutor = 2
publicado = 3
data = 4
influencia = 5
velocidade = 6
link = 7
linha = 0

bold = workbook.add_format({'bold': True, 'font_size': '16', 'align': 'center'})

worksheet.write(linha, titulo, 'Titulo', bold)
worksheet.write(linha, autores, 'Autores', bold)
worksheet.write(linha, paginaDoAutor, 'Pagina do Autor', bold)
worksheet.write(linha, publicado, 'Origem da Publicação', bold)
worksheet.write(linha, data, 'Ano de Publicação', bold)
worksheet.write(linha, influencia, 'Fator de Influencia', bold)
worksheet.write(linha, velocidade, 'Velocidade de Citação', bold)
worksheet.write(linha, link, 'Link do artigo', bold)
linha += 1

gerenciador = Gerenciador.Gerenciador('Snake Algorithm')
listaDeArtigos = gerenciador.loadArtigos()
listaDeAutores = gerenciador.loadAutores()

for artigo in listaDeArtigos:
    worksheet.write(linha, titulo, artigo.titulo)
    worksheet.write(linha, publicado, artigo.publicado_em)
    worksheet.write(linha, data, artigo.data)
    worksheet.write(linha, influencia, artigo.influencia)
    worksheet.write(linha, velocidade, artigo.velocidade)
    worksheet.write(linha, link, artigo.link)
    for autor in artigo.autores:
        worksheet.write(linha, autores, autor.nome)
        worksheet.write(linha, paginaDoAutor, autor.link)
        linha +=1

workbook.close()
