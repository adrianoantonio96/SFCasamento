from tkinter import *
from tkinter import ttk
from Dados import *
from Dados_SQLite import Manipulacao_SQL

class Janela_GeralD(object):
    def __init__(self, janela_geral):
        self.janela_geral = janela_geral
        self.janela_geral.geometry("300x205")
        self.janela_geral.title("Casamento - Info")
        self.janela_geral["bg"] = azul
        self.janela_geral.resizable(False, False)
        self.janela_geral.iconbitmap(r"Imagens/icon.ico")
        ttk.Label(janela_geral, text = "Noivo e Noiva", font = fonte, background = azul, foreground = branco).place(x = 10, y = 10)
        self.entry_nomenoivos = ttk.Entry(janela_geral, width = 35, font = fonte, justify = justificacao)
        self.entry_nomenoivos.place(x = 10, y = 35)
        self.entry_nomenoivos.focus_force()
        ttk.Label(janela_geral, text = "Data", font = fonte, background = azul, foreground = branco).place(x = 10, y = 65)
        self.entry_data = ttk.Entry(janela_geral, font = fonte, justify = justificacao)
        self.entry_data.place(x = 10, y = 92)
        self.entry_data.insert(0, "2018-05-18")
        self.inserir = ttk.Button(janela_geral, text = "inserir", state = desabilitado, command = self.inserir_dado)
        self.inserir.place(x = 55, y = 140)
        self.inserir.bind("<Enter>", self.validar_inserir)

    def validar_inserir(self, e):
        if len(self.entry_nomenoivos.get()) >= 4 and len(self.entry_data.get()) == 10:
            self.inserir.config(state = "normal")
        else:
            self.inserir.config(state = desabilitado)


    def inserir_dado(self):
        try:
            noivo = self.entry_nomenoivos.get()
            data = self.entry_data.get()
            objecto = Manipulacao_SQL()
            objecto.inserir_informacao(noivo, data)
            self.janela_geral.destroy()
        except:
            pass












def iniciar_janela():
    janela_geral = Tk()
    janela_geralinfo = Janela_GeralD(janela_geral)
    janela_geral.mainloop()


