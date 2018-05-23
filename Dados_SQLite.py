from sqlite3 import *
from time import *
class Manipulacao_SQL(object):
    def __init__(self):
        """Classe que cuida das queries' em sqlite, isso é muita lógica pessoal
        Não foi usado neste modulo nenhuma instrução inner, é tudo com base na criação"""
        self.iniciar_db()

    def iniciar_db(self):
        try:
            self.conectar = connect("db_cdf.db")
            self.conectado = self.conectar.cursor()
        except:
            pass

    def inserir_mesa(self, mesa):
        self.conectado.execute("""INSERT INTO Mesa(
        Mesa) VALUES (?)""", (mesa))
        self.conectar.commit()

    def eliminar_mesa(self, mesa):
        self.conectado.execute(""" DELETE FROM Mesa WHERE Mesa = ? """, (mesa,))
        self.conectar.commit()

    def eliminar_convidado(self, identificacao):
        self.conectado.execute(""" DELETE FROM Convidado WHERE Identificacao = ? """, (identificacao,))
        self.conectar.commit()

    def selecionar_mesas(self):
        self.lista_mesas = list()
        termo_pesquisa = """SELECT * FROM ViewMesa_All"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.lista_mesas.append(int(item[0]))


    def inserir_convidado(self, nome, mesa):
        termo_pesquisa = """SELECT COUNT(Mesa) FROM Convidado WHERE Mesa = ?"""
        for item in self.conectado.execute(termo_pesquisa, (mesa, )):
            contagem = item[0]
        if mesa == "StandBy":
            self.conectado.execute("""INSERT INTO Convidado(
            Nome,
            Tipo) VALUES (?, ?)""", (nome, mesa))
            self.conectar.commit()
        else:
            self.conectado.execute("""INSERT INTO Convidado(
            Nome,
            Mesa) VALUES (?, ?)""", (nome, mesa))
            self.conectar.commit()

    def selecionar_convidados(self):
        self.id_convidado = {}
        self.convidado_id = {}
        termo_pesquisa = """SELECT * FROM ViewConvidado_All"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.id_convidado[item[0]] = item[1]
            self.convidado_id[item[1]] = item[0]

    def selecionar_convite(self, identificacao):
        termo_pesquisa = """SELECT Mesa, Tipo FROM Convidado WHERE Identificacao = ?"""
        for item in self.conectado.execute(termo_pesquisa, (identificacao, )):
            if item[0] == None:
                self.mesacorrespondente = item[1]
            elif item[1] == None:
                self.mesacorrespondente = item[0]

    def selecionarconvite_tipo(self):
        self.listageral_convites = list()
        termo_pesquisa = """SELECT Nome, Tipo FROM Convidado WHERE Tipo = ?"""
        for item in self.conectado.execute(termo_pesquisa, ("StandBy", )):
            self.listageral_convites.append(item)

    def selecionarlocalizacao_activos(self):
        self.listalocalizacao = list()
        termo_pesquisa = """SELECT DISTINCT Localizacao FROM Activos"""
        for item in self.conectado.execute(termo_pesquisa, ):
            pass
            self.listalocalizacao.append(item[0])


    def selecionarnomes_activos(self, localizacao):
        self.listanomes = list()
        termo_pesquisa = """SELECT Nome FROM Activos WHERE Localizacao = ?"""
        for item in self.conectado.execute(termo_pesquisa, (localizacao, )):
            self.listanomes.append(item)




    def selecionarconvite_todos(self):
        self.listanomesconvidados = list()
        termo_pesquisa = """SELECT Nome FROM Convidado"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.listanomesconvidados.append(item[0])

    def selecionarconvite_mesa(self):
        self.listageral_convitemesa = list()
        termo_pesquisa = """SELECT Nome, Mesa FROM Convidado WHERE Tipo IS NULL"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.listageral_convitemesa.append(item)



    def inserir_activos(self, nome, localizacao):
        data = "2018-05-16"
        entrada = strftime("%H:%M:%S")
        self.conectado.execute("""INSERT INTO Activos(
        Nome,
        Localizacao,
        Entrada,
        Data) VALUES (?, ?, ?, ?)""", (nome, localizacao, entrada, data))
        self.conectar.commit()

    def selecionarconvite_activos(self):
        self.listageral_conviteactivos = list()
        self.listanomesactivos = list()
        termo_pesquisa = """SELECT Nome, Localizacao, Entrada FROM Activos"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.listageral_conviteactivos.append(item)
            self.listanomesactivos.append(item[0])

    def nomes_activos(self):
        self.nomesactivos = list()
        termo_pesquisa = """SELECT Nome FROM Activos"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.nomesactivos.append(item[0])


    def inserir_informacao(self, noivo, data):
        self.conectado.execute("""INSERT INTO Informacao(
        Noivos,
        Data) VALUES (?, ?)""", (noivo, data))
        self.conectar.commit()

    def comparar_informacao(self):
        self.comparacao = int()
        termo_pesquisa = """SELECT COUNT(Noivos), Noivos, Data FROM Informacao"""
        for item in self.conectado.execute(termo_pesquisa, ):
            self.comparacao = item[0]
            self.noivos = item[1]
            self.data = item[2]



