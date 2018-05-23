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
        """Classe principal do sistema, onde estão os widgets e é aqui que todos os modulos se relacionam"""
        self.janela_principal = janela_principal
        self.janela_principal.state("zoomed")#Janela em tamanho máximo
        self.janela_principal.resizable(False, False)#Sem redimensionamento
        self.menu_janela()
        self.janela_principal.protocol("WM_DELETE_WINDOW", self.fechar_janelaprincipal)#Evento de fecho acidental da janela
        self.pesquisa_lateral()

    def fechar_janelaprincipal(self):
        """Metodo que faz com não se feche a janela principal por acidente"""
        if tkinter.messagebox.askokcancel("Sair", "Deseja sair?") == True:
             self.janela_principal.destroy()

    def menu_janela(self):
        """Menu horizontal do programa, opções de facilitação para o usúario"""
        self.menubar = Menu(self.janela_principal)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Mesa", command = self.reg_mesa)
        filemenu.add_command(label="Convidado", command = self.validar_inserir_convidado)
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
        """Metodo que cuida da da criação e empacotamento dos widgets do frame superior
        que garante que só o proprietário do sistema pode inserir convidado, ou seja, metodo que bloqueia
        a opção de inserção de convidado"""
        self.frame_superiorpasse = Frame(self.janela_principal, width = 300, height = 40, relief = SOLID, bg = branco)
        self.frame_superiorpasse.place(x = 50, y = 4)
        self.entry_password = tkbest.Entry(self.frame_superiorpasse, justify = justificacao, show = "*")
        self.entry_password.place(x = 20, y = 10)
        self.entry_password.focus_force()
        bt_validarpasse = tkbest.Button(self.frame_superiorpasse, text = "validar", command = self.validar_password).place(x = 150, y = 8)
        try: #ocultação do frame de inserção de convidado sempre que que este (Frame superior) é chamado
            self.frame_fileconvidado.place_forget()
        except:
            pass

    def pesquisa_lateral(self):
        """Metodo de criação e empacotamento do label pesquisar activos e da sua caixa de pesquisa"""
        tkbest.Label(self.janela_principal, text="PESQUISAR ACTIVOS", background=azul, font=fonte).place(x=800, y=20)
        self.pesquisaactivo = tkbest.Combobox(self.janela_principal, justify = justificacao, state = leitura, font = fonte, width = 35)
        self.pesquisaactivo.place(x = 800, y = 50)
        #####Eventos de bind individual do sistema
        #Evento que insere as mesas e standby activas na caixa de pesquisa lateral direita da janela principal
        self.pesquisaactivo.bind("<Enter>", self.adicionardado_pesquisactivo)
        #Evento que define o que acontece quando um dado da caixa de pesquisa lateral esquerda é selecionado
        self.pesquisaactivo.bind("<<ComboboxSelected>>", self.frame_lateralactivos)

    def frame_lateralactivos(self, e):
        """Frame lateral direito que é chamado quando um dado da caixa de pesquisa lateral direita é selecionado"""
        self.frame_lateral = Frame(self.janela_principal, width = 300 ,height = 600, relief = "solid", bg = branco)
        self.frame_lateral.place(x = 800, y = 90)
        #Cabeçalho do treeview que mostra os convidados activos, de forma agrupada por posição
        cabecalho = ['Nome do convidado']
        objecto = Manipulacao_SQL()
        localizacao = self.pesquisaactivo.get()
        objecto.selecionarnomes_activos(localizacao)
        self.lista_dadostreeviewstb = objecto.listanomes #Lista guarda os nomes dos convidados activos de acordo a forma de agrupamento
        #Criação do treeview
        self.treedataview_stb = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_stb.place(x = 846, y = 130)
        #Colocação dos dados da lista que guarda os nomes no treeview
        for col in cabecalho:
            self.treedataview_stb.heading(col, text=col)
            self.treedataview_stb.column(col, anchor='center', width=200)
        for item in self.lista_dadostreeviewstb:
            self.treedataview_stb.insert('', 'end', values=item)

    def reg_mesa(self):
        """Metodo que trata da criação e empacotamento dos widgets do frame de inserção de mesa"""
        self.frame_filemesa = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_filemesa.place(x = 50, y = 50)
        self.cb_pesquisafilemesa = tkbest.Combobox(self.frame_filemesa, justify = justificacao, state = leitura, font = fonte, width = 35)
        self.cb_pesquisafilemesa.place(x = 20, y = 40)
        tkbest.Label(self.frame_filemesa, text="PESQUISAR", background=branco, font = fonte).place(x=330, y= 40)
        tkbest.Label(self.frame_filemesa, text="Nº da Mesa", background = branco).place(x=20, y=105)
        self.entry_mesafilemesa = tkbest.Entry(self.frame_filemesa, justify = justificacao)
        self.entry_mesafilemesa.place(x = 20, y = 130)
        #Frame que agrega os botões de CRUD
        frame_btsfilemesa = Frame(self.frame_filemesa, width = 300, height = 40, relief = "solid", bg = azul)
        frame_btsfilemesa.place(x = 20, y = 200)
        self.btnova_filemesa = tkbest.Button(frame_btsfilemesa, text = "novo", state = desabilitado, command = self.adicionar_mesa)
        self.btnova_filemesa.place(x = 20, y = 6)
        self.bteliminar_filemesa = tkbest.Button(frame_btsfilemesa, text = "eliminar", state = desabilitado, command = self.eliminar_mesa)
        self.bteliminar_filemesa.place(x = 200, y = 6)

        ###Eventos
        self.entry_mesafilemesa.focus_force()
        #Evento que trata da inserção de dados no combobox de pesquisa do frame de inserção de mesa
        self.cb_pesquisafilemesa.bind("<Enter>", self.adicionardado_cbfindmesa)
        #Evento que bloqueia o botão eliminar do frame de inserção de mesa caso algo esteja incorrecto
        self.bteliminar_filemesa.bind("<Enter>", self.validar_eliminarmesa)
        #Evento que bloqueia o botão de inserção do frame de inserção de mesa caso os dados não estejam bem preenchidos
        self.btnova_filemesa.bind("<Enter>", self.validar_inserirmesa)

    def reg_convidado(self):
        """Metodo que trata da criação e empacotamento dos widgets do frame de inserção de convidados"""
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

        ###Eventos
        self.entry_nomefileconvidado.focus_force()
        #Evento que faz a inserção de dados no combobox de inserção de posição do convidado na festa
        self.cb_numfileconvidado.bind("<Enter>", self.adicionardado_cbposicaoconv)
        #Evento que valida os campos de preenchimento do frame de inserção de convidado para assim activar o botão novo
        self.btnovo_fileconvidado.bind("<Enter>", self.validar_novoconvite)
        #Evento que faz a inserção do nome dos convidados na caixa de pesquisa do frame de inserção de convidados
        self.cb_pesquisafileconvidado.bind("<Enter>", self.find_convidados)
        #Evento que define o que acontece quando um dado desse combobox (caixa de pesquisa do frame de inserção de convidado) é selecionado
        self.cb_pesquisafileconvidado.bind("<<ComboboxSelected>>", self.selecionar_dado_convites)
        #Evento que bloqueia o botão eliminar do frame de inserção de convidado caso algo esteja incorrecto
        self.bteliminar_fileconvidado.bind("<Enter>", self.validar_eliminarconvidado)

    def vista_convidado(self):
        """Metodo que trata da criação e empacotamento dos widgets do frame permissão dos convidados a festa"""
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

        ###Eventos
        #Evento que faz inserção do nome dos convidados a caixa de inserção de nome do frame de permissão de convidados a festa
        self.entry_nomeviewconvidado.bind("<Enter>", self.adicionardado_cbnomeconvite)
        #Evento que define o que acontece quando um dado da caixa de inserção de nome do frame de permissão de convidados é selecionado
        self.entry_nomeviewconvidado.bind("<<ComboboxSelected>>", self.selecionardado_tipomesa)
        #Evento que bloqueia o botão de permissão caso algum dado esteja incorrecto
        self.btnovo_viewconvidado.bind("<Enter>", self.validar_novaviewconvidado)

    def vista_mesa(self):
        """Metodo que trata da inserção e empacotamento do frame de visualição de convidados nas mesas"""
        self.frame_viewmesa = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewmesa.place(x = 50, y = 50)
        bt_pdf = tkbest.Button(self.frame_viewmesa, text = "pdf", command = self.pdf_mesa)
        bt_pdf.place(x = 315, y = 250) #botão de chamada de relatório dos convidados nas mesas
        #Cabeçalho do treeview do frame de visualização de convidados na mesa
        cabecalho = ['Nome do convidado', 'Nº da Mesa']
        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_mesa()
        self.lista_dadostreeviewmesa = objecto.listageral_convitemesa
        total = len(self.lista_dadostreeviewmesa)
        tkbest.Label(self.frame_viewmesa, text = str(total) + " Pessoas nas mesas", background=branco).place(x=20, y=255)
        #Criação e empacotamento do treeview de visualização dos convidados na mesa do sistema
        self.treedataview_mesa = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_mesa.place(x = 150, y = 60)
        #Inserção dos dados da lista no treeview de visualização dos convidados na mesa do sistema
        for col in cabecalho:
            self.treedataview_mesa.heading(col, text=col)
            self.treedataview_mesa.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewmesa:
            self.treedataview_mesa.insert('', 'end', values=item)

    def vista_standby(self):
        """Metodo que trata da criação e empacotamento dos widgets do frame de visualização de convidados em standby"""
        self.frame_viewstandby = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewstandby.place(x = 50, y = 50)
        #Botão de chamada de relatório do equivalente frame
        bt_pdf = tkbest.Button(self.frame_viewstandby, text = "pdf", command = self.pdf_standby)
        bt_pdf.place(x = 315, y = 250)
        #Cabeçalho do treeview de visualização de convidados em standby
        cabecalho = ['Nome do convidado', 'Tipo']
        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_tipo()
        self.lista_dadostreeviewstb = objecto.listageral_convites #Lista que guarda o nome dos convidados em standby
        total = len(self.lista_dadostreeviewstb)
        tkbest.Label(self.frame_viewstandby, text = str(total) + " Pessoas em standby", background=branco).place(x=20, y=255)
        #Criação e empacotamento do treeview de visualização de convidados em standby
        self.treedataview_stb = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_stb.place(x = 150, y = 60)
        #Inserção dos dados guardados na lista no treeview de visualização de convidados em standby
        for col in cabecalho:
            self.treedataview_stb.heading(col, text=col)
            self.treedataview_stb.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewstb:
            self.treedataview_stb.insert('', 'end', values=item)

    def vista_activos(self):
        self.frame_viewsactivo = Frame(self.janela_principal, width = 650 ,height = 450, relief = "solid", bg = branco)
        self.frame_viewsactivo.place(x = 50, y = 50)
        #Chamada do relatório dos convidados activos do sistema
        bt_pdf = tkbest.Button(self.frame_viewsactivo, text = "pdf", command = self.pdf_activos)
        bt_pdf.place(x = 460, y = 250)
        #Cabeçalho do treeview de visualização dos convidados activos (no salão)
        cabecalho = ['Nome do convidado', 'Localização', 'Entrada']
        objecto = Manipulacao_SQL()
        objecto.selecionarconvite_activos()
        lista_activos = objecto.listanomesactivos
        self.lista_dadostreeviewact = objecto.listageral_conviteactivos
        objecto.selecionarconvite_todos()
        lista_convidados = objecto.listanomesconvidados
        #Operação com conjuntos (matemática
        conjunto_convi = set(lista_convidados) #conjunto convidados
        conjunto_acti = set(lista_activos) #Conjunto convidados activos (no salão)
        #Operação matemática de diferença de conjuntos, ou seja, insira na conjunto faltas todos os dados que estiverem no conjunto convidados e não estiverem no conjunto activos
        conjunto_faltas = conjunto_convi.difference(conjunto_acti)
        #Tamanho de cada conjunto para assim se saber quantos convidados estão presentes e quantos não
        activos = len(lista_activos)
        restantes = len(conjunto_faltas)
        tkbest.Label(self.frame_viewsactivo, text=str(activos) + " Pessoas na festa e "+str(restantes)+" a falta", background=branco).place(x=20, y=255)
        #Criação e empacotamento do treeview de visualização dos convidados activos (no salão)
        self.treedataview_act = tkbest.Treeview(columns=cabecalho, show="headings")
        self.treedataview_act.place(x = 150, y = 60)
        #Inserção dos dados guardados na lista no treeview de visualização de convidados activos
        for col in cabecalho:
            self.treedataview_act.heading(col, text=col)
            self.treedataview_act.column(col, anchor='center', width=145)
        for item in self.lista_dadostreeviewact:
            self.treedataview_act.insert('', 'end', values=item)

    def validar_password(self):
        """Metodo que valida o dado inserido na caixa de texto do frame superior para assim dar ou não acesso ao
            usuário de inserir convidado"""
        if self.entry_password.get() == "amorepaz":
            self.frame_superiorpasse.place_forget()
            self.reg_convidado()
        else:
            tkinter.messagebox.showinfo("Erro", "Não tem permissão para adicionar convidado")

    def geral_info(self):
        """Metodo que define que o sistema só poderá gerir um casamento de cada vez"""
        try:
            objecto = Manipulacao_SQL()
            objecto.comparar_informacao()
            informacao = objecto.comparacao
            if informacao == 0:
                Janela_Geral.iniciar_janela()
            else:
                tkinter.messagebox.showinfo("Excesso", "Um casamento já foi registado")
        except:
            pass

    def sobre_info(self):
        """Metodo que mostra informação sobre o programa e o desenvolvedor"""
        tkinter.messagebox.showinfo("SFC v.1", "Desenvolvedor: Adriano António"+"\n"+"Contacto: 922-961-983\n"+"Email: adriano.antonio@outlook.pt ou www.facebook.com\emmer.driizzi\n"+"Desenvolvedor Python - 2018")

    def pdf_mesa(self):
        """Metodo que chamada de relatório pdf de convidados sentados na mesa"""
        try:
            objecto = Relatorio_Convidados
            objecto.mesa()
        except:
            pass

    def pdf_standby(self):
        """Metodo que chamada de relatório pdf de convidados sentados em standby"""
        try:
            objecto = Relatorio_Convidados
            objecto.standby()
        except:
            pass

    def pdf_activos(self):
        """Metodo que chamada de relatório pdf de convidados sentados activos"""
        try:
            objecto = Relatorio_activos
            objecto.activos()
        except:
            pass

    def validar_inserirmesa(self, e):
        """Metodo que valida o botão de inserção do frame de inserção de mesa consuante a condição aplicada a baixo"""
        #se a informação contida no caixa de inserçao de mesa for maior que 1 e for numerico então active o botão de inserção
        if len(self.entry_mesafilemesa.get()) >= 1 and self.entry_mesafilemesa.get().isnumeric():
            self.btnova_filemesa.config(state = "normal")
        else:
            #Senão, desactive-o
            self.btnova_filemesa.config(state= desabilitado)


    def adicionardado_pesquisactivo(self, e):
        """Metodo que insere uma lista de dados de posições activas na caixa de pesquisa lateral direita"""
        try:
            objecto = Manipulacao_SQL()
            objecto.selecionarlocalizacao_activos()
            lista = objecto.listalocalizacao
            lista.sort() #Organização crescente da lista
            self.pesquisaactivo.config(values = lista)
        except:
            pass

    def adicionar_mesa(self):
        """Metodo de inserção de mesa no sistema"""
        try:
            mesa = self.entry_mesafilemesa.get()
            objecto = Manipulacao_SQL()
            objecto.inserir_mesa(mesa)
            tkinter.messagebox.showinfo("Registo", "Mesa adicionada")
            self.entry_mesafilemesa.delete(0, END)
            self.btnova_filemesa.config(state=desabilitado)
        except:
            tkinter.messagebox.showinfo("Erro", "Mesa já registada")

    def validar_eliminarmesa(self, e):
        """Metodo que bloqueia o botão eliminar do frame de inserção de mesa caso algo esteja incorrecto"""
        if len(self.cb_pesquisafilemesa.get()) >= 1:
            self.bteliminar_filemesa.config(state = "normal")
        else:
            self.bteliminar_filemesa.config(state= desabilitado)

    def eliminar_mesa(self):
        """Metodo que cuida da eliminação de uma determinada mesa, se uma mesa é eliminada, os convidados dela também são"""
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
            #Essa excepção é chamada se alguma coisa correr mal, nada em especifíco
            tkinter.messagebox.showinfo("Erro", "Falha inesperada")

    def adicionardado_cbfindmesa(self, e):
        """Metodo que faz a inserção de mesas já cadastradas na caixa de pesquisa do frame de inserção de mesa"""
        try:
            objecto = Manipulacao_SQL()
            objecto.selecionar_mesas()
            lista_dados = objecto.lista_mesas
            self.cb_pesquisafilemesa.config(values = lista_dados)
        except:
            pass


    def validar_novoconvite(self, e):
        """Metodo que valida o botão de inserção de novo convite do frame de inserção de convidados"""
        if len(self.entry_nomefileconvidado.get()) >= 4 and len(self.cb_numfileconvidado.get()) >=1:
            self.btnovo_fileconvidado.config(state = "normal")
        else:
            self.btnovo_fileconvidado.config(state= desabilitado)



    def adicionar_convidado(self):
        """Metodo que trata da inserção de convidados
        Lembrar que os convidados não podem ter o mesmo nome"""
        try:
            self.conectar = connect("db_cdf.db")
            self.conectado = self.conectar.cursor()
            nome = self.entry_nomefileconvidado.get().title()
            mesa = self.cb_numfileconvidado.get()
            #Bloqueio de inserção de uma determinada mesa quando ela atingir 10 lugares ocupados
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
                #Quando o número de convidado em uma determinada mesa tentar ultrapassar os 10, essa será a informação
                tkinter.messagebox.showinfo("Excesso", "Mesa cheia")
        except:
            #Prevendo que o único erro seria a inserção de um convidado já existente, essa será a excepção
            tkinter.messagebox.showinfo("Erro", "Convidado já existe")

    def actualizar_convidado(self):
        """Metodo que cuida da actualização dos dados de um determinado convidado"""
        tkinter.messagebox.showinfo("Registo", "Actualizado")

    def validar_eliminarconvidado(self, e):
        """Metodo que bloqueia o botão eliminar do frame de inserção de convidado caso algo esteja errado, seguindo a condição"""
        if len(self.cb_pesquisafileconvidado.get()) >= 4 and self.entry_nomefileconvidado.get() == self.cb_pesquisafileconvidado.get() and len(self.cb_numfileconvidado.get()) >= 1:
            self.bteliminar_fileconvidado.config(state="normal")
        else:
            self.bteliminar_fileconvidado.config(state=desabilitado)

    def eliminar_convidado(self):
        """Metodo que elimina um determinado convidado do sistema"""
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
            #Informação levantada quando não se conseguir eliminar, nada em espicifíco
            tkinter.messagebox.showinfo("Erro", "Dado não eliminado")

    def adicionardado_cbposicaoconv(self, e):
        """Metodo que insere dados na caixa de inserção de posição de convidado no frame de inserção de convidados"""
        try:
            objecto = Manipulacao_SQL()
            objecto.selecionar_mesas()
            lista_dados = objecto.lista_mesas
            lista_dados.append("StandBy") #Adiciona a opção de standby para convidados não previlegiados
            self.cb_numfileconvidado.config(values = lista_dados)
        except:
            pass

    def adicionardado_cbnomeconvite(self, e):
        """Metodo que oculta do frame de permissão de convidados os convidados já activos (no salão)"""
        try:
            objecto = Manipulacao_SQL()
            objecto.nomes_activos()
            lista_nomesactivos = objecto.nomesactivos
            objecto.selecionar_convidados()
            lista_dados = list(objecto.convidado_id)
            conjunto_a = set(lista_dados)
            conjunto_b = set(lista_nomesactivos)
            #Atribua ao conjunto c todos os elementos que estão no conjunto a e não no c, trazuzindo
            #Deixe disponível no frame de permissão de convidados todos os convidados que não estão no salão
            conjunto_c = conjunto_a.difference(conjunto_b)
            self.entry_nomeviewconvidado.config(values = list(conjunto_c))
        except:
            pass

    def find_convidados(self, e):
        """Metodo que insere a caixa de pesquisa de convidados do frame de inserção de convite todos os convidados"""
        try:
            objecto = Manipulacao_SQL()
            objecto.selecionar_convidados()
            lista_dados = list(objecto.convidado_id)
            lista_dados.sort()#Organização da lista
            self.cb_pesquisafileconvidado.config(values = lista_dados)
        except:
            pass

    def selecionardado_tipomesa(self, e):
        """Metodo que insere à caixa de posição do frame de permissão de entrada de convidados a posição de um determinado convidado"""
        try:
            self.entry_numviewconvidado.config(state = "normal")
            self.entry_numviewconvidado.delete(0, END)
            nome = self.entry_nomeviewconvidado.get()
            objecto = Manipulacao_SQL()
            objecto.selecionar_convidados()
            identificacao = objecto.convidado_id[nome]
            objecto.selecionar_convite(identificacao)
            self.entry_numviewconvidado.insert(0, objecto.mesacorrespondente)
            self.entry_numviewconvidado.config(state=leitura)
        except:
            pass

    def selecionar_dado_convites(self, e):
        """Metodo que insere..."""
        try:
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
        except:
            pass


    def inserir_entrada(self):
        """Metodo que trata da entrada de um determinado convidado ao salão"""
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
            #Excepção levantada, nada em especifico
            tkinter.messagebox.showinfo("Falha", "Um erro inesperado ocorreu")

    def validar_novaviewconvidado(self, e):
        """Metodo que bloqueia o botão de inserção de novo convidado caso algo não esteja bem inserido"""
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