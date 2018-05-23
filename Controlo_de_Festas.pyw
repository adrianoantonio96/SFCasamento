from tkinter import *
import tkinter.ttk as tkbest
import tkinter.messagebox
from sqlite3 import *
from Dados_SQLite import Manipulacao_SQL
from Dados import *
import Relatorio_Convidados
import Relatorio_activos
import Janela_Geral
class CDF(object):
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.state("zoomed")
        self.janela_principal.resizable(False, False)


        self.menu_janela()
        self.janela_principal.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.pesquisa_lateral()



    def fechar_janela(self):
        if tkinter.messagebox.askokcancel("Sair", "Deseja sair?") == True:
             self.janela_principal.destroy()




    def menu_janela(self):
        self.menubar = Menu(self.janela_principal)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Mesa", command = self.reg_mesa)
        filemenu.add_command(label="Convidado", command = self.validar_inserir_convidado)#self.reg_convidado
        self.menubar.add_cascade(label="Registar", menu=filemenu)
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Convidados", command = self.vista_convidado)
        editmenu.add_command(label="Mesas", command = self.vista_mesa)
        editmenu.add_command(label="Stand by", command = self.vista_standby)
        editmenu.add_command(label="Activos", command=self.vista_activos)
        self.menubar.add_cascade(label="Ver", menu=editmenu)
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Geral", command = self.geral_info)
        helpmenu.add_command(label="Manual")
        helpmenu.add_command(label="Sobre", command = self.sobre_info)
        self.menubar.add_cascade(label="Definições", menu=helpmenu)
        self.janela_principal.config(menu = self.menubar)


    def validar_inserir_convidado(self):
        self.frame_superiorpasse = Frame(self.janela_principal, width = 300, height = 40, relief = SOLID, bg = branco)
        self.frame_superiorpasse.place(x = 50, y = 4)
        self.entry_password = tkbest.Entry(self.frame_superiorpasse, justify = justificacao, show = "*")
        self.entry_password.place(x = 20, y = 10)
        self.entry_password.focus_force()
        bt_validarpasse = tkbest.Button(self.frame_superiorpasse, text = "validar", command = self.validar_password).place(x = 150, y = 8)
        try:
            self.frame_fileconvidado.place_forget()
        except:
            pass

    def validar_password(self):
        if self.entry_password.get() == "amorepaz":
            self.frame_superiorpasse.place_forget()
            self.reg_convidado()
        else:
            tkinter.messagebox.showinfo("Erro", "Não tem permissão para adicionar convidado")

    def geral_info(self):
        objecto = Manipulacao_SQL()
        objecto.comparar_informacao()
        informacao = objecto.comparacao
        if informacao == 0:
            Janela_Geral.iniciar_janela()
        else:
            tkinter.messagebox.showinfo("Excesso", "Um casamento já foi registado")


    def sobre_info(self):
        tkinter.messagebox.showinfo("Sobre", "Desenvolvedor: Adriano António"+"\n"+"Contacto: 922-961-983\n"+"Email: alexandredgar20@hotmail.com ou www.facebook.com\emmer.driizzi\n"+"Desenvolvedor Python - 2018")


    def pesquisa_lateral(self):
        tkbest.Label(self.janela_principal, text="PESQUISAR ACTIVOS", background=azul, font=fonte).place(x=800, y=20)
        self.pesquisaactivo = tkbest.Combobox(self.janela_principal, justify = justificacao, state = leitura, font = fonte, width = 35)
        self.pesquisaactivo.place(x = 800, y = 50)

        self.pesquisaactivo.bind("<Enter>", self.adicionardado_pesquisactivo)

        self.pesquisaactivo.bind("<<ComboboxSelected>>", self.frame_lateralactivos)

    def frame_lateralactivos(self, e):
        self.frame_lateral = Frame(self.janela_principal, width = 300 ,height = 600, relief = "solid", bg = branco)
        self.frame_lateral.place(x = 800, y = 90)

        cabecalho = ['Nome do convidado']

        objecto = Manipulacao_SQL()
        localizacao = self.pesquisaactivo.get()
        objecto.selecionarnomes_activos(localizacao)
        self.lista_dadostreeviewstb = objecto.listanomes


        self.treedataview_stb = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_stb.place(x = 846, y = 130)

        for col in cabecalho:
            self.treedataview_stb.heading(col, text=col)
            self.treedataview_stb.column(col, anchor='center', width=200)
        for item in self.lista_dadostreeviewstb:
            self.treedataview_stb.insert('', 'end', values=item)


    def reg_mesa(self):
        self.frame_filemesa = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_filemesa.place(x = 50, y = 50)
        self.cb_pesquisafilemesa = tkbest.Combobox(self.frame_filemesa, justify = justificacao, state = leitura, font = fonte, width = 35)
        self.cb_pesquisafilemesa.place(x = 20, y = 40)
        tkbest.Label(self.frame_filemesa, text="PESQUISAR", background=branco, font = fonte).place(x=330, y= 40)
        tkbest.Label(self.frame_filemesa, text="Nº da Mesa", background = branco).place(x=20, y=105)
        self.entry_mesafilemesa = tkbest.Entry(self.frame_filemesa, justify = justificacao)
        self.entry_mesafilemesa.place(x = 20, y = 130)

        frame_btsfilemesa = Frame(self.frame_filemesa, width = 300, height = 40, relief = "solid", bg = azul)
        frame_btsfilemesa.place(x = 20, y = 200)

        self.btnova_filemesa = tkbest.Button(frame_btsfilemesa, text = "novo", state = desabilitado, command = self.adicionar_mesa)
        self.btnova_filemesa.place(x = 20, y = 6)

        self.bteliminar_filemesa = tkbest.Button(frame_btsfilemesa, text = "eliminar", state = desabilitado, command = self.eliminar_mesa)
        self.bteliminar_filemesa.place(x = 200, y = 6)

        self.cb_pesquisafilemesa.bind("<Enter>", self.adicionardado_cbfindmesa)
        self.bteliminar_filemesa.bind("<Enter>", self.validar_eliminar)

        self.btnova_filemesa.bind("<Enter>", self.validar_inserirmesa)



    def reg_convidado(self):
        #self.frame_filemesa.place_forget()
        self.frame_fileconvidado = Frame(self.janela_principal, width = 650, height = 450, relief = "solid", bg = branco)
        self.frame_fileconvidado.place(x = 50, y = 50)
        self.cb_pesquisafileconvidado = tkbest.Combobox(self.frame_fileconvidado, justify = justificacao, state = leitura, font = fonte, width = 35)
        self.cb_pesquisafileconvidado.place(x = 20, y = 40)
        tkbest.Label(self.frame_fileconvidado, text="PESQUISAR", background=branco, font=fonte).place(x=330, y=40)
        tkbest.Label(self.frame_fileconvidado, text = "Nome completo", background = branco).place(x = 20, y = 105)
        self.entry_nomefileconvidado = tkbest.Entry(self.frame_fileconvidado, justify = justificacao)
        self.entry_nomefileconvidado.place(x = 20, y = 130)
        tkbest.Label(self.frame_fileconvidado, text="Posição (Mesa)", background = branco).place(x=180, y=105)
        self.cb_numfileconvidado = tkbest.Combobox(self.frame_fileconvidado, justify = justificacao, state = leitura)
        self.cb_numfileconvidado.place(x = 180, y = 130)
        frame_btsfileconvidado = Frame(self.frame_fileconvidado, width = 300, height = 40, relief = "solid", bg = azul)
        frame_btsfileconvidado.place(x = 20, y = 200)
        self.btnovo_fileconvidado = tkbest.Button(frame_btsfileconvidado, text = "novo", state = desabilitado, command = self.adicionar_convidado)
        self.btnovo_fileconvidado.place(x = 20, y = 6)
        self.btalterar_fileconvidado = tkbest.Button(frame_btsfileconvidado, text = "alterar", state = desabilitado, command = self.actualizar_convidado)
        self.btalterar_fileconvidado.place(x = 110, y = 6)
        self.bteliminar_fileconvidado = tkbest.Button(frame_btsfileconvidado, text = "eliminar", state=desabilitado, command = self.eliminar_convidado)
        self.bteliminar_fileconvidado.place(x = 200, y = 6)

        self.cb_numfileconvidado.bind("<Enter>", self.adicionardado_cbposicaoconv)
        self.btnovo_fileconvidado.bind("<Enter>", self.validar_novoconvite)
        self.cb_pesquisafileconvidado.bind("<Enter>", self.find_convidados)
        self.cb_pesquisafileconvidado.bind("<<ComboboxSelected>>", self.selecionar_dado_convites)
        self.bteliminar_fileconvidado.bind("<Enter>", self.validar_eliminarconvidado)



    def vista_mesa(self):
        self.frame_viewmesa = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewmesa.place(x = 50, y = 50)

        bt_pdf = tkbest.Button(self.frame_viewmesa, text = "pdf", command = self.pdf_mesa)
        bt_pdf.place(x = 315, y = 250)

        cabecalho = ['Nome do convidado', 'Nº da Mesa']

        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_mesa()
        self.lista_dadostreeviewmesa = objecto.listageral_convitemesa

        total = len(self.lista_dadostreeviewmesa)

        tkbest.Label(self.frame_viewmesa, text = str(total) + " Pessoas nas mesas", background=branco).place(x=20, y=255)


        self.treedataview_mesa = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_mesa.place(x = 150, y = 60)

        for col in cabecalho:
            self.treedataview_mesa.heading(col, text=col)
            self.treedataview_mesa.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewmesa:
            self.treedataview_mesa.insert('', 'end', values=item)



    def vista_convidado(self):
        self.frame_viewconvidado = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewconvidado.place(x = 50, y = 50)
        tkbest.Label(self.frame_viewconvidado, text="Nome completo", background = branco).place(x=20, y=105)
        self.entry_nomeviewconvidado = tkbest.Combobox(self.frame_viewconvidado, justify = justificacao, state = leitura)
        self.entry_nomeviewconvidado.place(x=20, y=130)
        tkbest.Label(self.frame_viewconvidado, text="Posição (Mesa)", background = branco).place(x=200, y=105)
        self.entry_numviewconvidado = tkbest.Combobox(self.frame_viewconvidado, justify = justificacao, state = leitura)
        self.entry_numviewconvidado.place(x=200, y=130)
        self.btnovo_viewconvidado = tkbest.Button(self.frame_viewconvidado, text="entrar", state = desabilitado, command = self.inserir_entrada)
        self.btnovo_viewconvidado.place(x=20, y=180)

        self.entry_nomeviewconvidado.bind("<Enter>", self.adicionardado_cbnomeconvite)
        self.entry_nomeviewconvidado.bind("<<ComboboxSelected>>", self.selecionardado_tipomesa)
        self.btnovo_viewconvidado.bind("<Enter>", self.validar_novaviewconvidado)

    def vista_standby(self):

        self.frame_viewstandby = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewstandby.place(x = 50, y = 50)


        bt_pdf = tkbest.Button(self.frame_viewstandby, text = "pdf", command = self.pdf_standby)
        bt_pdf.place(x = 315, y = 250)

        cabecalho = ['Nome do convidado', 'Tipo']

        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_tipo()
        self.lista_dadostreeviewstb = objecto.listageral_convites

        total = len(self.lista_dadostreeviewstb)

        tkbest.Label(self.frame_viewstandby, text = str(total) + " Pessoas em standby", background=branco).place(x=20, y=255)


        self.treedataview_stb = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_stb.place(x = 150, y = 60)

        for col in cabecalho:
            self.treedataview_stb.heading(col, text=col)
            self.treedataview_stb.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewstb:
            self.treedataview_stb.insert('', 'end', values=item)

    def vista_activos(self):
        self.frame_viewsactivo = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewsactivo.place(x = 50, y = 50)


        bt_pdf = tkbest.Button(self.frame_viewsactivo, text = "pdf", command = self.pdf_activos)
        bt_pdf.place(x = 460, y = 250)

        cabecalho = ['Nome do convidado', 'Localização', 'Entrada']

        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_activos()
        lista_activos = objecto.listanomesactivos
        self.lista_dadostreeviewact = objecto.listageral_conviteactivos
        objecto.selecionarconvite_todos()
        lista_convidados = objecto.listanomesconvidados

        conjunto_convi = set(lista_convidados)
        conjunto_acti = set(lista_activos)

        conjunto_faltas = conjunto_convi.difference(conjunto_acti)



        activos = len(lista_activos)
        restantes = len(conjunto_faltas)

        tkbest.Label(self.frame_viewsactivo, text=str(activos) + " Pessoas na festa e "+str(restantes)+" a falta", background=branco).place(x=20, y=255)

        self.treedataview_act = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_act.place(x = 150, y = 60)

        for col in cabecalho:
            self.treedataview_act.heading(col, text=col)
            self.treedataview_act.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewact:
            self.treedataview_act.insert('', 'end', values=item)


    def pdf_mesa(self):
        objecto = Relatorio_Convidados
        objecto.mesa()

    def pdf_standby(self):
        objecto = Relatorio_Convidados
        objecto.standby()

    def pdf_activos(self):
        objecto = Relatorio_activos
        objecto.activos()




    def validar_inserirmesa(self, e):
        try:
            if len(self.entry_mesafilemesa.get()) >= 1 and self.entry_mesafilemesa.get().isnumeric():
                self.btnova_filemesa.config(state = "normal")
            else:
                self.btnova_filemesa.config(state= desabilitado)
        except:
            pass


    def adicionardado_pesquisactivo(self, e):
        objecto = Manipulacao_SQL()
        objecto.selecionarlocalizacao_activos()
        lista = objecto.listalocalizacao
        lista.sort()
        self.pesquisaactivo.config(values = lista)




    def adicionar_mesa(self):
        try:
            mesa = self.entry_mesafilemesa.get()
            objecto = Manipulacao_SQL()
            objecto.inserir_mesa(mesa)
            tkinter.messagebox.showinfo("Registo", "Mesa adicionada")
            self.entry_mesafilemesa.delete(0, END)
            self.btnova_filemesa.config(state=desabilitado)
        except:
            tkinter.messagebox.showinfo("Erro", "Mesa já registada")

    def validar_eliminar(self, e):
        if len(self.cb_pesquisafilemesa.get()) >= 1:
            self.bteliminar_filemesa.config(state = "normal")
        else:
            self.bteliminar_filemesa.config(state= desabilitado)

    def eliminar_mesa(self):
        try:
            self.cb_pesquisafilemesa.config(state = "normal")
            mesa = self.cb_pesquisafilemesa.get()
            objecto = Manipulacao_SQL()
            objecto.eliminar_mesa(mesa)

            self.conectar = connect("db_cdf.db")
            self.conectado = self.conectar.cursor()
            self.conectado.execute(""" DELETE FROM Convidado WHERE Mesa = ? """, (mesa,))
            self.conectar.commit()
            tkinter.messagebox.showinfo("Registo", "Mesa eliminada")
            self.cb_pesquisafilemesa.delete(0, END)
            self.cb_pesquisafilemesa.config(state=leitura)
            self.bteliminar_filemesa.config(state = desabilitado)
        except:
            tkinter.messagebox.showinfo("Erro", "Falha inesperada")

    def adicionardado_cbfindmesa(self, e):
        objecto = Manipulacao_SQL()
        objecto.selecionar_mesas()
        lista_dados = objecto.lista_mesas
        self.cb_pesquisafilemesa.config(values = lista_dados)


    def validar_novoconvite(self, e):
        if len(self.entry_nomefileconvidado.get()) >= 4 and len(self.cb_numfileconvidado.get()) >=1:
            self.btnovo_fileconvidado.config(state = "normal")
        else:
            self.btnovo_fileconvidado.config(state= desabilitado)



    def adicionar_convidado(self):
        try:
            self.conectar = connect("db_cdf.db")
            self.conectado = self.conectar.cursor()
            nome = self.entry_nomefileconvidado.get().title()
            mesa = self.cb_numfileconvidado.get()
            termo_pesquisa = """SELECT COUNT(Mesa) FROM Convidado WHERE Mesa = ?"""
            for item in self.conectado.execute(termo_pesquisa, (mesa,)):
                contagem = item[0]
            if contagem <= 10:
                objecto = Manipulacao_SQL()
                objecto.inserir_convidado(nome, mesa)
                tkinter.messagebox.showinfo("Registo", "Convidado adicionado")
                self.entry_nomefileconvidado.delete(0, END)
                self.cb_numfileconvidado.config(state = "normal")
                self.cb_numfileconvidado.delete(0, END)
                self.btnovo_fileconvidado.config(state=desabilitado)
                self.cb_numfileconvidado.config(state=leitura)
            else:
                tkinter.messagebox.showinfo("Excesso", "Mesa cheia")
        except:
            tkinter.messagebox.showinfo("Erro", "Convidado já existe")


    def actualizar_convidado(self):
        tkinter.messagebox.showinfo("Registo", "Actualizado")

    def validar_eliminarconvidado(self, e):
        if len(self.cb_pesquisafileconvidado.get()) >= 4 and self.entry_nomefileconvidado.get() == self.cb_pesquisafileconvidado.get() and len(self.cb_numfileconvidado.get()) >= 1:
            self.bteliminar_fileconvidado.config(state="normal")
        else:
            self.bteliminar_fileconvidado.config(state=desabilitado)

    def eliminar_convidado(self):
        try:
            self.cb_pesquisafileconvidado.config(state = "normal")
            self.cb_numfileconvidado.config(state = "normal")
            nome = self.cb_pesquisafileconvidado.get()
            objecto = Manipulacao_SQL()
            objecto.selecionar_convidados()
            identificacao = objecto.convidado_id[nome]
            objecto.eliminar_convidado(identificacao)
            tkinter.messagebox.showinfo("Registo", "dado eliminado")
            self.cb_pesquisafileconvidado.delete(0, END)
            self.entry_nomefileconvidado.delete(0, END)
            self.cb_numfileconvidado.delete(0, END)
            self.cb_pesquisafileconvidado.config(state = leitura)
            self.cb_numfileconvidado.config(state = leitura)
            self.bteliminar_fileconvidado.config(state = desabilitado)
        except:
            tkinter.messagebox.showinfo("Erro", "Dado não eliminado")

    def adicionardado_cbposicaoconv(self, e):
        objecto = Manipulacao_SQL()
        objecto.selecionar_mesas()
        lista_dados = objecto.lista_mesas
        lista_dados.append("StandBy")
        self.cb_numfileconvidado.config(values = lista_dados)

    def adicionardado_cbnomeconvite(self, e):
        objecto = Manipulacao_SQL()
        objecto.nomes_activos()
        lista_nomesactivos = objecto.nomesactivos
        objecto.selecionar_convidados()
        lista_dados = list(objecto.convidado_id)
        conjunto_a = set(lista_dados)
        conjunto_b = set(lista_nomesactivos)
        conjunto_c = conjunto_a.difference(conjunto_b)
        self.entry_nomeviewconvidado.config(values = list(conjunto_c))


    def find_convidados(self, e):
        objecto = Manipulacao_SQL()
        objecto.selecionar_convidados()
        lista_dados = list(objecto.convidado_id)
        lista_dados.sort()
        self.cb_pesquisafileconvidado.config(values = lista_dados)

    def selecionardado_tipomesa(self, e):
        self.entry_numviewconvidado.config(state = "normal")
        self.entry_numviewconvidado.delete(0, END)
        nome = self.entry_nomeviewconvidado.get()
        objecto = Manipulacao_SQL()
        objecto.selecionar_convidados()
        identificacao = objecto.convidado_id[nome]
        objecto.selecionar_convite(identificacao)
        self.entry_numviewconvidado.insert(0, objecto.mesacorrespondente)
        self.entry_numviewconvidado.config(state=leitura)

    def selecionar_dado_convites(self, e):
        self.bteliminar_fileconvidado.config(state = "normal")
        self.cb_numfileconvidado.config(state = "normal")
        self.cb_numfileconvidado.delete(0, END)
        self.entry_nomefileconvidado.delete(0, END)
        nome = self.cb_pesquisafileconvidado.get()
        objecto = Manipulacao_SQL()
        objecto.selecionar_convidados()
        identificacao = objecto.convidado_id[nome]
        objecto.selecionar_convite(identificacao)
        self.cb_numfileconvidado.insert(0, objecto.mesacorrespondente)
        self.entry_nomefileconvidado.insert(0, nome)
        self.cb_numfileconvidado.config(state=leitura)


    def inserir_entrada(self):
        try:
            nome = self.entry_nomeviewconvidado.get()
            tipo = self.entry_numviewconvidado.get()
            self.entry_numviewconvidado.config(state = "normal")
            objecto = Manipulacao_SQL()
            objecto.inserir_activos(nome, tipo)
            tkinter.messagebox.showinfo("Registo", "Bem vindo ao salão")
            self.entry_nomeviewconvidado.config(state = "normal")
            self.entry_nomeviewconvidado.delete(0, END)
            self.entry_numviewconvidado.delete(0, END)
            self.entry_nomeviewconvidado.config(state = leitura)
            self.btnovo_viewconvidado.config(state=desabilitado)
            self.entry_numviewconvidado.config(state= leitura)
        except:
            tkinter.messagebox.showinfo("Falha", "Um erro inesperado ocorreu")

    def validar_novaviewconvidado(self, e):
        if len(self.entry_nomeviewconvidado.get()) >= 4 and len(self.entry_numviewconvidado.get()) >=1:
            self.btnovo_viewconvidado.config(state="normal")
        else:
            self.btnovo_viewconvidado.config(state=desabilitado)



sistema_principal = Tk()
sistema_principal["bg"] = azul
sistema_principal.title("Sistema de Gestão de Convites")
sistema_principal.iconbitmap(r"Imagens/icon.ico")
casamento = CDF(sistema_principal)
sistema_principal.mainloop()




