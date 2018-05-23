from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab import rl_config, rl_settings
from os import *
from Dados_SQLite import Manipulacao_SQL

def activos():
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    arquivo = r"Logs e Relatórios\Relatórios\Activos\activos.pdf"
    pdf = canvas.Canvas(arquivo)
    objecto = Manipulacao_SQL()
    objecto.selecionarconvite_activos()
    data = objecto.listageral_conviteactivos
    tamanho = len(data)
    objecto.comparar_informacao()
    noivos = objecto.noivos
    data_evento = objecto.data
    noivos_data = str(noivos) + " " + str(data_evento)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 700, "CONTROLO DE FESTAS")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 684, noivos_data)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 620, "Lista de convidados no salão - total: "+ str(tamanho))
    lista_cabecalho = ['Nome', 'Posição', 'Entrada']
    data.insert(0, lista_cabecalho)
    t = Table(data)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
    aW = 540
    aH = 720
    w, h = t.wrap(aW, aH)
    t.drawOn(pdf, 50, 520)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor("steelblue")

    pdf.setTitle("Convidados no salão")
    pdf.showPage()
    pdf.save()
    startfile(arquivo)


