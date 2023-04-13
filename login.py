from tkinter import *
from tkinter import messagebox


class TelaLogin:
    cores = ["#f0f3f5",
             "#feffff",
             "#3fb5a3",
             "#38576b",
             "#403d3d"]
    # Preta / black
    # branca / white
    # verde / green
    # valor / value
    # letra / letters]
    credenciais = ['joão', '123456789']

    def janela_inicio(self):
        # criando janela
        self.janela = Tk()
        self.janela.title('Gerenciador de Investimentos')
        self.janela.geometry('522x488')
        self.janela.configure(background=self.cores[1])
        self.janela.resizable(width=False, height=False)
        self.janela.iconbitmap("din2.ico")
        self.tela_login()

        self.janela.mainloop()

    def chamada(self, funcao: int):
        #   Destroi os frames anteriores
        self.frame_cima.destroy()
        self.frame_baixo.destroy()

        if funcao == 1:
            self.cadastro_usuario()
        elif funcao == 2:
            self.tela_login()

    # dividindo janela
    def frameCima(self):
        self.frame_cima = Frame(self.janela, width=310, height=50, bg=self.cores[3], relief='flat')
        self.frame_cima.place(relx=0, rely=0, relwidth=1, relheight=1)

    def frameBaixo(self):
        self.frame_baixo = Frame(self.janela, width=310, height=250, bg=self.cores[1], relief='flat')
        self.frame_baixo.place(relx=0, rely=0.2, relwidth=1, relheight=1)

    def tela_login(self):
        self.frameCima()
        self.frameBaixo()

        l_nome_login = Label(self.frame_cima, text='LOGIN', anchor=NE, font='Ivy 25', bg=self.cores[3],
                             fg=self.cores[1])
        l_nome_login.place(x=10, y=30)

        l_linha = Label(self.frame_cima, text='', width=600, anchor=NW, font='Ivy 1', bg=self.cores[2],
                        fg=self.cores[1])
        l_linha.place(x=0, y=90)

        l_nome = Label(self.frame_baixo, text='Nome *', anchor=NW, font='Ivy 15', bg=self.cores[1], fg=self.cores[4])
        l_nome.place(x=10, y=20)
        self.e_nome = Entry(self.frame_baixo, width=35, justify='left', font=("", 15), highlightthickness=1,
                            relief='solid')
        self.e_nome.place(x=10, y=60)

        l_pass = Label(self.frame_baixo, text='Senha *', anchor=NW, font='Ivy 15', bg=self.cores[1], fg=self.cores[4])
        l_pass.place(x=10, y=95)
        self.e_pass = Entry(self.frame_baixo, width=35, justify='left', show='*', font=("", 15), highlightthickness=1,
                            relief='solid')
        self.e_pass.place(x=10, y=140)

        # Botões
        b_confirmar = Button(self.frame_baixo, command=lambda: self.verificar_senha(), text='Entrar', width=15,
                             height=1,
                             font='Ivy 8 bold', bg=self.cores[0], fg=self.cores[4], relief=RAISED, overrelief=RIDGE)
        b_confirmar.place(x=10, y=190)

        b_cadastro = Button(self.frame_baixo, command=lambda: self.chamada(1), text='Cadastrar', width=15, height=1,
                            font='Ivy 8 bold', bg=self.cores[0], fg=self.cores[4], relief=RAISED, overrelief=RIDGE)
        b_cadastro.place(x=381, y=190)

    # função para verificar senha
    def verificar_senha(self):
        nome = self.e_nome.get()
        senha = self.e_pass.get()
        if self.credenciais[0] == nome and self.credenciais[1] == senha:
            messagebox.showinfo('Login', 'Seja bem vindo de volta! ')
        else:
            messagebox.showwarning('Erro!', 'Verifique o nome e a senha!')

    def cad_senha(self):
        senha_cad = self.senha_cadastro.get()
        conf_senha = self.senha_conf.get()
        if senha_cad == conf_senha:
            messagebox.showinfo('Cadastro', 'Cadastro efetuado com sucesso!')
        else:
            messagebox.showwarning('Cadastro', 'Senhas diferentes! Tente novamente!')

    def cadastro_usuario(self):
        self.frameCima()
        self.frameBaixo()

        l_nome_login = Label(self.frame_cima, text='Cadastro de Usuário', anchor=NE, font='Ivy 20', bg=self.cores[3],
                             fg=self.cores[1])
        l_nome_login.place(x=10, y=30)

        l_linha = Label(self.frame_cima, text='', width=600, anchor=NW, font='Ivy 1', bg=self.cores[2],
                        fg=self.cores[1])
        l_linha.place(x=0, y=90)

        l_nome = Label(self.frame_baixo, text='Nome de usuário:', anchor=NW, font='Ivy 15', bg=self.cores[1],
                       fg=self.cores[4])
        l_nome.place(x=10, y=20)

        self.nome_cadastro = Entry(self.frame_baixo, width=35, justify='left', font=("", 15), highlightthickness=1,
                                   relief='solid')
        self.nome_cadastro.place(x=10, y=60)

        l_pass = Label(self.frame_baixo, text='Senha *', anchor=NW, font='Ivy 15', bg=self.cores[1], fg=self.cores[4])
        l_pass.place(x=10, y=95)

        self.senha_cadastro = Entry(self.frame_baixo, width=35, justify='left', show='*', font=("", 15),
                                    highlightthickness=1,
                                    relief='solid')
        self.senha_cadastro.place(x=10, y=140)

        l_pass_cad = Label(self.frame_baixo, text='Confirmar senha', anchor=NW, font='Ivy 15', bg=self.cores[1],
                           fg=self.cores[4])
        l_pass_cad.place(x=10, y=180)

        self.senha_conf = Entry(self.frame_baixo, width=35, justify='left', show='*', font=("", 15),
                                highlightthickness=1,
                                relief='solid')
        self.senha_conf.place(x=10, y=225)

        b_confirmar = Button(self.frame_baixo, command=lambda: self.cad_senha(), text='Confirmar', width=15, height=1,
                             font='Ivy 8 bold', bg=self.cores[0], fg=self.cores[4], relief=RAISED, overrelief=RIDGE)
        b_confirmar.place(x=10, y=300)

        b_cadastro = Button(self.frame_baixo, command=lambda: self.chamada(2), text='Voltar', width=15, height=1,
                            font='Ivy 8 bold', bg=self.cores[0], fg=self.cores[4], relief=RAISED, overrelief=RIDGE)
        b_cadastro.place(x=381, y=300)


test = TelaLogin()
test.janela_inicio()
