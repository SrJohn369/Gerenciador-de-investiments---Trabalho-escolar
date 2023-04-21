from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from  datetime import date


class BancoDeDados:
    def __init__(self, nome_banco):
        self.__abrirBanco(nome_banco)
        self.__criarTabela('Ativos', 'Ativo VARCHAR(7) PRIMARY KEY')
        self.__criarTabela('Acoes', 'acao                   VARCHAR(7),'
                                    'data                   DATE,'
                                    'quantidade_papeis      SMALLINT,'
                                    'valor_unitario         NUMERIC(7,2),'
                                    'tipo_de_ordem          VARCHAR(7),'
                                    'corretagem             NUMERIC(5,2),'
                                    'valor_da_opercao       NUMERIC(7,2),'
                                    'imposto                NUMERIC(6,2),'
                                    'valor_final            NUMERIC(7,2),'
                                    'FOREIGN KEY (acao)'
                                    '   REFERENCES Ativos(Ativo)')

    def __abrirBanco(self, nomeBanco):
        self.banco = sqlite3.connect(f'{nomeBanco}.db')
        self.cursor = self.banco.cursor()

    def __criarTabela(self, nomeTabela: str, colunasEDados: str) -> bool:

        try:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nomeTabela} 
                                ({colunasEDados});""")
        except sqlite3.OperationalError as err:
            print(err)
            return False

        self.banco.commit()
        return True

    def atualizarTabela(self, nomeTabela: str, set: str, where: str):

        self.cursor.execute(f"""
        UPDATE {nomeTabela}
        SET {set}
        WHERE {where};""")

    def introduzirDados(self, nome_tabela: str, especifico: bool, valores: str,
                        colum_especificas: str = 'Default') -> bool:
        """o parametro colum_especificas pode ser usado somente quando o parametro 'especifico' for True"""

        if especifico:
            try:

                self.cursor.execute(f"""INSERT INTO {nome_tabela}
                                    ({colum_especificas})
                                        VALUES 
                                    ({valores});""")

            except sqlite3.OperationalError as err:
                print(err)
                return False

        else:
            try:
                self.cursor.execute(f"""INSERT INTO {nome_tabela}
                                        VALUES 
                                    ({valores});""")

            except sqlite3.OperationalError as err:
                print(err)
                return False
            except sqlite3.IntegrityError as interr:
                print(interr)
                return False

        self.banco.commit()
        return True

    def delete(self, tabela: str) -> bool:

        try:
            self.cursor.execute(f"""DROP TABLE {tabela};""")
            self.banco.commit()
            return True
        except sqlite3.OperationalError as err:
            print(err)
            return False

    def select(self, select: str, from1: str, order_by=False, coluna='default', ordem='ASC'):
        if not order_by:
            for row in self.cursor.execute(f"SELECT {select} FROM {from1}"):
                print(row)
        else:
            lista = self.cursor.execute(f"SELECT {select} FROM {from1} ORDER BY {coluna} {ordem}")
            return lista


class Funcs:
    __ano = int(date.today().year)
    __mes = int(date.today().month)
    __dia = int(date.today().day)

    def __init__(self, *args):
        """indices: 0 ← Frame/treview | 1 ← get.Entry | 2 ← get.Variável | 3+ ← Lista (Não serão considerados Frame, Entry e
         nem a Variavel apenas a lista Lista) """
        self.frame_treeview = self.entry = self.variavel = None
        self.lista = []
        if len(args) == 1:
            self.frame_treeview = args[0]
        elif len(args) == 2:
            self.entry = args[1]
        elif len(args) == 3:
            self.variavel = args[2]
        elif len(args) >= 4:
            self.lista = args

    def abrir_calendario(self):
        self.calendario = Calendar(self.frame_treeview, fg="gray75", bg="blue", font=('KacstOffice', '10', 'bold'),
                                   locale='pt_br')
        self.get_btn_data = Button(self.frame_treeview, text='Inserir data', command=lambda: self.__por_entry())

        self.get_btn_data.place(x=270, y=67)
        self.calendario.place(x=240, y=100)

    def __por_entry(self):
        get_date = self.calendario.get_date()
        self.calendario.destroy()
        self.entry.delete(0, END)
        self.entry.insert(END, get_date)
        self.get_btn_data.destroy()

    def limpa_tela(self):
        self.lista[0].delete(0, END)
        self.lista[1].delete(0, END)
        self.lista[2].delete(0, END)
        self.lista[3].delete(0, END)
        self.lista[4].delete(0, END)
        self.lista[5].delete(0, END)
        self.lista[6].delete(0, END)
        self.lista[7].delete(0, END)

    def salvar(self):
        banco = BancoDeDados('Investimentos')
        # VERIFICANDO ERROS DE INTEGRIDADE DE DADOS
        # garantindo que o codigo não esteja vazío
        if self.lista[0].get() == '':
            messagebox.showerror('Controle de investimentos', 'O campo "Código", não pode estar vazío!')
            return False
        # garantindo que a data não ultrapasse a data atual
        elif int(self.lista[1].get()[6:10]) > self.__ano:
            messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
            return False
        # garantindo que a data não ultrapasse a data atual
        elif int(self.lista[1].get()[6:10]) == self.__ano and int(self.lista[1].get()[3:5]) > self.__mes:
            messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
            return False
        # garantindo que a data não ultrapasse a data atual
        elif int(self.lista[1].get()[6:10]) == self.__ano and int(self.lista[1].get()[3:5]) == self.__mes and\
                int(self.lista[1].get()[0:2]) > self.__dia:
            messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
            return False
        # garantindo que a haja um tipo de operação, compra ou venda
        elif self.lista[4].get() == '----':
            messagebox.showerror('Controle de investimentos',
                                 'O campo "Tipo Operação" não possui uma opção de compra ou venda!')
            return False

        # verifica se o ativo ja existe na tabela ativo
        if banco.introduzirDados('Ativos', False, f"'{self.lista[0].get()}'"):
            banco.introduzirDados('Acoes', False, f"'{self.lista[0].get()}', '{self.lista[1].get()}',"
                                                  f"'{self.lista[2].get()}', '{self.lista[3].get()}',"
                                                  f"'{self.lista[4].get()}', '{self.lista[5].get()}',"
                                                  f"'{self.lista[6].get()}', '{self.lista[7].get()}',"
                                                  f"'{self.lista[8].get()}'")
            banco.select('*', 'Ativos')
            messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
        else:
            banco.introduzirDados('Acoes', False, f"'{self.lista[0].get()}', '{self.lista[1].get()}',"
                                                  f"'{self.lista[2].get()}', '{self.lista[3].get()}',"
                                                  f"'{self.lista[4].get()}', '{self.lista[5].get()}',"
                                                  f"'{self.lista[6].get()}', '{self.lista[7].get()}',"
                                                  f"'{self.lista[8].get()}'")
            messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
            banco.select('*', 'Acoes')

    def visualizar_investimentos(self):
        banco = BancoDeDados('Investimentos')

        lista = banco.select('*', 'Acoes', True, 'data', ordem='DESC')
        for i in lista:
            self.frame_treeview.insert("", END, values=i)


class Application:

    def __init__(self):
        #   CRIANDO VARIAVEIS PARA JANELA E FRAME PRINCIPAL
        self.root = tk.Tk()
        #           --- variáveis de início para centralizar a tela ---
        w = 750
        h = 400
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        #   CONFIGURANDO JANELA
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.title('Plataforma de Investimentos')
        self.root.resizable(False, False)

        #   FUNÇÕES DE INÍCIO
        self.frame_principal()
        self.seja_bem_vindoA(frame=True)

        #   MATEM A JANELA ATIVA
        self.root.mainloop()

    def chamada(self, func, new_frame=True):
        """Funções de chamada:
        1 - Cadastrar | 2 - voltar | 3 - salvar
        4 - editar
        5 - excluir
        6 - limpar
        7 - Investimento
        8 - Data"""
        if new_frame:
            self.inicio_frame.destroy()
            self.frame_Tela_Inicio()

        if func == 1:
            self.frame_cadastro()
        elif func == 2:
            self.seja_bem_vindoA()
        elif func == 8:
            Funcs(self.inicio_frame, self.entry_data).abrir_calendario()
        elif func == 7:
            self.frame_investimento()
            Funcs(self.treeview).visualizar_investimentos()
        elif func == 6:
            Funcs(
                self.entry_codigo, self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario,
                self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto, self.entry_valor_final
            ).limpa_tela()
        elif func == 3:
            Funcs(
                self.entry_codigo, self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario, self.varCV,
                self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto, self.entry_valor_final
            ).salvar()

    def bt_voltar(self):
        bt_voltar = Button(self.inicio_frame, text='Voltar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                           borderwidth=2, highlightbackground='black', command=lambda: self.chamada(2))

        bt_voltar.place(x=20, y=10, relheight=0.07)

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
        acess = tk.Button(self.options_frame, text='Investimentos', font=('KacstOffice', '10'), bg='#2fc7f4',
                          command=lambda: self.chamada(7))

        #   CONFIGURANDO FRAME PRINCIPAL
        # |---botoes---|
        cad_btn.pack(pady=100, anchor='center')
        acess.pack(anchor='center')
        # |---linha---|
        l_linha.place(x=0, y=70)
        title_op.place(x=45, y=20)

    def frame_Tela_Inicio(self):
        #   CRIANDO FRAME DE TELA DE INICIO
        self.inicio_frame = Frame(self.root, background='black')

        #   CONFIGURANDO FRAME
        self.inicio_frame.place(x=150, relheight=1, relwidth=1)

    def seja_bem_vindoA(self, frame=False):
        #   CHAMANDO FRAME DE TELA INICIAL
        if frame:
            self.frame_Tela_Inicio()
        # Foto bg
        self.imagem = tk.PhotoImage(file='b3.png')
        self.imagem.subsample(1, 1)
        self.imagem_fundo = Label(self.inicio_frame, image=self.imagem)
        self.imagem_fundo.place(x=180, y=140, relwidth=0.333, relheight=0.28)

        # label
        bem_vindo = tk.Label(self.inicio_frame, text='SEJA BEM-VINDO(A)', font=('KacstOffice', '15'), bg='black',
                             fg='#2fc7f4')
        bem_vindo.place(x=202, y=20)

    def frame_cadastro(self):
        # LISTA e VAR PARA OPTIONMENU
        listaOP = ['----', 'Compra', 'Venda']
        self.varCV = StringVar()
        self.varCV.set(listaOP[0])

        #   CRIANDO BOTOES, LABELS, ENTRYS e OPTIONSMENU
        # |---BOTÃO--|
        self.bt_voltar()
        self.bt_limpar = Button(self.inicio_frame, text='Limpar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.chamada(6, new_frame=False))
        self.bt_salvar = Button(self.inicio_frame, text='Salvar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.chamada(3, new_frame=False))
        self.bt_data = Button(self.inicio_frame, text='Data', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                              borderwidth=2, highlightbackground='black',
                              command=lambda: self.chamada(8, new_frame=False))
        # |---LABEL---|
        lb_cadastrar_investimento = Label(self.inicio_frame, text="Cadastrar Investimento", font=('KacstOffice', '15'),
                                          bg='black', fg='#2fc7f4')
        lb_codigo = Label(self.inicio_frame, text='Código', font=('KacstOffice', '10'), bg='black', fg='white')
        lb_quantidade_papeis = Label(self.inicio_frame, text='Qnt. De Papéis', font=('KacstOffice', '10'),
                                     bg='black', fg='white')
        lb_valor_unitario = Label(self.inicio_frame, text='Valor Unit.', font=('KacstOffice', '10'),
                                  bg='black', fg='white')
        lb_compra_venda = Label(self.inicio_frame, text='Tipo Operação', font=('KacstOffice', '10'),
                                bg='black', fg='white')
        lb_taxa_corretagem = Label(self.inicio_frame, text='Corretagem', font=('KacstOffice', '10'),
                                   bg='black', fg='white')
        lb_valor_operacao = Label(self.inicio_frame, text='Valor Op.', font=('KacstOffice', '10'),
                                  bg='black', fg='white')
        lb_imposto = Label(self.inicio_frame, text='Imposto', font=('KacstOffice', '10'),
                           bg='black', fg='white')
        lb_valor_final = Label(self.inicio_frame, text='Valor Final', font=('KacstOffice', '10'),
                               bg='black', fg='white')

        # |---OPTIONMENU---|
        op_compraVenda = OptionMenu(self.inicio_frame, self.varCV, *listaOP)
        # |---ENTRY---|
        self.entry_codigo = Entry(self.inicio_frame, width=10)
        self.entry_data = Entry(self.inicio_frame, width=10)
        self.entry_qnt_de_papeis = Entry(self.inicio_frame, width=10)
        self.entry_valor_unitario = Entry(self.inicio_frame, width=10)
        self.entry_taxa_corretagem = Entry(self.inicio_frame, width=10)
        self.entry_valor_da_operacao = Entry(self.inicio_frame, width=10)
        self.entry_imposto = Entry(self.inicio_frame, width=10)
        self.entry_valor_final = Entry(self.inicio_frame, width=10)

        #   CONFIGURANDO BOTOES, LABELS, ENTRYS e OPTIONSMENU
        # |---BOTÃO--|
        self.bt_salvar.place(x=510, y=10, relheight=0.07)
        self.bt_limpar.place(x=510, y=360, relheight=0.07)
        self.bt_data.place(x=155, y=67, height=20)
        # |---LABEL---|
        lb_cadastrar_investimento.place(x=180, y=12)
        lb_codigo.place(x=25, y=70)
        lb_quantidade_papeis.place(x=285, y=70)
        lb_valor_unitario.place(x=425, y=70)
        lb_compra_venda.place(x=25, y=150)
        lb_taxa_corretagem.place(x=155, y=150)
        lb_valor_operacao.place(x=285, y=150)
        lb_imposto.place(x=425, y=150)
        lb_valor_final.place(x=25, y=240)
        # |---ENTRY---|
        self.entry_codigo.place(x=25, y=100)
        self.entry_data.place(x=155, y=100)
        self.entry_qnt_de_papeis.place(x=285, y=100)
        self.entry_valor_unitario.place(x=425, y=100)
        self.entry_taxa_corretagem.place(x=155, y=180)
        self.entry_valor_da_operacao.place(x=285, y=180)
        self.entry_imposto.place(x=425, y=180)
        self.entry_valor_final.place(x=25, y=270)
        # |---OPTIONMENU---|
        op_compraVenda.place(x=25, y=180)
        op_compraVenda.configure(highlightcolor='black', borderwidth=1, highlightbackground='black')

    def treeview_frame(self):
        #   CRIANDO FRAME PARA TREEVIEW
        self.tree_frame = Frame(self.inicio_frame, background='gray8')

        #   CONFIGURANDO FRAME
        self.tree_frame.place(y=80, x=10, width=580, height=312)

    def frame_investimento(self):
        #   CRIANDO BOTOES, LABELS, ENTRYS e OPTIONSMENU
        # |---BOTÃO--|
        self.bt_voltar()
        # |---LABEL---|
        lb_cadastrar_investimento = Label(self.inicio_frame, text="Seus Investimentos", font=('KacstOffice', '15'),
                                          bg='black', fg='#2fc7f4')

        #   CONFIGURANDO BOTOES, LABELS, ENTRYS e OPTIONSMENU
        # |---LABEL---|
        lb_cadastrar_investimento.place(x=180, y=12)

        #   CHAMANDO FRAME TREEVIEW
        self.treeview_frame()

        #   CRIANDO BOTOES e TREEVIEW
        # |---BOTÃO--|
        self.bt_filtro = Button(self.tree_frame, text='Filtrar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black')
        self.bt_remover = Button(self.tree_frame, text='Remover', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                 borderwidth=2, highlightbackground='black')
        self.bt_editar = Button(self.tree_frame, text='Editar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black')
        # |---TREEVIEW---|
        self.treeview = ttk.Treeview(self.tree_frame, height=3)
        # |---SCROLLBAR---|
        #   se não defininir o command na Scrollbar e não configurar a qauntidade de colunas na treeview a barra de
        #   rolagem provavelmente não funcionará
        self.scrollbar_vertical = Scrollbar(self.tree_frame, orient='vertical', command=self.treeview.yview)
        self.scrollbar_horizontal = Scrollbar(self.tree_frame, orient='horizontal', command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)

        #   CONFIGURANDO BOTOES e TREEVIEW
        # |---BOTÃO--|
        self.bt_filtro.place(relx=0.015, rely=0.015)
        self.bt_remover.place(relx=0.83, rely=0.015)
        self.bt_editar.place(relx=0.70, rely=0.015)
        # |---TREEVIEW---|
        self.treeview.place(rely=0.13, relx=0.015, relwidth=0.9365, relheight=0.85)
        self.treeview["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.treeview['show'] = 'headings'  # mostrar os cabeçalhos
        # cabeçalho
        self.treeview.heading('1', text='Cod. Ativo')
        self.treeview.heading('2', text='Data')
        self.treeview.heading('3', text='Qtd. Papéis')
        self.treeview.heading('4', text='Valor Unitário')
        self.treeview.heading('5', text='Compra/Venda')
        self.treeview.heading('6', text='Corretagem')
        self.treeview.heading('7', text='Valor da Operação')
        self.treeview.heading('8', text='Imposto')
        self.treeview.heading('9', text='Valor final')
        # espaçamento das colunas
        self.treeview.column("1", width=90, anchor='c')
        self.treeview.column("2", width=90, anchor='c')
        self.treeview.column("3", width=100, anchor='c')
        self.treeview.column("4", width=120, anchor='c')
        self.treeview.column("5", width=120, anchor='c')
        self.treeview.column("6", width=120, anchor='c')
        self.treeview.column("7", width=180, anchor='c')
        self.treeview.column("8", width=90, anchor='c')
        self.treeview.column("9", width=120, anchor='c')
        # |---CROLLBAR---|
        self.scrollbar_vertical.place(relx=0.955, rely=0.13, relheight=0.85)
        self.scrollbar_horizontal.place(relx=0.015, rely=0.94, relwidth=0.9365)


Application()
