import sqlite3


class BancoDeDados:

    def abrirBanco(self, nomeBanco='DataBase'):
        self.banco = sqlite3.connect(f'{nomeBanco}.db')
        self.cursor = self.banco.cursor()

    def criarTabela(self, nomeTabela: str, colunasEDados: str) -> bool:
        self.abrirBanco()

        try:
            self.cursor.execute(f"""CREATE IF NOT EXISTS {nomeTabela} 
                                ({colunasEDados});""")
        except sqlite3.OperationalError as err:
            print(err)
            return False

        self.banco.commit()
        return True

    def atualizarTabela(self, nomeTabela: str, ):
        pass

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
            return True
        except sqlite3.OperationalError as err:
            print(err)
            return False

        self.banco.commit()
