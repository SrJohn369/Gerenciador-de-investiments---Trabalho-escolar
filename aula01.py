from tkinter import *

root = Tk()  # criar janela


class Aplication():

    def __init__(self):
        self.root = root
        self.tela()  # chamar função tela
        self.frames_de_tela()
        root.mainloop()  # criar looping para manter janela aberta

    def tela(self):
        self.root.title('Cadastro de clientes')
        self.root.configure(background='#10246a')  # backgraund da tela
        self.root.geometry('722x588')  # dimensões da janela
        self.root.resizable(True, True)  # para tela responsiva (vertical, horizontal)
        self.root.maxsize(width=900, height=700)  # tamanho máximo na (largula, altura) da tela
        self.root.minsize(width=400, height=300)  # tamanho mínimo na (largura, altura) da tela

    def frames_de_tela(self):  # classe para frames (espaços na tela)
        self.frame_1 = Frame(self.root, bd=4, bg='white',
                             highlightbackground='#2553F7', highlightthickness=6)
        # place pack grid  # tipos de widgets
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96,
                           relheight=0.5)  # relx: numeração de 0: esquerdo a 1: direito (horizontal)
        self.frame_2 = Frame(self.root, bd=6, bg='white',
                             highlightbackground='#2553F7', highlightthickness=10)
        self.frame_2.place(relx=0.02, rely=0.5, relwigth=0.96, relheight=0.46)


Aplication()
