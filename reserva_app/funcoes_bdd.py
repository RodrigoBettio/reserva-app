from reserva_app.conexao_bdd import conexao_abrir, conexao_fechar

def cliente_listar(conexao):
    cursor = conexao.cursor()
    sql = "SELECT * FROM usuario"

    cursor = conexao.cursor(dictionary = True)
    cursor.execute(sql)

    for (registro) in cursor:
        print(registro["cli_nome"] + " - "+ registro["cli_fone"])

    cursor.close()

def cliente_inserir(conexao, codigo, nome, fone, email):
    cursor = conexao.cursor()
    sql = "INSERT INTO t_cliente (cli_codigo, cli_nome, cli_fone, cli_email) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql,(codigo, nome, fone, email))
    conexao.commit()
    cursor.close()

def main():
    conexao = conexao_abrir("localhost", "estudante1", "maravilha", "reserva_app")

    cliente_inserir(conexao, 1,"Rodrigo","4274-9390","rodrigo@gmail.com")
    cliente_listar(conexao)

    conexao_fechar(conexao)

if __name__ == "__main__":
	main()

