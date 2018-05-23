from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab import rl_config, rl_settings
from os import *
from Dados_SQLite import Manipulacao_SQL

def mesa():
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    arquivo = r"Logs e Relatórios\Relatórios\Convidados\mesa.pdf"
    pdf = canvas.Canvas(arquivo)
    objecto = Manipulacao_SQL()
    objecto.selecionarconvite_mesa()
    data = objecto.listageral_convitemesa
    tamanho = len(data)
    objecto.comparar_informacao()
    noivos = objecto.noivos
    data_evento = objecto.data
    noivos_data = str(noivos) + " " + str(data_evento)
    #pdf.drawImage("logon.png", 50, 710, 120, 100)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 700, "CONTROLO DE FESTAS")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 684, noivos_data)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 620, "Lista de convidados sentados na mesa - total: "+str(tamanho))



    lista_cabecalho = ['Nome', 'Mesa']
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

    pdf.setTitle("Convidados na mesa")
    pdf.showPage()
    pdf.save()
    startfile(arquivo)



def standby():
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    arquivo = r"Logs e Relatórios\Relatórios\Convidados\standby.pdf"
    pdf = canvas.Canvas(arquivo)
    objecto = Manipulacao_SQL()
    objecto.selecionarconvite_tipo()
    data = objecto.listageral_convites
    tamanho = len(data)
    objecto.comparar_informacao()
    noivos = objecto.noivos
    data_evento = objecto.data
    noivos_data = str(noivos) + " " + str(data_evento)
    #pdf.drawImage("logon.png", 50, 710, 120, 100)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 700, "CONTROLO DE FESTAS")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 684, noivos_data)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawString(50, 590, "Lista de convidados em standby - total: "+str(tamanho))


    lista_cabecalho = ['Nome', 'Tipo']
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

    pdf.setTitle("Convidados em standby")
    pdf.showPage()
    pdf.save()
    startfile(arquivo)

