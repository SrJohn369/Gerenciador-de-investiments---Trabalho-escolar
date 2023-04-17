from tkinter import *
from tkinter import messagebox
import sqlite3


class BancoDeDados:

    def abrirBanco(self, nomeBanco='Investimentos'):
        self.banco = sqlite3.connect(f'{nomeBanco}.db')
        self.cursor = self.banco.cursor()

    def criarTabela(self, nomeTabela: str, colunasEDados: str) -> bool:
        self.abrirBanco()

        try:
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nomeTabela} 
                                ({colunasEDados});""")
        except sqlite3.OperationalError as err:
            print(err)
            return False

        self.banco.commit()
        return True

    def atualizarTabela(self, nomeTabela: str, set:str, where:str):
        self.abrirBanco()

        self.cursor.execute(f"""
        UPDATE {nomeTabela}
        SET {set}
        WHERE {where};""")

    def introduzirDados(self, nomeTabela: str, especifico: bool, Valores: str,
                        columEspecificas: str = 'Default') -> bool:
        self.abrirBanco()

        if especifico:
            try:

                self.cursor.execute(f"""INSERT INTO {nomeTabela}
                                    ({columEspecificas})
                                        VALUES 
                                    ({Valores});""")

            except sqlite3.OperationalError as err:
                print(err)
                return False

        else:
            try:
                self.cursor.execute(f"""INSERT INTO {nomeTabela}
                                        VALUES 
                                    ({Valores});""")

            except sqlite3.OperationalError as err:
                print(err)
                return False

        self.banco.commit()
        return True

    def delete(self, tabela: str) -> bool:
        self.abrirBanco()

        try:
            self.cursor.execute(f"""DROP TABLE {tabela};""")
            self.banco.commit()
            return True
        except sqlite3.OperationalError as err:
            print(err)
            return False

    def select(self, select: str, from1: str):
        for row in self.cursor.execute(f"SELECT {select} FROM {from1}"):
            print(row)


dado1 = BancoDeDados()
dado1.abrirBanco()
dado1.criarTabela("Ativo", "Ativo VARCHAR(7) PRIMARY KEY")
dado1.criarTabela("DadosAtivo", "ativo VARCHAR(7),"
                                " data DATE,"
                                " qtd_papel SMALLINT,"
                                " FOREIGN KEY (ativo) REFERENCES Ativo(ativo)")
dado1.introduzirDados("Ativo",False,"PETR4")
dado1.introduzirDados("DadosAtivo",False,"PETR4,"
                                         "2022-03-02,"
                                         "100,")
dado1.select('*', "DadosAtivo")
