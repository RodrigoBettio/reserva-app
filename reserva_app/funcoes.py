from flask import request
import csv
from datetime import datetime

def obter_dados():
    """Obtem nome, sobrenome, email e password de um formulário e retorna os mesmos"""
    if "nome" in request.form:
        nome = request.form['nome'] 
        nome = nome.title().strip()
    else: 
        nome = None

    if "sobrenome" in request.form:
        sobrenome = request.form['sobrenome'] 
        sobrenome = sobrenome.title().strip()
    else: 
        sobrenome = None

    if "email" in request.form:
        email = request.form['email']
        email = email.strip().lower()
    else: 
        email = None  
    
    if "password" in request.form:
        password = request.form['password']
    else: 
        password = None
    return nome, sobrenome, email, password

def obter_dados_sala():
    """Obtem os dados de um formulário com infos de uma reserva de sala e retorna os mesmos"""

    sala = request.form.get("sala")
    infos_inicio = request.form.get("inicio")
    infos_fim = request.form.get("fim")

    data_inicio, hora_inicio = conversao(infos_inicio) if infos_inicio else (None, None)
    data_final, hora_final = conversao(infos_fim) if infos_fim else (None, None)

    return sala, data_inicio, hora_inicio, data_final, hora_final

def conversao(infos):
        """Converte uma string com data e hora usando a biblioteca datetime, com modelo de dia, mês e ano e hora e minuto"""
        infos_convertida = datetime.fromisoformat(infos) #Converte a string infos em um objeto da biblioteca datetime

        data = infos_convertida.strftime("%d-%m-%Y") #Modelo dia, mes, ano
        hora = infos_convertida.strftime("%H:%M") #Modelo hora e minuto

        return data, hora

 # if "sala" in request.form:
    #     sala = request.form["sala"]
    # else:
    #     sala = None

    # if "inicio" in request.form:
    #     infos_inicio = request.form["inicio"]
    #     data_inicio, hora_inicio = conversao(infos_inicio)

    # else:
    #     infos_inicio = None

    # if "fim" in request.form:
    #     infos_fim = request.form["fim"]
    #     data_final, hora_final = conversao(infos_fim) 
 
    # else:
    #     infos_fim = None
 
    # return sala, data_inicio, hora_inicio, data_final, hora_final

# def conversao(data_hora):
#     """Converte a string de data e hora em data e hora separadas"""
#     data, hora = data_hora.split("T")
#     return data, hora
 
def add_banco_reservas(nome,sobrenome,sala,data_inicio,hora_inicio,data_final,hora_final):
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
   
def add_banco_salas(tipo,capacidade,descricao):
    """Adiciona a salas no banco de dados (Arquivo.csv), recebendo um tipo, capacidade e descricao da sala"""

    with open("csv/salas.csv", "r") as arquivo_salas:
        if arquivo_salas.readline() == "":
            with open("salas.csv", "a", newline="") as arquivo_salas:
                escritor_csv = csv.writer(arquivo_salas)
                escritor_csv.writerow(["tipo", "capacidade","descricao"])  

    with open("csv/salas.csv", "a", newline="") as arquivo_salas:
        escritor_csv = csv.writer(arquivo_salas)
        escritor_csv.writerow([tipo, capacidade, descricao])

def verificacao_usuario(email, password):
    """Verifica se os dados de email e password existem no banco de dados (No caso, arquivo csv)"""
    with open("csv/usuarios_cadastrados.csv", "r") as arquivo_usuarios:
        leitor_csv = csv.DictReader(arquivo_usuarios)
        for linha in leitor_csv:
            if linha["email"] == email and linha["password"] == password:
                return True, linha ["nome"], linha["sobrenome"]
        return False, None, None
    

def formulario_cadastro_salas():
    """Pega tipo, capacidade e descricao de um formulário"""
    if "tipo" in request.form:
        tipo = request.form ["tipo"]
    else:
        tipo = None

    if "capacidade" in request.form:    
        capacidade = request.form ["capacidade"]
    else: 
        capacidade = None
    
    if "descricao" in request.form:
        descricao = request.form ["descricao"]
    else:
        descricao = None

    return tipo, capacidade, descricao

    
def procurar_salas():
    """Procura no arquivo usuarios_reserva, se existe alguma reserva no nome do usuário"""
    salas = [] 
    with open("csv/salas.csv", "r") as arquivo_salas:
        leitor_csv = csv.DictReader(arquivo_salas)
        for linha in leitor_csv:
            # if linha["tipo"] == tipo and linha["capacidade"] == capacidade and linha["descricao"] == descricao:
                salas.append(list(linha.values())) 

    if salas: 
        return salas
    else:
        return None
    
def procurar_reserva(nome, sobrenome):
    """Procura no arquivo usuarios_reserva, se existe alguma reserva no nome do usuário"""
    reservas_encontradas = [] 
    with open("csv/usuarios_reserva.csv", "r") as arquivo_reserva:
        leitor_csv = csv.DictReader(arquivo_reserva)
        for linha in leitor_csv:
            if linha["nome"] == nome and linha["sobrenome"] == sobrenome:
                reservas_encontradas.append(list(linha.values())) 

    if reservas_encontradas: 
        return True, reservas_encontradas
    else:
        return False, None

