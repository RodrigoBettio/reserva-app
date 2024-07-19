from flask import request
import csv

def add_banco(nome, sobrenome, email, password):
    """Adiciona os dados do usuário no arquivo CSV conferindo se o cabeçalho está escrito."""
    with open("csv/usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        if arquivo_usuarios.readline() == "":
            with open("usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
                escritor_csv = csv.writer(arquivo_usuarios)
                escritor_csv.writerow(["nome","sobrenome", "email", "password"])  

    with open("csv/usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
        escritor_csv = csv.writer(arquivo_usuarios)
        escritor_csv.writerow([nome, sobrenome, email, password])

def obter_dados():
    """Obtem nome, sobrenome, email e password de um formulário e retorna os mesmos"""
    if "nome" in request.form:
        nome = request.form['nome'] 
    else: 
        nome = None

    if "sobrenome" in request.form:
        sobrenome = request.form['sobrenome'] 
    else: 
        sobrenome = None

    if "email" in request.form:
        email = request.form['email']
    else: 
        email = None  
    
    if "password" in request.form:
        password = request.form['password']
    else: 
        password = None
    return nome, sobrenome, email, password

def verificacao_usuario(email, password):
    """Verifica se os dados de email e password existem no banco de dados (No caso, arquivo csv)"""
    with open("csv/usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        leitor_csv = csv.DictReader(arquivo_usuarios)
        for linha in leitor_csv:
            if linha["email"] == email and linha["password"] == password:
                return True, linha ["nome"]
        return False, None
