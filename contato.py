from usuario import Usuario
from conexao import Conexao

def mostar_contatos():
    mydb = Conexao.conectar()
    mycursor = mydb.cursor()

    sql = "SELECT nome, mensagem FROM tb_mensagem INNER JOIN tb_usuario ON tb_mensagem.tel_remetente = tb_usuario.tel "

    mycursor.execute(sql)

    resultado = mycursor.fetchall()