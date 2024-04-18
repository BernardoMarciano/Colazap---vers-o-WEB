from conexao import Conexao
from hashlib import sha256


class Usuario():
    def __init__(self):
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False

    def cadastrar(self, nome, telefone, senha):
        try:
            mydb = Conexao.conectar()

            mycursor = mydb.cursor()

            # Criptografando a senha
            senha= sha256(senha.encode()).hexdigest()

            sql = "INSERT INTO tb_usuario (nome, tel, senha) VALUES (%s, %s, %s)"
            valores = (nome, telefone, senha)

            mycursor.execute(sql, valores)    
            mydb.commit()

            self.nome = nome
            self.tel = telefone
            self.senha = senha
            self.logado = True

            return True
        
        except:
            return False
        
    def logar(self,telefone,senha):
        # Criptografando a senha
        senha= sha256(senha.encode()).hexdigest()

        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        sql = "SELECT nome, tel, senha FROM tb_usuario where tel = %s and BINARY senha = %s;"
        valores = [telefone,senha]

        mycursor.execute(sql,valores)

        resultado = mycursor.fetchone()
        
        if not resultado == None:
            self.logado = True
            self.nome = resultado[0]
            self.telefone = resultado[1]
            self.senha = resultado[2]

        else:
            self.logado = False