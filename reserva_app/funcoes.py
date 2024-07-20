from flask import request
import csv
from datetime import datetime

def obter_dados():
    """Obtem nome, sobrenome, email e password de um formulário e retorna os mesmos"""
    if "nome" in request.form:
        nome = request.form['nome'] 
        nome = nome.title()
    else: 
        nome = None

    if "sobrenome" in request.form:
        sobrenome = request.form['sobrenome'] 
        sobrenome = sobrenome.title()
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

def add_banco_salas(nome,sobrenome,sala,data_inicio,hora_inicio,data_final,hora_final):
    """Adiciona os dados da sala no arquivo CSV conferindo se o cabeçalho está escrito."""
    with open("csv/usuarios_reserva.csv", "r") as arquivo_reservas:
        if arquivo_reservas.readline() == "":
            with open("usuarios_reserva.csv", "a", newline="") as arquivo_reservas:
                escritor_csv = csv.writer(arquivo_reservas)
                escritor_csv.writerow(["nome","sobrenome", "sala", "data_inicio", "hora_inicio", "data_final", "hora_final"])  

    with open("csv/usuarios_reserva.csv", "a", newline="") as arquivo_reservas:
        escritor_csv = csv.writer(arquivo_reservas)
        escritor_csv.writerow([nome, sobrenome, sala, data_inicio, hora_inicio, data_final, hora_final])
   

def add_banco_usuarios(nome, sobrenome, email, password):
    """Adiciona os dados do usuário no arquivo CSV conferindo se o cabeçalho está escrito."""
    with open("csv/usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        if arquivo_usuarios.readline() == "":
            with open("usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
                escritor_csv = csv.writer(arquivo_usuarios)
                escritor_csv.writerow(["nome","sobrenome", "email", "password"])  

    with open("csv/usuarios_cadastrados.csv", "a", newline="") as arquivo_usuarios:
        escritor_csv = csv.writer(arquivo_usuarios)
        escritor_csv.writerow([nome, sobrenome, email, password])
   
def verificacao_usuario(email, password):
    """Verifica se os dados de email e password existem no banco de dados (No caso, arquivo csv)"""
    with open("csv/usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        leitor_csv = csv.DictReader(arquivo_usuarios)
        for linha in leitor_csv:
            if linha["email"] == email and linha["password"] == password:
                return True, linha ["nome"], linha["sobrenome"]
        return False, None
    
def procurar_reserva(nome, sobrenome):
    """Procura no arquivo usuarios_reserva, se existe alguma reserva no nome do usuário"""
    with open("csv/usuarios_reserva.csv","r") as arquivo_reserva:
        leitor_csv = csv.DictReader(arquivo_reserva)
        for linha in leitor_csv:
            if linha["nome"] == nome and linha["sobrenome"] == sobrenome:
                return True, list(linha.values())
        return False, None
    

def conversao(infos):
        infos_convertida = datetime.fromisoformat(infos) #Converte a string infos em um objeto da biblioteca datetime

        data_inicio = infos_convertida.strftime("%d-%m-%Y") #Modelo dia, mes, ano
        hora_inicio = infos_convertida.strftime("%H:%M") #Modelo hora e minuto

        return data_inicio, hora_inicio

def obter_dados_sala():
    """Obtem os dados de um formulário com infos de uma reserva de sala e retorna os mesmos"""

    sala = request.form("sala") 
    infos_inicio = request.form("inicio") #Converter em duas strings, data_inicio e hora_inicio
    infos_fim = request.form("fim") #Converter em data_fim e hora_fim

    data_inicio, hora_inicio = conversao(infos_inicio)
    data_final, hora_final = conversao(infos_fim) #Fazer na mesma função, a lógica é a mesma

    return sala, data_inicio, hora_inicio, data_final, hora_final