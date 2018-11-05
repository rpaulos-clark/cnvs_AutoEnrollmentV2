import pyodbc


class PyDB(object):

    def __init__(self, server, database):
        self.connection = pyodbc.connect(
            r'DRIVER={ODBC DRiver 11 for SQL Server};'
            r'SERVER='+str(server)+';'
            r'DATABASE='+str(database)+';'
            r'Trusted_connection=yes;'
        )
        self.cursor = self.connection.cursor()

    def select_table(self, table):
        data_cursor = self.cursor.execute(
            'select * from {}'.format(table)
        )
        return data_cursor.fetchall()

    def call_procedure(self, procedure):
        data_cursor = self.cursor.execute(
            "{CALL"+str(procedure)+"}"
        )
        return data_cursor.fetchall()
