from app.models.casos import Casos
from app.helpers.data import formata_data

SQL_BUSCA_DADOS = 'SELECT * FROM casos'
SQL_FILTRA_DADOS = 'SELECT id, data, uf, sum(confirmados), sum(mortes) FROM casos WHERE uf = %s AND data BETWEEN %s AND %s GROUP BY data ASC'
SQL_FILTRA_UF = 'SELECT id, data, uf, sum(confirmados), sum(mortes) FROM casos WHERE uf = %s GROUP BY data ASC'
SQL_MIN_MAX = 'SELECT min(data), max(data) FROM casos WHERE uf = %s'
SQL_CONFIRMADOS_MORTES_UF = 'SELECT sum(confirmados), sum(mortes) FROM casos WHERE uf = %s GROUP BY data DESC'
SQL_CONFIRMADOS_MORTES = 'SELECT sum(confirmados), sum(mortes) FROM casos WHERE uf = %s AND data = %s GROUP BY data'
SQL_CONFIRMADOS_UF = 'SELECT uf, sum(confirmados) FROM casos WHERE data = %s GROUP BY uf'
SQL_CONFIRMADOS_UF_DESC = 'SELECT uf, sum(confirmados), sum(mortes) FROM casos WHERE data = %s GROUP BY uf ORDER BY sum(confirmados) DESC'
SQL_INTERVALO_PESQUISAS = 'SELECT uf, min(data), max(data) FROM casos GROUP BY uf'

class CasosDao:
    def __init__(self, db):
        self.db = db

    def para_casos(self, dados):
        # Converte formato DB para objeto Casos.
        lst_casos = [Casos(dado[0], formata_data(dado[1]), dado[2], dado[3], dado[4]) for dado in dados]

        return lst_casos

    def busca_dados(self):
        cur = self.db.connection.cursor()
        cur.execute(SQL_BUSCA_DADOS)
        dados = cur.fetchall()
        casos = self.para_casos(dados)

        return casos

    def filtra_dados(self, uf, data_inicial, data_final):
        cur = self.db.connection.cursor()
        cur.execute(SQL_FILTRA_DADOS, (uf, data_inicial, data_final, ))
        dados = cur.fetchall()
        casos = self.para_casos(dados)

        return casos

    def filtra_uf(self, uf):
        cur = self.db.connection.cursor()
        cur.execute(SQL_FILTRA_UF, (uf, ))
        dados = cur.fetchall()
        casos = self.para_casos(dados)

        return casos

    def min_max(self, uf):
        cur = self.db.connection.cursor()
        cur.execute(SQL_MIN_MAX, (uf, ))
        dados = cur.fetchone()

        return dados

    def confirmados_mortes_uf(self, uf):
        cur = self.db.connection.cursor()
        cur.execute(SQL_CONFIRMADOS_MORTES_UF, (uf, ))
        dados = cur.fetchone()

        return dados

    def confirmados_mortes(self, uf, data_final):
        cur = self.db.connection.cursor()
        cur.execute(SQL_CONFIRMADOS_MORTES, (uf, data_final))
        dados = cur.fetchone()

        return dados

    def confirmados_uf(self, uf):
        cur = self.db.connection.cursor()
        cur.execute(SQL_CONFIRMADOS_UF, (uf, ))
        dados = cur.fetchall()

        return dados

    def confirmados_uf_desc(self, uf):
        cur = self.db.connection.cursor()
        cur.execute(SQL_CONFIRMADOS_UF_DESC, (uf, ))
        dados = cur.fetchall()

        return dados

    def intervalo_pesquisas(self):
        cur = self.db.connection.cursor()
        cur.execute(SQL_INTERVALO_PESQUISAS)
        dados = cur.fetchall()

        return dados