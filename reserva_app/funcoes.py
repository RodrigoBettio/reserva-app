from flask import request
import csv, os, mysql.connector
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

def add_banco_reservas(conexao, nome, sobrenome, sala, data_inicio, hora_inicio, data_final, hora_final):
    """Adiciona os dados da reserva no banco de dados MySQL"""
    cursor = conexao.cursor()
    sql = """INSERT INTO reservas (nome, sobrenome, sala, data_inicio, hora_inicio, data_final, hora_final) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (nome, sobrenome, sala, data_inicio, hora_inicio, data_final, hora_final))
    conexao.commit()
    cursor.close()



def add_banco_usuarios(conexao, nome, sobrenome, email, password):
    """Adiciona os dados do usuário no banco de dados MySQL"""
    cursor = conexao.cursor()
    sql = "INSERT INTO usuarios (nome, sobrenome, email, password) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (nome, sobrenome, email, password))
    conexao.commit()
    cursor.close()

   
def add_banco_salas(conexao, tipo, capacidade, descricao):
    """Adiciona uma sala no banco de dados MySQL"""
    cursor = conexao.cursor()
    sql = "INSERT INTO salas (tipo, capacidade, descricao) VALUES (%s, %s, %s)"
    cursor.execute(sql, (tipo, capacidade, descricao))
    conexao.commit()
    cursor.close()


def verificacao_usuario(conexao, email, password):
    """Verifica se o usuário está no banco de dados MySQL"""
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
    cursor.execute(sql, (email, password))
    usuario = cursor.fetchone() #Retorna a primeira linha encontrada
    cursor.close()

    if usuario:
        return True, usuario['nome'], usuario['sobrenome']
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

    
def procurar_salas(conexao):
    """Procura no banco de dados MySQL todas as salas cadastradas"""
    salas = []
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM salas"
    cursor.execute(sql)
    resultados = cursor.fetchall() #Retorna todas as linhas da consulta como uma lista de tuplas.
    cursor.close()

    if resultados:
        for sala in resultados:
            salas.append(list(sala.values())) 
        return salas
    else:
        return None
    
def pegar_tipo_sala(conexao):
    """Obtém todos os tipos de salas únicos do banco de dados MySQL"""
    tipo_salas = set()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT DISTINCT tipo FROM salas"
    cursor.execute(sql)
    resultados = cursor.fetchall() #Retorna todas as linhas da consulta como uma lista de tuplas.
    cursor.close()

    if resultados:
        for tipo in resultados:
            tipo_salas.add(tipo['tipo'])  
        return list(tipo_salas)
    else:
        return None


    
def procurar_reserva(conexao, nome, sobrenome):
    """Procura no banco de dados MySQL se existe alguma reserva no nome do usuário"""
    reservas_encontradas = []
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM reservas WHERE nome = %s AND sobrenome = %s"
    cursor.execute(sql, (nome, sobrenome))
    resultados = cursor.fetchall() #Retorna todas as linhas da consulta como uma lista de tuplas.
    cursor.close()

    if resultados:
        for reserva in resultados:
            reservas_encontradas.append(list(reserva.values()))
        return True, reservas_encontradas
    else:
        return False, None