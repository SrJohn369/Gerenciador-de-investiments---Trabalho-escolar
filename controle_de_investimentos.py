from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import date
from tkinter import Toplevel as NovaJanela


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

    def delete(self, tabela: str, especifico=False) -> bool:
        if not especifico:
            try:
                self.cursor.execute(f"""DROP TABLE {tabela};""")
                self.banco.commit()
                return True
            except sqlite3.OperationalError as err:
                print(err)
                return False
        else:
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
            self.lista = list(args)

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

    def salvar(self, update=False):
        banco = BancoDeDados('Investimentos')
        # VERIFICANDO ERROS DE INTEGRIDADE DE DADOS
        if not update:
            # garantindo que o codigo não esteja vazío ao salvar
            if not self.lista[0].get() == '':
                # VERIFICA SE TEM PONTO OU VIRGULA
                if self.lista[0].get().count(",") >= 1 or self.lista[0].get().count(".") >= 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Código" só aceita valores de caracteres sem ponto flutuante, '
                                         'por exemplo:\n\tPETR4\n\tALPA4\n\tABEV3')
                    return False
                # VERIFICA SE ULTRAPASSA O LIMITE DE 7 NCARACTERES
                if len(self.lista[0].get()) > 7:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Código" possui código inválido para B3 que possui apenas 7 caracteres'
                                         ' no maximo.'
                                         'Por exemplo:\n\tTAEE11(6)\n\tSANB11(6)\n\tKLBN11(6)')
                    return False
                try:
                    float(self.lista[0].get())
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Código" possui código inválido para B3.\nCódigos de ações possuem letras'
                                         ' e números.\n'
                                         'Por exemplo:\n\tTAEE11(6)\n\tSANB11(6)\n\tKLBN11(6)')
                    return False
                except:
                    pass
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Código", não pode estar vazío!')
                return False

        # varificando se a data está ou não vazía
        if not self.lista[1].get() == '':
            # garantindo que é uma data válida
            try:
                int(self.lista[1].get()[6:10])
                int(self.lista[1].get()[3:5])
                int(self.lista[1].get()[0:2])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            if int(self.lista[1].get()[6:10]) > self.__ano:
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            elif int(self.lista[1].get()[6:10]) == self.__ano and int(self.lista[1].get()[3:5]) > self.__mes:
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            elif int(self.lista[1].get()[6:10]) == self.__ano and int(self.lista[1].get()[3:5]) == self.__mes and \
                    int(self.lista[1].get()[0:2]) > self.__dia:
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Data", não pode estar vazío!')
            return False

        # garantindo que a haja um tipo de operação, compra ou venda
        if self.lista[4].get() == '----':
            messagebox.showerror('Controle de investimentos',
                                 'O campo "Tipo Operação" não possui uma opção de compra ou venda!')
            return False

        # garantindo que em QNT. DE PAPEIS os valores numéricos sejam numéricos
        if not self.lista[2].get() == '':
            # testa de é possivel converter para INTEIRO
            try:
                self.lista[2] = self.lista[2].get()
                self.lista[2] = self.lista[2].replace(",", ".")
                if self.lista[2].count(",") >= 1 or self.lista[2].count(".") >= 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Qnt. De Papeis" só aceita valores numéricos INTEIROS '
                                         'sem ponto flutuante, por exemplo:\n145\t(Cento e quarenta e cinco)')
                    return False
                int(self.lista[2])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Qnt. De Papeis" só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Qtn. De Papeis", não pode estar vazío!')
            return False

        # garantindo que em VALOR UNIT. os valores numéricos sejam numéricos
        if not self.lista[3].get() == '':
            # testa de é possivel converter para FLOAT
            try:
                self.lista[3] = self.lista[3].get()
                self.lista[3] = self.lista[3].replace(",", ".")
                if self.lista[3].count(",") > 1 or self.lista[3].count(".") > 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Valor Unit." só aceita valores numéricos com apenas um ponto '
                                         'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis reais'
                                         ' e setenta e oito centavos)')
                    return False
                float(self.lista[3])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Valor Unit" só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Valor Unit.", não pode estar vazío!')
            return False

        # garantindo que em CORRETAGEM. os valores numéricos sejam numéricos
        if not self.lista[5].get() == '':
            # testa de é possivel converter para FLOAT
            try:
                self.lista[5] = self.lista[5].get()
                self.lista[5] = self.lista[5].replace(",", ".")
                if self.lista[5].count(",") > 1 or self.lista[5].count(".") > 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Corretagem." só aceita valores numéricos com apenas um ponto '
                                         'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis reais'
                                         ' e setenta e oito centavos)')
                    return False
                float(self.lista[5])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Corretagem" só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Corretagem", não pode estar vazío!')
            return False

        # garantindo que em VALOR OP. os valores numéricos sejam numéricos
        if not self.lista[6].get() == '':
            # testa de é possivel converter para FLOAT
            try:
                self.lista[6] = self.lista[6].get()
                self.lista[6] = self.lista[6].replace(",", ".")
                if self.lista[6].count(",") > 1 or self.lista[6].count(".") > 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Valor Op." só aceita valores numéricos com apenas um ponto '
                                         'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis reais'
                                         ' e setenta e oito centavos)')
                    return False
                float(self.lista[6])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Valor Op." só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Valor Op.", não pode estar vazío!')
            return False

        # garantindo que em IMPOSTO. os valores numéricos sejam numéricos
        if not self.lista[7].get() == '':
            # testa de é possivel converter para FLOAT
            try:
                self.lista[7] = self.lista[7].get()
                self.lista[7] = self.lista[7].replace(",", ".")
                if self.lista[7].count(",") > 1 or self.lista[7].count(".") > 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Imposto." só aceita valores numéricos com apenas um ponto '
                                         'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis reais'
                                         ' e setenta e oito centavos)')
                    return False
                float(self.lista[7])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Imposto." só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Imposto", não pode estar vazío!')
            return False

        # garantindo que em VALOR FINAL. os valores numéricos sejam numéricos
        if not self.lista[8].get() == '':
            # testa de é possivel converter para FLOAT
            try:
                self.lista[8] = self.lista[8].get()
                self.lista[8] = self.lista[8].replace(",", ".")
                if self.lista[8].count(",") > 1 or self.lista[8].count(".") > 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Valor Final." só aceita valores numéricos com apenas um ponto '
                                         'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis reais'
                                         ' e setenta e oito centavos)')
                    return False
                float(self.lista[8])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos',
                                     'O campo "Valor Final." só aceita valores numéricos!')
                return False
        else:
            messagebox.showerror('Controle de investimentos', 'O campo "Vlor Final", não pode estar vazío!')
            return False

        # verifica se o ativo ja existe na tabela ativo
        if not update:
            if banco.introduzirDados('Ativos', False, f"'{self.lista[0].get()}'"):
                banco.introduzirDados('Acoes', False, f"'{self.lista[0].get()}', '{self.lista[1].get()}',"
                                                      f"'{self.lista[2]}',       '{self.lista[3]}',"
                                                      f"'{self.lista[4].get()}', '{self.lista[5]}',"
                                                      f"'{self.lista[6]}',       '{self.lista[7]}',"
                                                      f"'{self.lista[8]}'")
                banco.select('*', 'Acoes')
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                return True
            else:
                banco.introduzirDados('Acoes', False, f"'{self.lista[0].get()}', '{self.lista[1].get()}',"
                                                      f"'{self.lista[2]}',       '{self.lista[3]}',"
                                                      f"'{self.lista[4].get()}', '{self.lista[5]}',"
                                                      f"'{self.lista[6]}',       '{self.lista[7]}',"
                                                      f"'{self.lista[8]}'")
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                banco.select('*', 'Acoes')
                return True
        else:

            if lambda :Application().tela_confirmacao(update=True):
                banco.atualizarTabela(
                    'Acoes',
                    f"""data =              '{self.lista[1].get()},'
                        quantidade_papeis = '{self.lista[2].get()},'
                        valor_unitario =    '{self.lista[3].get()},'
                        tipo_de_ordem =     '{self.lista[4].get()},'
                        corretagem =        '{self.lista[5].get()},'
                        valor_da_opercao =  '{self.lista[6].get()},'
                        imposto =           '{self.lista[7].get()},'
                        valor_final =       '{self.lista[8].get()}'     """,
                    f"""acao = '{self.lista[0].get()}'"""
                )
                self.lista[9].destroy()
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                return True

    def visualizar_investimentos(self):
        banco = BancoDeDados('Investimentos')

        lista = banco.select('*', 'Acoes', True, 'Acao', ordem='DESC')
        for i in lista:
            self.frame_treeview.insert("", END, values=i)

    def editar(self):
        # separar os dados na lista
        id_list = self.lista[0].selection()[0]  # como só será selecionado um item, na tupla ele sempre será 0
        colum_1, colum_2, colum_3, colum_4, colum_5, colum_6, colum_7, colum_8, \
            colum_9 = self.lista[0].item(id_list, 'values')
        # separar os dados da optionmenu
        itens = self.lista[4][1]
        optiomenu = 0
        for i, item in enumerate(itens):
            if item == colum_5:
                optiomenu = i
        # por os dados nas entry para editar
        self.lista[1].insert(END, colum_2)
        self.lista[2].insert(END, colum_3)
        self.lista[3].insert(END, colum_4)
        # aqui tive que guardar tupla dentro de tupla de outra
        # tupla para usar os valores e da o set() correto
        self.lista[4][0].set(self.lista[4][1][optiomenu])
        self.lista[5].insert(END, colum_6)
        self.lista[6].insert(END, colum_7)
        self.lista[7].insert(END, colum_8)
        self.lista[8].insert(END, colum_9)


class Application:

    def iniciar(self):
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

    def chamada(self, func, new_frame=True, editar=False):
        """Funções de chamada:
        1 - Cadastrar | 2 - voltar | 3 - salvar | 4 - editar | 5 - excluir | 6 - limpar | 7 - Investimento
        8 - Data"""
        if new_frame:
            self.inicio_frame.destroy()
            self.frame_Tela_Inicio()

        if func == 1:
            self.frame_cadastro()
        elif func == 2:
            self.seja_bem_vindoA()
        elif func == 8:
            if not editar:
                Funcs(self.inicio_frame, self.entry_data).abrir_calendario()
            else:
                Funcs(self.new_window, self.entry_data).abrir_calendario()
        elif func == 7:
            self.frame_investimento()
            Funcs(self.treeview).visualizar_investimentos()
        elif func == 6:
            Funcs(
                self.entry_codigo, self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario,
                self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto, self.entry_valor_final
            ).limpa_tela()
        elif func == 3:
            if not editar:
                Funcs(
                    self.entry_codigo, self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario, self.varCV,
                    self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto, self.entry_valor_final
                ).salvar()
            else:
                id_list = self.treeview.selection()[0]  # como só será selecionado um item, na tupla ele sempre será 0
                Funcs(
                    self.treeview.item(id_list, "values")[0],
                    self.entry_data_edit, self.entry_qnt_de_papeis_edit, self.entry_valor_unitario_edit,
                    self.editar_varCV, self.entry_taxa_corretagem_edit, self.entry_valor_da_operacao_edit,
                    self.entry_imposto_edit, self.entry_valor_final_edit
                ).salvar(update=True)
        elif func == 4:
            self.tela_editar()

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
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.chamada(4, new_frame=False))
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
        self.treeview.place(rely=0.13, relx=0.015, relwidth=0.937, relheight=0.805)
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

    def nova_tela(self, width, height, locateY=2, locateX=2):
        # CHAMA UMA NOVA JANELA PARA EDIÇÃO DE DADOS
        self.new_window = NovaJanela()

        # CONFIGURANDO NOVA JANELA
        #           --- variáveis de início para centralizar a tela ---
        w = width
        h = height
        ws = self.new_window.winfo_screenwidth()
        hs = self.new_window.winfo_screenheight()
        x = (ws / locateX) - (w / 2)
        y = (hs / locateY) - (h / 2)

        #   CONFIGURANDO JANELA
        self.new_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.new_window.title('Plataforma de Investimentos')
        self.new_window.resizable(False, False)
        self.new_window.configure(background='Black')

    def tela_editar(self):
        # usar para selecionar na lista da treeview
        # verifica se tem um item selecionado
        if not self.treeview.selection() == ():
            # print(self.lista[0].selection()) # a função selection() retornará uma tupla, se nenhum item for
            # selecionado retornará uma tupla vazia ()
            id_list = self.treeview.selection()[0]  # como só será selecionado um item, na tupla ele sempre será 0

            # LISTA e VAR PARA OPTIONMENU
            listaOP = ['----', 'Compra', 'Venda']
            self.editar_varCV = StringVar()

            self.nova_tela(350, 450, locateX=4, locateY=2)

            # CONFIGURANDO
            # |---Labels---|
            lbl_editar = Label(self.new_window, text='Editar', font=('KacstOffice', '15'), bg='black', fg='white')
            lbl_linha = Label(self.new_window, text='', width=700, height=1, anchor=NW, font=' Ivy 1 ', bg='#2fc7f4',
                              highlightbackground='#F2F2F2')
            lbl_linha_2 = Label(self.new_window, text='', width=700, height=1, anchor=NW, font=' Ivy 1 ', bg='#2fc7f4',
                                highlightbackground='#F2F2F2')
            lbl_ativo = Label(self.new_window, text=f'{self.treeview.item(id_list, "values")[0]}',
                              font=('KacstOffice', '15'), bg='black', fg='white')
            lbl_Qtn_Papeis = Label(self.new_window, text='Qtn. De Papeis', bg='black', fg='white')
            lbl_valor_unit = Label(self.new_window, text='Valor Unit.', bg='black', fg='white')
            lbl_corretagem = Label(self.new_window, text='Corretagem', bg='black', fg='white')
            lbl_valor_op = Label(self.new_window, text='Valor da Operação', bg='black', fg='white')
            lbl_imposto = Label(self.new_window, text='Imposto', bg='black', fg='white')
            lbl_valor_final = Label(self.new_window, text='Valor final', bg='black', fg='white')
            lbl_compra_venda = Label(self.new_window, text='Tipo Operação', bg='black', fg='white')
            # |---Bottuns---|
            btn_cancelar = Button(self.new_window, text='Cancelar', font=('KacstOffice', '10'), bg='#02347c',
                                  fg='white',borderwidth=2, highlightbackground='black',
                                  command=lambda: self.new_window.destroy())
            btn_salvar = Button(self.new_window, text='Salvar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.chamada(3, editar=True, new_frame=False))
            btn_data = Button(self.new_window, text='Data', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                              borderwidth=2, highlightbackground='black',
                              command=lambda: self.chamada(8, new_frame=False))
            # |---OPTIONMENU---|
            op_compraVenda = OptionMenu(self.new_window, self.editar_varCV, *listaOP)
            # |---ENTRY---|
            self.entry_data_edit = Entry(self.new_window, width=10)
            self.entry_qnt_de_papeis_edit = Entry(self.new_window, width=10)
            self.entry_valor_unitario_edit = Entry(self.new_window, width=10)
            self.entry_taxa_corretagem_edit = Entry(self.new_window, width=10)
            self.entry_valor_da_operacao_edit = Entry(self.new_window, width=10)
            self.entry_imposto_edit = Entry(self.new_window, width=10)
            self.entry_valor_final_edit = Entry(self.new_window, width=10)

            # |---ENTRY position---|
            self.entry_qnt_de_papeis_edit.place(relx=0.4, rely=0.23, relheight=0.04)
            self.entry_valor_unitario_edit.place(relx=0.4, rely=0.28, relheight=0.04)
            self.entry_taxa_corretagem_edit.place(relx=0.4, rely=0.33, relheight=0.04)
            self.entry_valor_da_operacao_edit.place(relx=0.4, rely=0.387, relheight=0.04)
            self.entry_imposto_edit.place(relx=0.4, rely=0.44, relheight=0.04)
            self.entry_valor_final_edit.place(relx=0.4, rely=0.49, relheight=0.04)
            self.entry_data_edit.place(relx=0.53, rely=0.755, relheight=0.04)
            # |---Labels position---|
            lbl_editar.pack(pady=10, anchor='center')
            lbl_linha.pack(anchor='center')
            lbl_ativo.pack(pady=10, anchor='center')
            lbl_Qtn_Papeis.pack(pady=3, anchor='w')
            lbl_valor_unit.pack(anchor='w')
            lbl_corretagem.pack(pady=3, anchor='w')
            lbl_valor_op.pack(anchor='w')
            lbl_imposto.pack(pady=3, anchor='w')
            lbl_valor_final.pack(anchor='w')
            lbl_linha_2.pack(pady=4, anchor='center')
            lbl_compra_venda.pack(pady=5, anchor='center')
            # |---Bottuns position---|
            btn_cancelar.place(relx=0.05, rely=0.9, relheight=0.07)
            btn_salvar.place(relx=0.75, rely=0.9, relheight=0.07)
            btn_data.place(relx=0.30, rely=0.75, relheight=0.07)
            # |---OPTIONMENU position---|
            op_compraVenda.pack(anchor='center')
            op_compraVenda.configure(highlightcolor='black', borderwidth=1, highlightbackground='black')

            # CHAMADA DA CLASS FUNCS PARA EDITAR DADOS
            Funcs(self.treeview, self.entry_data_edit, self.entry_qnt_de_papeis_edit,
                  self.entry_valor_unitario_edit, (self.editar_varCV, listaOP), self.entry_taxa_corretagem_edit,
                  self.entry_valor_da_operacao_edit, self.entry_imposto_edit, self.entry_valor_final_edit,
                  self.new_window).editar()
            self.new_window.mainloop()
            return True

        else:
            messagebox.showerror('Controle de investimentos',
                                 'SELECIONE UM ITEM PARA EDITAR')
            return False

    def tela_confirmacao(self, update=False, delete=False):
        # gera telinha no centro
        self.nova_tela(300,100)

        if update:
            # funcoes falsas para dar o retorno que eu quero
            def confirmar():
                self.new_window.destroy()
                self.new_window.destroy()
                return True
            # LABEL
            lbl_alterar = Label(self.new_window, text='DESEJA ALTERAR AS \nINFORMAÇÕES DA AÇÃO EDITADA?')
            lbl_alterar.configure(font=('KacstOffice', '10'), bg='black', fg='white')
            lbl_alterar.pack(pady=12)
            # BUTOES
            btn_cancelar = Button(self.new_window, text='Cancelar', font=('KacstOffice', '10'), bg='#02347c',
                                  fg='white', borderwidth=2, highlightbackground='black',
                                  command=lambda: self.new_window.destroy())
            btn_confirmar = Button(self.new_window, text='Confirmar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: confirmar())
            btn_cancelar.place(relx=0.05, rely=0.65, relheight=0.30)
            btn_confirmar.place(relx=0.65, rely=0.65, relheight=0.30)
            if confirmar():
                return True


Application().iniciar()
