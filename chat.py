from usuario import Usuario
from mensagem import Mensagem
from conexao import Conexao
from contatos import Contatos

class Chat:
    def __init__(self, nome_usuario: str, telefone_usuario: str):
       self.nome_usuario = nome_usuario
       self.telefone_usuario = telefone_usuario

    def enviar_mensagem(self,conteudo:str) -> bool:
        try: 
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            tel_remetente = self.telefone_usuario 
            tel_destinatario = None
            self.conteudo = conteudo
            mensagem = self.conteudo

            sql = "INSERT INTO tb_mensagem (tel_remetente, tel_destinatario, mensagem) VALUES (%s, %s, %s)"
            valores = (tel_remetente, tel_destinatario, mensagem)

            mycursor.execute(sql, valores)    
            mydb.commit()

            return True
        
        except:
            return False 
        
    def verificar_mensagem(self, quantidade:int, contato:Contatos):
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = f"SELECT nome, mensagem FROM tb_mensagem m INNER JOIN tb_usuario u ON m.tel_remetente = u.tel WHERE m.tel_remetente = '{self.telefone_usuario}' AND m.tel_destinatario = '{contato.telefone}' OR m.tel_remetente = '{contato.telefone}' AND m.tel_destinatario = '{self.telefone_usuario}' ORDER BY m.id_mensagem"

        mycursor.execute(sql)

        resultado = mycursor.fetchall()

        mydb.close()
        
        lista_mensagens = []

        for linha in resultado:
            # Tudo em uma linha só
            # lista_mensagens.append(Mensagem(linha[0],linha[1]))

            # Criando a mensagem primeiro e incluindo na lista
            mensagem = {"nome":linha[0], "mensagem":linha[1]}
            lista_mensagens.append(mensagem)

        return(lista_mensagens)

    def retornar_contatos(self):
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = "SELECT nome, tel FROM tb_usuario ORDER BY nome"

        mycursor.execute(sql)

        resultado = mycursor.fetchall()

        lista_contatos = []

        lista_contatos.append({"nome":"TODOS", "telefone":""})

        for linha in resultado:
            # Tudo em uma linha só
            # lista_contatos.append(Contato(linha[0],linha[1]))

            # Criando a mensagem primeiro e incluindo na lista
            contato = {"nome": linha[0], "telefone": linha[1]}
            lista_contatos.append(contato)
        
        return(lista_contatos)

    def mandar_mensagem(self, mensagem:str, tel_destinatario:Contatos) -> bool:
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        sql = "INSERT INTO tb_mensagem (tel_remetente, mensagem, tel_destinatario) VALUES (%s,%s,%s)"

        val= (self.telefone_usuario, mensagem, tel_destinatario)
        mycursor.execute(sql,val)

        mydb.commit()

        return True