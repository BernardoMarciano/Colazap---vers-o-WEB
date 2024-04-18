# Importa o flask
from flask import Flask, render_template, request, redirect, session, jsonify
from usuario import Usuario
from chat import Chat
from contatos import Contatos
from hashlib import sha256

# Cria o servidor
app = Flask(__name__)

app.secret_key = "abc123"

usuario = Usuario()
     
@app.route("/", methods= ["GET","POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        usuario.cadastrar(nome,telefone,senha)
        return render_template("login.html")

    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        
        usuario.logar(telefone,senha)
        
        if usuario.logado:
            session['usuario_logado'] = {"nome":usuario.nome, "telefone":usuario.telefone}
            return redirect("/chat")  
       
        else:
            session.clear()
            return "Erro ao logar"
    else:
        return render_template("login.html")

@app.route("/chat")
def chat():
    if 'usuario_logado' in session:
        return render_template("chat.html")
    else:
        return redirect("/")

@app.route("/mostrar_usuarios")
def solicitarUsuarios():

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)

    contatos = chat.retornar_contatos()

    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    chat = Chat(nome_usuario,telefone_usuario)

    destinatario = Contatos("",tel_destinatario)
    mensagens = chat.verificar_mensagem(0, destinatario)

    return jsonify(mensagens), 200

@app.route("/post/mensagens", methods=["POST"])
def post_mensagem():
    if "usuario_logado" in session:
        dados = request.json
        mensagem = dados.get("mensagem")
        tel_destinatario = dados.get("tel_destinatario")

        if mensagem and tel_destinatario:
            nome_usuario = session["usuario_logado"]["nome"]
            telefone_usuario = session["usuario_logado"]["telefone"]
            chat = Chat(nome_usuario, telefone_usuario)

            if chat.mandar_mensagem(mensagem, tel_destinatario):
                return jsonify({"status": "Mensagem enviada com sucesso"}), 200
            else:
                return jsonify({"status": "Erro ao enviar mensagem"}), 500

app.run(debug= True)