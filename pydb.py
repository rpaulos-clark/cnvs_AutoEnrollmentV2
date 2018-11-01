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

    def table(self, table):
        data_cursor = self.cursor.execute(
            'select * from {}'.format(table)
        )
        return data_cursor.fetchall()

    def procedure(self, procedure):
        data_cursor = self.cursor.execute(
            "{CALL"+procedure+"}"
        )
        return data_cursor.fetchall()


db = PyDB('prometheus', 'IRKanna')
data = db.procedure('[CouncilConnect].[usp_CouncilConnect_getEnrollmentList_StopGap]')
print(data)