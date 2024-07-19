from flask import Flask, render_template
from reserva_app.funcoes import add_banco, obter_dados, verificacao_usuario, procurar_reserva
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
    nome, sobrenome, email, password = obter_dados()
    if nome == "":
        return render_template("cadastro.html", erro = "Você não tem nome?")
    
    elif sobrenome == "":
        return render_template("cadastro.html", erro = "Seus pais esqueceram do seu sobrenome?")
    
    elif email == "":
        return render_template("cadastro.html", erro = "Algum email deve estar disponível...")
    
    elif password == "":
        return render_template("cadastro.html", erro = "Última vez que não coloquei senha em algo não tive um bom resultado...")
    
    else:
        add_banco(nome, sobrenome, email, password)
    
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
        return render_template ("login.html", erro = "Você deve inserir uma senha")
    else:
        verificacao_resultado, nome_usuario = verificacao_usuario(email, password)
        if verificacao_resultado == True:
            return render_template("reservas.html", nome_usuario = nome_usuario)
        else:
            return render_template("login.html", erro="O email ou senha estão incorretos, tente novamente")

@app.route("/filtrar", methods = ["POST"])
def filtrar():
    nome, sobrenome,_,_ = obter_dados() 
    if nome == "":
        return render_template("reservas.html", erro = "Digite o seu nome", linha = None)
    elif sobrenome == "":
        return render_template("reservas.html", erro = "Digite o seu sobrenome também", linha = None)
    else:
        verificacao_usuario, linha =  procurar_reserva(nome, sobrenome)
        if verificacao_usuario == True:
            return render_template("reservas.html", linha = linha)
        else: 
            return render_template("reservas.html", erro = "Reserva não encontrada. Digite novamente ou faça a reserva no nosso site", linha = None)
    

app.run(debug=True)
