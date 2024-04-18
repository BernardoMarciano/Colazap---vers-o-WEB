import mysql.connector

class Conexao():
    def conectar():
        mydb = mysql.connector.connect(
            host="10.110.140.136",
            user="equipe",
            password="123456789",
            database="colazap"
            )

        return mydb
