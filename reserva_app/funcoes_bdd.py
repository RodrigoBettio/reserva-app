from reserva_app.conexao_bdd import conexao_abrir, conexao_fechar

def cliente_listar(conexao):
    cursor = conexao.cursor()
    sql = "SELECT * FROM usuarios"

    cursor = conexao.cursor(dictionary = True)
    cursor.execute(sql)

    for (registro) in cursor:
        print(registro["nome"] + " - "+ registro["email"])

    cursor.close()

def cliente_inserir(conexao, codigo, nome, sobrenome, email, senha):
    cursor = conexao.cursor()
    sql = "INSERT INTO usuarios (id_usuarios, nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql,(codigo, nome, sobrenome , email, senha))
    conexao.commit()
    cursor.close()

def main():
    conexao = conexao_abrir("localhost", "estudante1", "123", "reserva_app")

    cliente_inserir(conexao, 2,"Rodrigo","Bettio","rodrigo@gmail.com", "123")
    cliente_listar(conexao)

    conexao_fechar(conexao)

if __name__ == "__main__":
	main()

