from flask import Flask, render_template, session
from reserva_app.funcoes import add_banco_usuarios, add_banco_salas, obter_dados,obter_dados_sala, verificacao_usuario, procurar_reserva
import os

 
app = Flask(__name__, template_folder=os.path.abspath('templates'))

@app.route("/")
def home():
    return render_template ("login.html")

@app.route("/cadastrar_sala")
def cadastrar_sala():
    return render_template ("cadastrar_sala.html")

@app.route("/cadastro")
def cadastro():
    return render_template ("cadastro.html")

@app.route("/listar_salas")
def listar_salas():
    return render_template("listar_salas.html")

@app.route("/reservar_sala")
def reservar_sala():
    return render_template("reservar_sala.html")

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

@app.route("/reserva/detalhe_reserva", methods = ["POST"])
def detalhe_reserva():
    return render_template("/reserva/detalhe_reserva.html")

#Rota usada para cadastro de usuários
@app.route("/cadastro", methods = ['POST'])
def cadastrar_usuario():
    nome, sobrenome, email, password = obter_dados()
    if nome == "":
        return render_template("cadastro.html", erro = "Você não tem nome?")
    
    elif sobrenome == "":
        return render_template("cadastro.html", erro = "Seus pais esqueceram do seu sobrenome?", nome = nome)
    
    elif email == "":
        return render_template("cadastro.html", erro = "Esse email não existe", nome = nome, sobrenome = sobrenome)
    
    elif password == "":
        return render_template("cadastro.html", erro = "Última vez que não coloquei senha em algo não tive um bom resultado...", nome = nome, sobrenome = sobrenome, email = email)
    
    else:
        add_banco_usuarios(nome, sobrenome, email, password)
    
    return render_template("login.html")

#Rota usada para ler infos do login
@app.route("/", methods = ['POST'])
def login():
    _,_,email, password = obter_dados()
    if email == "" and password == "":
        return render_template ("login.html", erro = "Você deve inserir um email e senha")
    elif email == "":
        return render_template ("login.html", erro = "Você deve inserir um email")
    elif password == "":
        return render_template ("login.html", erro = "Você deve inserir uma senha", email = email)
    else:
        verificacao_resultado, nome_usuario, sobrenome_usuario = verificacao_usuario(email, password)
        if verificacao_resultado == True:
            session["nome_usuario"] = nome_usuario
            session["sobrenome_usuario"] = sobrenome_usuario
            return render_template("reservas.html", nome_usuario = nome_usuario, email = email)
        else:
            return render_template("login.html", erro="O email ou senha estão incorretos, tente novamente")

#Rota usada para filtragem na página de reservas
@app.route("/filtrar", methods = ["POST"])
def filtrar():
    nome, sobrenome,_,_ = obter_dados() 
    nome_usuario = session.get("nome_usuario")
    if nome == "":
        return render_template("reservas.html", erro = "Digite o seu nome", linha = None, nome_usuario = nome_usuario)
    elif sobrenome == "":
        return render_template("reservas.html", erro = "Digite o seu sobrenome também", linha = None, nome = nome, nome_usuario = nome_usuario)
    else:
        verificacao_usuario, linha =  procurar_reserva(nome, sobrenome)
        if verificacao_usuario == True:
            return render_template("reservas.html", linha = linha, nome_usuario = nome_usuario)
        else: 
            return render_template("reservas.html", erro = "Reserva não encontrada. Digite novamente ou faça a reserva no nosso site", linha = None, nome_usuario = nome_usuario, nome = nome)
    
#Rota usada para reserva de salas
@app.route("/reservar_sala", methods =["POST"])
def reservas_sala():
    nome = session.get("nome_usuario") 
    sobrenome = session.get("sobrenome_usuario") 
    sala, data_inicio, hora_inicio, data_final, hora_final = obter_dados_sala()
    
    add_banco_salas (nome, sobrenome, sala, data_inicio, hora_inicio, data_final, hora_final)
    
    return render_template ("reserva/detalhe_reserva.html")

app.secret_key = 'teste_sessao' 
app.run(debug=True)
