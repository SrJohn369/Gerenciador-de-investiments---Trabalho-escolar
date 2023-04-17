from tkinter import *
import tkinter as tk


class JanelaInicio:
    cores = ["#F26B8F",
             "#302A59",
             "#353A8C",
             "#049DD9",
             "#F24444",
             "#F2F2F2"]

    def __init__(self):
        #   CRIANDO VARIAVEIS PARA JANELA E FRAME PRINCIPAL
        self.root = tk.Tk()

        #   CONFIGURANDO JANELA
        self.root.geometry('750x400')
        self.root.title('Plataforma de Investimentos')
        self.root.resizable(False, False)

        #   FUNÇÕES DE INÍCIO
        self.frame_principal()
        self.seja_bem_vindoA()

        #   MATEM A JANELA ATIVA
        self.root.mainloop()

    def chamada(self, func):
        """Funções de chamada:
        1 - Cadastrar"""
        self.inicio_frame.destroy()
        self.frame_Tela_Inicio()

        if func == 1:
            self.cadastrar()

    def frame_principal(self):
        #   CRIANDO VARIAVEIS PARA FRAME PRINCIPAL
        self.options_frame = tk.Frame(self.root, bg='#02347c')

        #   CONFIGURANDO FRAME PRINCIPAL
        self.options_frame.pack(side=tk.LEFT)
        self.options_frame.pack_propagate(False)
        self.options_frame.configure(width=150, height=400)

        #   CRIANDO VARIAVEIS PARA BOTOES E LINHA
        # |---label---|
        title_op = tk.Label(self.options_frame, text='Menu', font=('KacstOffice', '15'), bg='#02347c', fg='white')
        l_linha = Label(self.options_frame, text='', width=700, height=1, anchor=NW, font=' Ivy 1 ', bg='#2fc7f4',
                        highlightbackground='#F2F2F2')
        # |---botoes---|
        cad_btn = tk.Button(self.options_frame, text='Cadastrar', font=('KacstOffice', '10'), bg='#2fc7f4',
                            command=lambda: self.chamada(1))
        acess = tk.Button(self.options_frame, text='Investimentos', font=('KacstOffice', '10'), bg='#2fc7f4')

        #   CONFIGURANDO FRAME PRINCIPAL
        # |---botoes---|
        cad_btn.pack(pady=130, anchor='center')
        acess.place(x=13, y=200)
        # |---linha---|
        l_linha.place(x=0, y=70)
        title_op.place(x=45, y=20)

    def frame_Tela_Inicio(self):
        #   CRIANDO FRAME DE TELA DE INICIO
        self.inicio_frame = Frame(self.root, background='black')

        #   CONFIGURANDO FRAME
        self.inicio_frame.place(rely=0, relx=0.200, relheight=1, relwidth=1)

    def seja_bem_vindoA(self):
        #   CHAMANDO FRAME DE TELA INICIAL
        self.frame_Tela_Inicio()
        # Foto bg
        self.imagem = tk.PhotoImage(file='b3.png')
        self.imagem.subsample(1,1)
        self.imagem_fundo = Label(self.inicio_frame, image=self.imagem)
        self.imagem_fundo.place(x=180, y=140, relwidth=0.333, relheight=0.28)

        # label
        bem_vindo = tk.Label(self.inicio_frame, text='SEJA BEM-VINDO(A)', font=('KacstOffice', '15'), bg='black',
                             fg='#2fc7f4')
        bem_vindo.place(x=202, y=20)



JanelaInicio()
