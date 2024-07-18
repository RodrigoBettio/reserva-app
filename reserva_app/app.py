from flask import Flask, render_template, request
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

def add_banco(nome, email, password):
    """Adiciona os dados do usuário no banco de dados (No caso, arquivo csv)"""
    usuario = {"nome": nome, "email": email, "password": password}

    with open("usuarios_cadastrados.csv", "a") as arquivo_usuarios:
        dados = f"\n{usuario}"
        arquivo_usuarios.write(dados)
    
def obter_dados():
    """Obtem nome, email e password de um formulário e retorna os mesmos"""
    nome = request.form['nome'] 
    email = request.form['email']
    password = request.form['password']

    return nome, email, password
app.run(debug=True)
