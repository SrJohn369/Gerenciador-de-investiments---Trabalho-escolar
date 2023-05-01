from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Toplevel as NovaJanela
import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import date
import sqlite3


class BancoDeDados:
    def __init__(self, nome_banco):
        self.__abrirBanco(nome_banco)
        self.__criarTabela('Ativos', 'Ativo VARCHAR(7) PRIMARY KEY')
        self.__criarTabela('Acoes', 'id_acao                INTEGER        PRIMARY KEY     AUTOINCREMENT,'
                                    'acao                   VARCHAR(7),'
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
        try:
            self.cursor.execute(f"""
            UPDATE {nomeTabela}
            SET {set}
            WHERE {where};""")
            self.banco.commit()
        except sqlite3.OperationalError as err:
            print(err)
            return False
        except sqlite3.IntegrityError as interr:
            print(interr)
            return False

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
                print(err, 'erro operacional em "especifico"')
                return False

        else:
            try:
                self.cursor.execute(f"""INSERT INTO {nome_tabela}
                                        VALUES 
                                    ({valores});""")

            except sqlite3.OperationalError as err:
                print(err, 'erro na operação de update')
                return False
            except sqlite3.IntegrityError as interr:
                print(interr, 'Falha de integridade')
                return False

        self.banco.commit()
        return True

    def delete(self, tabela: str, especifico=False, arg:str='') -> bool:
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
                self.cursor.execute(f"""DELETE FROM {tabela} WHERE {arg};""")
                self.banco.commit()
                return True
            except sqlite3.OperationalError as err:
                print(err)
                return False

    def select(self, select: str, from1: str, join: str = '', on: str = '', where: str = '', onde=False,
               associacao=False, order_by=False, coluna='default', ordem='ASC'):
        if order_by:
            if onde:
                lista = []
                print("OXII")
                for dado in self.cursor.execute(f"SELECT {select} FROM {from1}"
                                                f" WHERE {where} ORDER BY {coluna} {ordem}"):
                    lista.append(dado)
                print(lista)
                return lista
            lista = []
            for dado in self.cursor.execute(f"SELECT {select} FROM {from1} ORDER BY {coluna} {ordem}"):
                lista.append(dado)
            return lista
        if associacao:
            if onde:
                lista = []
                for dado in self.cursor.execute(f"SELECT {select} FROM {from1} INNER JOIN {join} ON {on} "
                                                f"WHERE {where}"):
                    lista.append(dado)
                print("\t\t\tLISTA ASSOCIADA\n", lista)
                return lista
            lista = []
            for dado in self.cursor.execute(f"SELECT {select} FROM {from1} INNER JOIN {join} ON {on}"):
                lista.append(dado)
            print("\t\t\tLISTA ASSOCIADA\n", lista)
            return lista
        else:
            lista = []
            for dado in self.cursor.execute(f"SELECT {select} FROM {from1}"):
                lista.append(dado)
            print("\t\t\tLISTA NÃO ORDENADA\n", lista)
            return lista


class Funcs:
    __ano = int(date.today().year)
    __mes = int(date.today().month)
    __dia = int(date.today().day)

    def __init__(self, *args):
        """indices: 0 ← Frame/treview | 1 ← get.Entry | 2 ← get.Variável | 3+ ← Lista (Não serão considerados Frame, Entry e
         nem a Variavel apenas a lista Lista) """
        self.variavel_1 = self.variavel_2 = self.variavel_3 = None
        self.lista = []
        if len(args) == 1:
            self.variavel_1 = args[0]
        elif len(args) == 2:
            self.variavel_1 = args[0]
            self.variavel_2 = args[1]
        elif len(args) == 3:
            self.variavel_1 = args[0]
            self.variavel_2 = args[1]
            self.variavel_3 = args[2]
        elif len(args) >= 4:
            self.lista = list(args)

    def abrir_calendario(self, EDITAR=False) -> None:
        if EDITAR:
            self.calendario = Calendar(self.variavel_1, fg="gray75", bg="blue", font=('KacstOffice', '10', 'bold'),
                                       locale='pt_br')
            self.get_btn_data = Button(self.variavel_1, text='Inserir data', command=lambda: self.__por_entry(),
                                       relief='solid')

            self.get_btn_data.place(relx=0.08, rely=0.5, relwidth=0.845)
            self.get_btn_data.configure(bg='#02347c', fg='white', font=('KacstOffice', '10', 'bold'))
            self.calendario.place(relx=0.08, rely=0.57)

        else:
            self.calendario = Calendar(self.variavel_1, fg="gray75", bg="blue", font=('KacstOffice', '10', 'bold'),
                                       locale='pt_br')
            self.get_btn_data = Button(self.variavel_1, text='Inserir data', command=lambda: self.__por_entry(),
                                       relief='solid')

            self.get_btn_data.place(relx=0.21, rely=0.195, relwidth=0.395)
            self.get_btn_data.configure(bg='#02347c', fg='white', font=('KacstOffice', '10', 'bold'))
            self.calendario.place(relx=0.21, rely=0.27)

    def __por_entry(self):
        get_date = self.calendario.get_date()  # vai me retornar uma data no formato YYYY/MM/DD
        ano = get_date[6:10]
        mes = get_date[3:5]
        dia = get_date[0:2]
        get_date = f'{ano}-{mes}-{dia}'
        self.calendario.destroy()
        self.variavel_2.delete(0, END)
        self.variavel_2.insert(END, get_date)
        self.get_btn_data.destroy()

    def limpa_tela(self):
        self.lista[0].delete(0, END)
        self.lista[1].delete(0, END)
        self.lista[2].delete(0, END)
        self.lista[2].insert(0, '0')
        self.lista[3].delete(0, END)
        self.lista[3].insert(0, '0.0')
        self.lista[4].delete(0, END)
        self.lista[4].insert(0, '0.0')
        self.lista[5].delete(0, END)
        self.lista[6].delete(0, END)
        self.lista[7].delete(0, END)

    def salvar(self, update=False) -> bool:
        banco = BancoDeDados('Investimentos')
        # VERIFICANDO ERROS DE INTEGRIDADE DE DADOS
        if not update:
            # garantindo que o codigo não esteja vazío ao salvar
            if not self.lista[9].get() == '':
                # VERIFICA SE TEM PONTO OU VIRGULA
                if self.lista[9].get().count(",") >= 1 or self.lista[9].get().count(".") >= 1:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Código" só aceita valores de caracteres sem ponto flutuante, '
                                         'por exemplo:\n\tPETR4\n\tALPA4\n\tABEV3')
                    return False
                # Aqui remove todos os espaços em branco no inicio e no fim
                self.lista[9] = self.lista[9].get().strip()
                # VERIFICA SE ULTRAPASSA O LIMITE DE 7 NCARACTERES
                if len(self.lista[9]) > 7:
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Código" possui código inválido para B3 que possui apenas 7 caracteres'
                                         ' no maximo.'
                                         'Por exemplo:\n\tTAEE11(6)\n\tSANB11(6)\n\tKLBN11(6)')
                    return False
                try:
                    float(self.lista[9])
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
                int(self.lista[1].get()[0:4])
                int(self.lista[1].get()[5:7])
                int(self.lista[1].get()[8:10])
            except ValueError as err:
                print(err)
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            if int(self.lista[1].get()[0:4]) > self.__ano:
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            elif int(self.lista[1].get()[0:4]) == self.__ano and int(self.lista[1].get()[5:7]) > self.__mes:
                messagebox.showerror('Controle de investimentos', 'O campo "Data" possui uma data invalida!')
                return False

            # garantindo que a data não ultrapasse a data atual
            elif int(self.lista[1].get()[0:4]) == self.__ano and int(self.lista[1].get()[5:7]) == self.__mes and \
                    int(self.lista[1].get()[8:10]) > self.__dia:
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
            print('Vaerificou se já existe ativo com esse nome')
            if banco.introduzirDados('Ativos', False, f"'{self.lista[9]}'"):
                banco.introduzirDados('Acoes', True, f"'{self.lista[9]}', '{self.lista[1].get()}',"
                                                     f"'{self.lista[2].get()}', '{self.lista[3].get()}',"
                                                     f"'{self.lista[4].get()}', '{self.lista[5].get()}',"
                                                     f"'{self.lista[6]}',       '{self.lista[7]}',"
                                                     f"'{self.lista[8]}'",
                                      "acao, data, quantidade_papeis, valor_unitario,tipo_de_ordem,"
                                      "corretagem,valor_da_opercao,imposto,valor_final")
                banco.select('*', 'Acoes')
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                return True
            else:
                banco.introduzirDados('Acoes', True, f"'{self.lista[9]}', '{self.lista[1].get()}',"
                                                     f"'{self.lista[2].get()}', '{self.lista[3].get()}',"
                                                     f"'{self.lista[4].get()}', '{self.lista[5].get()}',"
                                                     f"'{self.lista[6]}',       '{self.lista[7]}',"
                                                     f"'{self.lista[8]}'",
                                      "acao, data, quantidade_papeis, valor_unitario,tipo_de_ordem,"
                                      "corretagem,valor_da_opercao,imposto,valor_final")
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                banco.select('*', 'Acoes')
                return True
        else:
            confirma = messagebox.askquestion('Controle de investimentos',
                                              'TEM CERTEZA QUE DESEJA SALVAR OS DADOS ALTERADOS?', )

            if confirma == 'yes':
                banco.atualizarTabela(
                    'Acoes',
                    f"""data =              '{self.lista[1].get()}',
                        quantidade_papeis = '{self.lista[2].get()}',
                        valor_unitario =    '{self.lista[3].get()}',
                        tipo_de_ordem =     '{self.lista[4].get()}',
                        corretagem =        '{self.lista[5].get()}',
                        valor_da_opercao =  '{self.lista[6]}',
                        imposto =           '{self.lista[7]}',
                        valor_final =       '{self.lista[8]}'     """,
                    f"""id_acao = '{self.lista[10]}'"""
                )
                self.lista[9].destroy()
                self.visualizar_investimentos('',EDITAR=True)
                messagebox.showinfo('Controle de investimentos', 'Salvo com sucesso!!')
                return True
            else:
                print('cancealdo')
                return False

    def visualizar_investimentos(self, evento: any, EDITAR=False, ativo=False) -> bool:
        banco = BancoDeDados('Investimentos')
        if EDITAR:
            self.lista[0].delete(*self.lista[0].get_children())
            lista = banco.select('*', 'Acoes', order_by=True, coluna='acao', ordem='DESC')
            for i in lista:
                self.lista[0].insert("", END, values=i)
        else:
            if ativo:
                self.variavel_1.delete(*self.variavel_1.get_children())
                lista = banco.select('*', 'Acoes', where=f"acao = '{evento}'",
                                     order_by=True, onde=True, coluna='acao', ordem='DESC')
                if not lista:
                    return False
                else:
                    for i, dado in enumerate(lista):
                        self.variavel_1.insert("", END, values=dado)
                    return True
            else:
                self.variavel_1.delete(*self.variavel_1.get_children())
                lista = banco.select('*', 'Acoes', order_by=True, coluna='acao', ordem='DESC')
                print(len(lista))
                for i, dados in enumerate(lista):
                    self.variavel_1.insert("", END, values=dados)

    def editar(self):
        # separar os dados na lista
        id_list = self.lista[0].selection()[0]  # como só será selecionado um item, na tupla ele sempre será 0
        colum_1, colum_2, colum_3, colum_4, colum_5, colum_6, colum_7, colum_8, \
            colum_9, colum_10 = self.lista[0].item(id_list, 'values')
        # separar os dados da optionmenu
        itens = self.lista[4][1]
        optiomenu = 0
        for i, item in enumerate(itens):
            if item == colum_6:
                optiomenu = i
        # por os dados nas entrys para editar
        self.lista[8].insert(END, colum_10)  # valor total
        self.lista[1].insert(END, colum_3)  # data
        self.lista[2].insert(END, colum_4)  # qtn papeis
        # aqui tive que guardar tupla dentro de tupla de outra
        # tupla para usar os valores e da o set() correto
        self.lista[4][0].set(self.lista[4][1][optiomenu])
        self.lista[3].insert(END, colum_5)  # valor unit
        self.lista[5].insert(END, colum_7)  # corretagem
        self.lista[6].insert(END, colum_8)  # valor op
        self.lista[7].insert(END, colum_9)  # imposto

    def remover(self):
        banco = BancoDeDados('Investimentos')
        confirma = messagebox.askquestion('Controle de investimentos',
                                          f'TEM CERTEZA QUE DESEJA REMOVER'
                                          f' ESSA AÇÃO?\n{self.lista[2]}\t{self.lista[3]}')
        if confirma == 'yes':
            banco.delete('Acoes', especifico=True, arg=f"id_acao = '{self.lista[1]}'")
            # deleta o ativo tambem caso não exista mais ordens
            lista = banco.select(select="Ativos.Ativo, Acoes.acao", from1="Ativos", join="Acoes", on="Ativo = acao",
                                 where=f"acao = '{self.lista[2]}'", onde=True, associacao=True)
            if not lista:
                banco.delete(tabela="Ativos", especifico=True, arg=f"Ativo = '{self.lista[2]}'")
            self.visualizar_investimentos('',EDITAR=True)
            messagebox.showinfo('Controle de investimentos', 'Removido com sucesso!')
            return True


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
        self.__frame_principal()
        self.__seja_bem_vindoA(frame=True)

        #   MATEM A JANELA ATIVA
        self.root.mainloop()

    def __chamada(self, func, new_frame=True, editar=False):
        """Funções de chamada:
        1 - Cadastrar | 2 - voltar | 3 - salvar | 4 - editar | 5 - excluir | 6 - limpar | 7 - Investimento
        8 - Data | 9 - calcular"""
        if new_frame:
            self.inicio_frame.destroy()
            self.__frame_Tela_Inicio()

        if func == 1:
            self.__frame_cadastro()
        elif func == 2:
            self.__seja_bem_vindoA()
        elif func == 8:
            if not editar:
                Funcs(self.inicio_frame, self.entry_data).abrir_calendario()
            else:
                Funcs(self.new_window, self.entry_data_edit).abrir_calendario(EDITAR=True)
        elif func == 7:
            self.__frame_investimento()
            Funcs(self.treeview).visualizar_investimentos('')
        elif func == 6:
            Funcs(
                self.entry_codigo, self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario,
                self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto, self.entry_valor_final
            ).limpa_tela()
        elif func == 3:
            if not editar:
                # "0 foi apenas para ocupar espaço na lista"
                Funcs(
                    0,
                    self.entry_data, self.entry_qnt_de_papeis, self.entry_valor_unitario, self.varCV,
                    self.entry_taxa_corretagem, self.entry_valor_da_operacao, self.entry_imposto,
                    self.entry_valor_final,
                    self.entry_codigo,
                ).salvar()
            else:
                try:
                    id_list = self.treeview.selection()[0]  # como só será selecionado um item, na tupla ele
                    # sempre será 0
                    Funcs(
                        self.treeview,
                        self.entry_data_edit, self.entry_qnt_de_papeis_edit, self.entry_valor_unitario_edit,
                        self.editar_varCV, self.entry_taxa_corretagem_edit, self.entry_valor_da_operacao_edit,
                        self.entry_imposto_edit, self.entry_valor_final_edit, self.new_window,
                        self.treeview.item(id_list, "values")[0]
                    ).salvar(update=True)
                except ValueError as err:
                    print(err)
                    messagebox.showerror(title="ERROR", message="Não há itens para remover!")
                except TypeError as err:
                    print(err)
                    messagebox.showerror(title="ERROR", message="Não há itens para remover!")
        elif func == 4:
            self.__tela_editar()
        elif func == 9:
            if not editar:
                pass
            else:
                Funcs(
                    self.entry_qnt_de_papeis_edit.get(), self.entry_valor_unitario_edit.get(),
                    self.entry_taxa_corretagem_edit.get(), self.entry_valor_da_operacao_edit,
                    self.entry_imposto_edit, self.entry_valor_final_edit
                ).calcular()
        elif func == 5:
            try:
                id_list = self.treeview.selection()[0]  # como só será selecionado um item, na tupla ele
                # sempre será 0
                Funcs(
                    self.treeview, self.treeview.item(id_list, "values")[0], self.treeview.item(id_list, "values")[1],
                    self.treeview.item(id_list, "values")[2], 0
                ).remover()
            except TypeError as err:
                print(err)
                messagebox.showerror(title="ERROR", message="Selecione um item para remover")
            except IndexError as err:
                print(err)
                messagebox.showerror(title="ERROR", message="Selecione um item para remover")
            except ValueError as err:
                print(err)
                messagebox.showerror(title="ERROR", message="Selecione um item para remover")

    def __bt_voltar(self):
        bt_voltar = Button(self.inicio_frame, text='Voltar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                           borderwidth=2, highlightbackground='black', command=lambda: self.__chamada(2))

        bt_voltar.place(x=20, y=10, relheight=0.07)

    def __frame_principal(self):
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
                            command=lambda: self.__chamada(1))
        acess = tk.Button(self.options_frame, text='Investimentos', font=('KacstOffice', '10'), bg='#2fc7f4',
                          command=lambda: self.__chamada(7))

        #   CONFIGURANDO FRAME PRINCIPAL
        # |---botoes---|
        cad_btn.pack(pady=100, anchor='center')
        acess.pack(anchor='center')
        # |---linha---|
        l_linha.place(x=0, y=70)
        title_op.place(x=45, y=20)

    def __frame_Tela_Inicio(self):
        #   CRIANDO FRAME DE TELA DE INICIO
        self.inicio_frame = Frame(self.root, background='black')

        #   CONFIGURANDO FRAME
        self.inicio_frame.place(x=150, relheight=1, relwidth=1)

    def __seja_bem_vindoA(self, frame=False):
        #   CHAMANDO FRAME DE TELA INICIAL
        if frame:
            self.__frame_Tela_Inicio()
        # Foto bg
        self.imagem = tk.PhotoImage(file='b3.png')
        self.imagem.subsample(1, 1)
        self.imagem_fundo = Label(self.inicio_frame, image=self.imagem)
        self.imagem_fundo.place(x=180, y=140, relwidth=0.333, relheight=0.28)

        # label
        bem_vindo = tk.Label(self.inicio_frame, text='SEJA BEM-VINDO(A)', font=('KacstOffice', '15'), bg='black',
                             fg='#2fc7f4')
        bem_vindo.place(x=202, y=20)

    def __frame_cadastro(self):
        def calcular(*args):
            lista = list(args)

            # verificação de erros
            # garantindo que em QNT. DE PAPEIS os valores numéricos sejam numéricos
            if not lista[0].get() == '':
                # testa de é possivel converter para INTEIRO
                try:
                    if lista[0].get().count(",") >= 1 or lista[0].get().count(".") >= 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Qtn. De Papeis" não pode ter ponto ou vírgula')
                        lista[0].delete(0, END)
                        lista[0].insert(END, "0")
                        lista[0] = int(lista[0].get())
                    else:
                        # testando erro para garantir apenas valores numericos
                        lista[0] = int(lista[0].get())
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Qnt. De Papeis" só aceita valores numéricos!')
                    lista[0].delete(0, END)
                    lista[0].insert(END, "0")
                    lista[0] = int(lista[0].get())
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Qtn. De Papeis", não pode estar vazío!')
                lista[0] = 0

            # garantindo que em VALOR UNIT. os valores numéricos sejam numéricos
            if not lista[1].get() == '':
                # testa de é possivel converter para FLOAT
                try:
                    if lista[1].get().count(",") > 1 or lista[1].get().count(".") > 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Valor Unit." só aceita valores numéricos com apenas um ponto '
                                             'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis '
                                             'reais'
                                             ' e setenta e oito centavos)')
                        lista[1].delete(0, END)
                        lista[1].insert(END, "0.0")
                        lista[1] = float(lista[1].get().replace(",", "."))
                    else:
                        if lista[1].get().count(",") == 1:
                            val_formatado = lista[1].get().replace(",", ".")
                            lista[1].delete(0, END)
                            lista[1].insert(END, val_formatado)
                        lista[1] = float(lista[1].get().replace(",", "."))
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Valor Unit" só aceita valores numéricos!')
                    lista[1].delete(0, END)
                    lista[1].insert(END, "0.0")
                    lista[1] = float(lista[1].get().replace(",", "."))
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Valor Unit.", não pode estar vazío!')
                lista[1] = 0.0

            # garantindo que em CORRETAGEM. os valores numéricos sejam numéricos
            if not lista[2].get() == '':
                # testa de é possivel converter para FLOAT
                try:
                    if lista[2].get().count(",") > 1 or lista[2].get().count(".") > 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Corretagem." só aceita valores numéricos com apenas um ponto '
                                             'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis '
                                             'reais'
                                             ' e setenta e oito centavos)')
                        lista[2].delete(0, END)
                        lista[2].insert(END, "0.0")
                        lista[2] = float(lista[2].get().replace(",", "."))
                    else:
                        if lista[2].get().count(",") == 1:
                            val_formatado = lista[2].get().replace(",", ".")
                            lista[2].delete(0, END)
                            lista[2].insert(END, val_formatado)
                        lista[2] = float(lista[2].get().replace(",", "."))
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Corretagem" só aceita valores numéricos!')
                    lista[2].delete(0, END)
                    lista[2].insert(END, "0.0")
                    lista[2] = float(lista[2].get().replace(",", "."))
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Corretagem", não pode estar vazío!')
                lista[2] = 0.0

            # calculo do valor da operação
            valor_operacao = (lista[0] * lista[1]) + lista[2]
            # calculo do imposto
            imposto = valor_operacao * (0.0300 / 100)
            # calculo do valor final
            valor_final = imposto + valor_operacao

            # pondo no estado norma para editar
            lista[3].configure(state='normal')
            lista[4].configure(state='normal')
            lista[5].configure(state='normal')

            # excluindo dados das entrys
            lista[3].delete(0, END)
            lista[4].delete(0, END)
            lista[5].delete(0, END)

            # pondo dados nas entrys
            lista[3].insert(END, f'{valor_operacao:.2f}')
            lista[4].insert(END, f'{imposto:.2f}')
            lista[5].insert(END, f'{valor_final:.2f}')

            # impedindo usuário mexa nessa parte
            lista[3].configure(state='readonly')
            lista[4].configure(state='readonly')
            lista[5].configure(state='readonly')

            self.inicio_frame.after(2500, calcular, self.entry_qnt_de_papeis, self.entry_valor_unitario,
                                    self.entry_taxa_corretagem, self.entry_valor_da_operacao,
                                    self.entry_imposto, self.entry_valor_final, self.inicio_frame)

        # LISTA e VAR PARA OPTIONMENU
        listaOP = ['----', 'Compra', 'Venda']
        self.varCV = StringVar()
        self.varCV.set(listaOP[0])

        #   CRIANDO BOTOES, LABELS, ENTRYS e OPTIONSMENU
        # |---BOTÃO--|
        self.__bt_voltar()
        self.bt_limpar = Button(self.inicio_frame, text='Limpar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.__chamada(6, new_frame=False))
        self.bt_salvar = Button(self.inicio_frame, text='Salvar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.__chamada(3, new_frame=False))
        self.bt_data = Button(self.inicio_frame, text='Data', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                              borderwidth=2, highlightbackground='black',
                              command=lambda: self.__chamada(8, new_frame=False))
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
        # |---ENTRY INSERTS INICIAIS---|
        self.entry_qnt_de_papeis.insert(0, '0')
        self.entry_valor_unitario.insert(0, '0.0')
        self.entry_taxa_corretagem.insert(0, '0.0')

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
        # |---FAZ O CALCULO A CADA 2s---|
        calcular(self.entry_qnt_de_papeis, self.entry_valor_unitario,
                 self.entry_taxa_corretagem, self.entry_valor_da_operacao,
                 self.entry_imposto, self.entry_valor_final, self.inicio_frame)

    def __treeview_frame(self):
        #   CRIANDO FRAME PARA TREEVIEW
        self.tree_frame = Frame(self.inicio_frame, background='gray8')

        #   CONFIGURANDO FRAME
        self.tree_frame.place(y=80, x=10, width=580, height=312)

    def __frame_investimento(self):
        def filtar(coluna, concatena, numeric=False):

            # Obtendo o estado atual de classificação da coluna
            current_state = self.estado_atual[coluna]

            # Classificando os dados de acordo com a ordem atual
            items = [(self.treeview.set(k, coluna), k) for k in self.treeview.get_children('')]
            if numeric:
                # se for numerico vamos converter
                items = [(float(item[0]), item[1]) for item in items]
            items.sort(reverse=current_state[0])

            # Atualizando o estado de classificação da coluna
            new_state = (not current_state[0],)
            self.estado_atual[coluna] = new_state

            # Atualizando a exibição em árvore com os dados classificados
            for index, (val, k) in enumerate(items):
                self.treeview.move(k, '', index)  # .move() vai mover o item para cima ou para baixo na coluna

                # Atualizando o ícone do cabeçalho da coluna
                if not current_state[0]:
                    self.treeview.heading(coluna, text=concatena + '↑')  # ascendente
                else:
                    self.treeview.heading(coluna, text=concatena + '↓')  # descendente

            # fazendo as outras colunas voltarem ao titulo normal
            for col in self.treeview['columns']:
                if col != coluna:
                    self.treeview.heading(col, text=col)

        def on_selected(event):
            funcao = Funcs(self.treeview)
            if self.filtrando.get() != 'TODOS':
                validar = funcao.visualizar_investimentos(self.filtrando.get(), ativo=True)
                print(validar)
                # se retornar uma lista vazia
                if not validar:
                    messagebox.showerror(title='Controle de investimentos', message='Esse ativo não existe'
                                                                                    ' mais na base dados. '
                                                                                    'A lista foi atualizada')
                    combobox()
            else:
                funcao.visualizar_investimentos('')

        def combobox():
            # variavel para ComboBox
            self.lista = ['TODOS']
            # acrescenta valores à lista da Base de Dados
            banco = BancoDeDados('Investimentos')
            lista_ativos = banco.select("*", "Ativos")
            print("\t\t\tLISTA DE ATIVOS\n", lista_ativos)
            print()
            for ativo in lista_ativos:
                self.lista.append(ativo[0])
            self.filtrando = ttk.Combobox(self.tree_frame, values=self.lista,
                                          background='gray8', justify='center')
            self.filtrando.place(relx=0.1, rely=0.035)
            self.filtrando.configure(width=8)
            self.filtrando.bind("<<ComboboxSelected>>", on_selected)
        #   CRIANDO BOTOES e LABELS frame inicio_frame
        # |---BOTÃO--|
        self.__bt_voltar()
        # |---LABEL---|
        lb_cadastrar_investimento = Label(self.inicio_frame, text="Seus Investimentos", font=('KacstOffice', '15'),
                                          bg='black', fg='#2fc7f4')

        #   CHAMANDO FRAME TREEVIEW
        self.__treeview_frame()

        lbl_filtro = Label(self.tree_frame, text='Filtro', background='gray8', foreground='white')
        # |---LABEL---|
        lb_cadastrar_investimento.place(x=180, y=12)
        lbl_filtro.place(relx=0.015, rely=0.035)

        #   CRIANDO BOTOES, TREEVIEW e ComboBox
        # |---BOTÃO--|
        self.bt_remover = Button(self.tree_frame, text='Remover', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                 borderwidth=2, highlightbackground='black',
                                 command=lambda: self.__chamada(5, new_frame=False))
        self.bt_editar = Button(self.tree_frame, text='Editar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.__chamada(4, new_frame=False))
        # |---TREEVIEW---|
        self.treeview = ttk.Treeview(self.tree_frame, height=3)
        # |---COMBOBOX---|
        combobox()
        # |---SCROLLBAR---|
        #   se não defininir o command na Scrollbar e não configurar a qauntidade de colunas na treeview a barra de
        #   rolagem provavelmente não funcionará
        self.scrollbar_vertical = Scrollbar(self.tree_frame, orient='vertical', command=self.treeview.yview)
        self.scrollbar_horizontal = Scrollbar(self.tree_frame, orient='horizontal', command=self.treeview.xview)
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)

        #   CONFIGURANDO BOTOES e TREEVIEW
        # |---BOTÃO--|
        self.bt_remover.place(relx=0.83, rely=0.015)
        self.bt_editar.place(relx=0.70, rely=0.015)
        # |---TREEVIEW---|
        self.treeview.place(rely=0.13, relx=0.015, relwidth=0.937, relheight=0.805)
        self.treeview["columns"] = ("ID", "Cod. Ativo",
                                    "Data", "Qtd. Papéis",
                                    "Valor Unitário", "Compra/Venda",
                                    "Corretagem", "Valor da Operação",
                                    "Imposto", "Valor final")
        self.treeview['show'] = 'headings'  # mostrar os cabeçalhos
        # usado para ajudar na lógica do filtro
        self.estado_atual = {'ID': (False,), 'Cod. Ativo': (False,),
                             'Data': (False,), 'Qtd. Papéis': (False,),
                             'Valor Unitário': (False,), 'Compra/Venda': (False,),
                             'Corretagem': (False,), 'Valor da Operação': (False,),
                             'Imposto': (False,), 'Valor final': (False,)}
        # cabeçalho
        self.treeview.heading('ID', text='ID',
                              command=lambda: filtar('ID', 'ID', numeric=True, ))
        self.treeview.heading('Cod. Ativo', text='Cod. Ativo',
                              command=lambda: filtar('Cod. Ativo', 'Cod. Ativo'))
        self.treeview.heading('Data', text='Data',
                              command=lambda: filtar('Data', 'Data'))
        self.treeview.heading('Qtd. Papéis', text='Qtd. Papéis',
                              command=lambda: filtar('Qtd. Papéis', 'Qtd. Papéis', numeric=True))
        self.treeview.heading('Valor Unitário', text='Valor Unitário',
                              command=lambda: filtar('Valor Unitário', 'Valor Unitário', numeric=True))
        self.treeview.heading('Compra/Venda', text='Compra/Venda',
                              command=lambda: filtar('Compra/Venda', 'Compra/Venda'))
        self.treeview.heading('Corretagem', text='Corretagem',
                              command=lambda: filtar('Corretagem', 'Corretagem', numeric=True))
        self.treeview.heading('Valor da Operação', text='Valor da Operação',
                              command=lambda: filtar('Valor da Operação', 'Valor da Operação', numeric=True))
        self.treeview.heading('Imposto', text='Imposto',
                              command=lambda: filtar('Imposto', 'Imposto', numeric=True))
        self.treeview.heading('Valor final', text='Valor final',
                              command=lambda: filtar('Valor final', 'Valor final', numeric=True))
        # espaçamento das colunas
        self.treeview.column("ID", width=30, anchor='c', minwidth=30)
        self.treeview.column("Cod. Ativo", width=90, anchor='c',minwidth=90)
        self.treeview.column("Data", width=90, anchor='c',minwidth=90)
        self.treeview.column("Qtd. Papéis", width=100, anchor='c',minwidth=100)
        self.treeview.column("Valor Unitário", width=120, anchor='c', minwidth=120)
        self.treeview.column("Compra/Venda", width=120, anchor='c', minwidth=120)
        self.treeview.column("Corretagem", width=120, anchor='c', minwidth=120)
        self.treeview.column("Valor da Operação", width=180, anchor='c',minwidth=180)
        self.treeview.column("Imposto", width=90, anchor='c', minwidth=90)
        self.treeview.column("Valor final", width=120, anchor='c',minwidth=120)
        # |---CROLLBAR---|
        self.scrollbar_vertical.place(relx=0.955, rely=0.13, relheight=0.85)
        self.scrollbar_horizontal.place(relx=0.015, rely=0.94, relwidth=0.9365)

    def __nova_tela(self, width, height, locateY=2, locateX=2):
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

    def __tela_editar(self):
        def calcular(*args):
            lista = list(args)

            # verificação de erros
            # garantindo que em QNT. DE PAPEIS os valores numéricos sejam numéricos
            if not lista[0].get() == '':
                # testa de é possivel converter para INTEIRO
                try:
                    if lista[0].get().count(",") >= 1 or lista[0].get().count(".") >= 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Qtn. De Papeis" não pode ter ponto ou vírgula')
                        lista[0].delete(0, END)
                        lista[0].insert(END, "0")
                        lista[0] = int(lista[0].get())
                    else:
                        # testando erro para garantir apenas valores numericos
                        lista[0] = int(lista[0].get())
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Qnt. De Papeis" só aceita valores numéricos!')
                    lista[0].delete(0, END)
                    lista[0].insert(END, "0")
                    lista[0] = int(lista[0].get())
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Qtn. De Papeis", não pode estar vazío!')
                lista[0] = 0

            # garantindo que em VALOR UNIT. os valores numéricos sejam numéricos
            if not lista[1].get() == '':
                # testa de é possivel converter para FLOAT
                try:
                    if lista[1].get().count(",") > 1 or lista[1].get().count(".") > 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Valor Unit." só aceita valores numéricos com apenas um ponto '
                                             'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis '
                                             'reais'
                                             ' e setenta e oito centavos)')
                        lista[1].delete(0, END)
                        lista[1].insert(END, "0.0")
                        lista[1] = float(lista[1].get().replace(",", "."))
                    else:
                        if lista[1].get().count(",") == 1:
                            val_formatado = lista[1].get().replace(",", ".")
                            lista[1].delete(0, END)
                            lista[1].insert(END, val_formatado)
                        lista[1] = float(lista[1].get().replace(",", "."))
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Valor Unit" só aceita valores numéricos!')
                    lista[1].delete(0, END)
                    lista[1].insert(END, "0.0")
                    lista[1] = float(lista[1].get().replace(",", "."))
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Valor Unit.", não pode estar vazío!')
                lista[1] = 0.0

            # garantindo que em CORRETAGEM. os valores numéricos sejam numéricos
            if not lista[2].get() == '':
                # testa de é possivel converter para FLOAT
                try:
                    if lista[2].get().count(",") > 1 or lista[2].get().count(".") > 1:
                        messagebox.showerror('Controle de investimentos',
                                             'O campo "Corretagem." só aceita valores numéricos com apenas um ponto '
                                             'decimal, por exemplo:\n1456.78\t(mil quatrocentos e cinquenta e seis '
                                             'reais'
                                             ' e setenta e oito centavos)')
                        lista[2].delete(0, END)
                        lista[2].insert(END, "0.0")
                        lista[2] = float(lista[2].get().replace(",", "."))
                    else:
                        if lista[2].get().count(",") == 1:
                            val_formatado = lista[2].get().replace(",", ".")
                            lista[2].delete(0, END)
                            lista[2].insert(END, val_formatado)
                        lista[2] = float(lista[2].get().replace(",", "."))
                except ValueError as err:
                    print(err)
                    messagebox.showerror('Controle de investimentos',
                                         'O campo "Corretagem" só aceita valores numéricos!')
                    lista[2].delete(0, END)
                    lista[2].insert(END, "0.0")
                    lista[2] = float(lista[2].get().replace(",", "."))
            else:
                messagebox.showerror('Controle de investimentos', 'O campo "Corretagem", não pode estar vazío!')
                lista[2] = 0.0

            # calculo do valor da operação
            valor_operacao = (lista[0] * lista[1]) + lista[2]
            # calculo do imposto
            imposto = valor_operacao * (0.0300 / 100)
            # calculo do valor final
            valor_final = imposto + valor_operacao

            # pondo no estado norma para editar
            lista[3].configure(state='normal')
            lista[4].configure(state='normal')
            lista[5].configure(state='normal')

            # excluindo dados das entrys
            lista[3].delete(0, END)
            lista[4].delete(0, END)
            lista[5].delete(0, END)

            # pondo dados nas entrys
            lista[3].insert(END, f'{valor_operacao:.2f}')
            lista[4].insert(END, f'{imposto:.2f}')
            lista[5].insert(END, f'{valor_final:.2f}')

            # impedindo usuário mexa nessa parte
            lista[3].configure(state='readonly')
            lista[4].configure(state='readonly')
            lista[5].configure(state='readonly')

            self.new_window.after(2000, calcular, self.entry_qnt_de_papeis_edit, self.entry_valor_unitario_edit,
                                  self.entry_taxa_corretagem_edit, self.entry_valor_da_operacao_edit,
                                  self.entry_imposto_edit, self.entry_valor_final_edit, self.new_window)

        # usar para selecionar na lista da treeview
        # verifica se tem um item selecionado
        if not self.treeview.selection() == ():
            # print(self.lista[0].selection()) # a função selection() retornará uma tupla, se nenhum item for
            # selecionado retornará uma tupla vazia ()
            id_list = self.treeview.selection()[0]  # como só será selecionado um item, na tupla ele sempre será 0

            # LISTA e VAR PARA OPTIONMENU
            listaOP = ['----', 'Compra', 'Venda']
            self.editar_varCV = StringVar()

            self.__nova_tela(350, 450, locateX=4, locateY=2)

            # CONFIGURANDO
            # |---Labels---|
            lbl_editar = Label(self.new_window, text='Editar', font=('KacstOffice', '15'), bg='black', fg='white')
            lbl_linha = Label(self.new_window, text='', width=700, height=1, anchor=NW, font=' Ivy 1 ', bg='#2fc7f4',
                              highlightbackground='#F2F2F2')
            lbl_linha_2 = Label(self.new_window, text='', width=700, height=1, anchor=NW, font=' Ivy 1 ', bg='#2fc7f4',
                                highlightbackground='#F2F2F2')
            lbl_ativo = Label(self.new_window, text=f'{self.treeview.item(id_list, "values")[1]}',
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
                                  fg='white', borderwidth=2, highlightbackground='black',
                                  command=lambda: self.new_window.destroy())
            btn_salvar = Button(self.new_window, text='Salvar', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                                borderwidth=2, highlightbackground='black',
                                command=lambda: self.__chamada(3, new_frame=False, editar=True))
            btn_data = Button(self.new_window, text='Data', font=('KacstOffice', '10'), bg='#02347c', fg='white',
                              borderwidth=2, highlightbackground='black',
                              command=lambda: self.__chamada(8, new_frame=False, editar=True))
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

            calcular(self.entry_qnt_de_papeis_edit, self.entry_valor_unitario_edit,
                     self.entry_taxa_corretagem_edit, self.entry_valor_da_operacao_edit,
                     self.entry_imposto_edit, self.entry_valor_final_edit, self.new_window)

        else:
            messagebox.showerror('Controle de investimentos',
                                 'SELECIONE UM ITEM PARA EDITAR')
            return False


Application().iniciar()
