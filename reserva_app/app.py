from flask import Flask, render_template
from reserva_app.funcoes import add_banco, obter_dados, obter_dados_login, verificacao_usuario
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

@app.route("/reserva/detalhe_reserva")
def detalhe_reserva():
    return render_template("/reserva/detalhe_reserva.html")

#Rota usada para cadastro de usuários
@app.route("/cadastro", methods = ['POST'])
def cadastrar_usuario():
    nome, email, password = obter_dados()
    add_banco(nome, email, password)
    
    return render_template("login.html")

#Rota usada para ler infos do login
@app.route("/", methods = ['POST'])
def login():
    email, password = obter_dados_login()
    verificacao_resultado, nome_usuario = verificacao_usuario(email, password)
    if verificacao_resultado == True:
        return render_template("reservas.html", nome_usuario = nome_usuario)
    else:
        return render_template("login.html", erro="O email ou senha estão incorretos, tente novamente")


app.run(debug=True)
