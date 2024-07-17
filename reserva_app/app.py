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

@app.route("/login")
def login():
    return render_template ("login.html")

@app.route("/reservar_sala")
def reservar_sala():
    return render_template("reservar_sala.html")

@app.route("/reservas")
def reservas():
    return render_template("reservas.html")

@app.route("/reserva/detalhe_reserva")
def detalhe_reserva():
    return render_template("/reserva/detalhe_reserva.html")
app.run(debug=True)

 