from flask import Flask, render_template, request, session
from reserva_app.funcoes import add_banco_usuarios, add_banco_reservas, obter_dados,obter_dados_sala, procurar_salas, verificacao_usuario, procurar_reserva, formulario_cadastro_salas, add_banco_salas, pegar_tipo_sala
import os, mysql.connector
from reserva_app.conexao_bdd import *

 
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

@app.route("/reservar_sala")
def reservar_sala():
    tipo_salas = pegar_tipo_sala()
    return render_template("reservar_sala.html", tipo_salas = tipo_salas)

@app.route("/reservas")
def reservas():
    nome_usuario = session.get("nome_usuario") 
    return render_template("reservas.html", nome_usuario = nome_usuario)

@app.route("/reserva/detalhe_reserva", methods =["GET"])
def detalhe_reserva():
    return render_template("reserva/detalhe_reserva.html")

#Rota usada para cadastro de usuários
@app.route("/cadastro", methods = ['POST'])
def cadastrar_usuario():
    nome, sobrenome, email, senha = obter_dados()
    if nome == "":
        return render_template("cadastro.html", erro = "Você não tem nome?")
    
    elif sobrenome == "":
        return render_template("cadastro.html", erro = "Seus pais esqueceram do seu sobrenome?", nome = nome)
    
    elif email == "":
        return render_template("cadastro.html", erro = "Esse email não existe", nome = nome, sobrenome = sobrenome)
    
    elif senha == "":
        return render_template("cadastro.html", erro = "Última vez que não coloquei senha em algo não tive um bom resultado...", nome = nome, sobrenome = sobrenome, email = email)
    
    else:
        conexao = conexao_abrir("localhost", "estudante1", "123", "reserva_app")
        add_banco_usuarios(conexao,nome, sobrenome, email, senha)
        conexao.close()
    return render_template("login.html")

#Rota usada para ler infos do login
@app.route("/", methods = ['POST'])
def login():
    _,_,email, senha = obter_dados()
    conexao = conexao_abrir("localhost", "estudante1", "123", "reserva_app")
    if email == "" and senha == "":
        return render_template ("login.html", erro = "Você deve inserir um email e senha")
    elif email == "":
        return render_template ("login.html", erro = "Você deve inserir um email")
    elif senha == "":
        return render_template ("login.html", erro = "Você deve inserir uma senha", email = email)
    else:
        verifica_resultado, nome_usuario, sobrenome_usuario = verificacao_usuario(conexao, email, senha)
        conexao.close()
        if verifica_resultado:
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
        verifica_usuario, reservas =  procurar_reserva(nome, sobrenome)
        if verifica_usuario:
            return render_template("reservas.html", reservas = reservas, nome_usuario = nome_usuario)
        else: 
            return render_template("reservas.html", erro = "Reserva não encontrada. Digite novamente ou faça a reserva no nosso site", reservas = None, nome_usuario = nome_usuario, nome = nome)
    
#Rota usada para reserva de salas
@app.route("/reservar_sala", methods =["GET", "POST"])
def reservas_sala():
    pegar_tipo_sala()
    conexao = conexao_abrir

    if request.method == "POST":
        nome_usuario = session.get("nome_usuario")
        sobrenome_usuario = session.get("sobrenome_usuario")
        sala, data_inicio, hora_inicio, data_final, hora_final = obter_dados_sala()


        if sala == None or data_inicio == None or hora_inicio == None or  data_final == None or  hora_final == None:    
            erro = "Preencha todos os campos!"
            return render_template("reservar_sala.html", erro=erro)
        else:
            add_banco_reservas(conexao,nome_usuario, sobrenome_usuario, sala, data_inicio, hora_inicio, data_final, hora_final)
            conexao.close()
            return render_template("reserva/detalhe_reserva.html", nome_usuario=nome_usuario, sobrenome_usuario=sobrenome_usuario, sala=sala)

@app.route("/minha_reserva")
def minha_reserva():
    nome_usuario = session.get("nome_usuario") 
    
    sobrenome_usuario = session.get("sobrenome_usuario") 

    verifica_usuario, reservas =  procurar_reserva(nome_usuario, sobrenome_usuario)

    if verifica_usuario == False:
        return render_template("minha_reserva.html", erro = "Não acredito que você ainda não possui reservas no nosso site :( ", reservas = None, nome_usuario = nome_usuario)
    elif verifica_usuario == True:
        return render_template("minha_reserva.html", reservas = reservas, nome_usuario = nome_usuario) 

@app.route("/cadastrar_sala", methods = ["GET","POST"])
def cadastro_sala():
    conexao = conexao_abrir()
    tipo, capacidade, descricao = formulario_cadastro_salas()

    if tipo == "Selecione um tipo..." or capacidade == "":
        erro = "Preencha o tipo e a capacidade da sala para prosseguir com o cadastro!"
        return render_template("cadastrar_sala.html", erro=erro)
    else:
        add_banco_salas (conexao,tipo,capacidade,descricao)
        salas = procurar_salas()

    conexao.close()
    return render_template("listar_salas.html", salas = salas)

@app.route("/listar_salas")
def listar_salas():
    conexao = conexao_abrir()  

    salas = procurar_salas(conexao)

    conexao.close()
    if salas == None:
        return render_template("listar_salas.html", erro = "Você ainda não possui nenhuma sala cadastrada!")
    else: 
        return render_template("listar_salas.html", salas = salas)
    
app.secret_key = 'teste_sessao' 
app.run(debug=True)


