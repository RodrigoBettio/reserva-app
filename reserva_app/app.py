from flask import Flask, render_template, request
import os
import csv

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

def add_banco(nome, email, password):
    """Adiciona os dados do usuário no arquivo CSV conferindo se o cabeçalho está escrito."""
    with open("usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        if arquivo_usuarios.readline() == "":
            with open("usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
                escritor_csv = csv.writer(arquivo_usuarios)
                escritor_csv.writerow(["nome", "email", "password"])  

    with open("usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
        escritor_csv = csv.writer(arquivo_usuarios)
        escritor_csv.writerow([nome, email, password])
        
def obter_dados():
    """Obtem nome, email e password de um formulário e retorna os mesmos"""
    nome = request.form['nome'] 
    email = request.form['email']
    password = request.form['password']

    return nome, email, password

def obter_dados_login():
    """Obtem email e password de um formulário e retorna os mesmos"""
    email = request.form['email']
    password = request.form['password']

    return email, password

def verificacao_usuario(email, password):
    """Verifica se os dados de email e password existem no banco de dados (No caso, arquivo csv)"""
    with open("usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        leitor_csv = csv.DictReader(arquivo_usuarios)
        for linha in leitor_csv:
            if linha["email"] == email and linha["password"] == password:
                return True
        return False

@app.route("/", methods = ['POST'])
def login():
    email, password = obter_dados_login()
    if verificacao_usuario(email, password) == True:
        return render_template("reservas.html")
    else:
        return render_template("login.html", erro="O email ou senha estão incorretos, tente novamente")


app.run(debug=True)
