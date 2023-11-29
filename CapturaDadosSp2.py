import psutil
import mysql.connector
import time

# Função para autenticar o usuário
def autenticar_usuario(mycursor, email, senha):
    sql_query = "SELECT idUsuario FROM Usuario WHERE Email = %s AND Senha = %s"
    mycursor.execute(sql_query, (email, senha))
    result = mycursor.fetchone()
    return result

# Função para exibir a lista de ATMs disponíveis
def exibir_atms_disponiveis(mycursor):
    mycursor.execute("SELECT idATM, Modelo FROM ATM")
    atms_disponiveis = mycursor.fetchall()
    print("ATMs disponíveis para monitoramento:")
    for atm in atms_disponiveis:
        print(f"ATM ID: {atm[0]}, Modelo: {atm[1]}")

# Conectar ao banco de dados
mydb = mysql.connector.connect(host='localhost', port="3306", user="giba", password="fgandb25", database='secureATM')

if mydb.is_connected():
    print("------------------------------------------------------------")
    print("| Bem-vindo(a) à Secure ATM. Por favor, faça o login.       |")
    print("------------------------------------------------------------")

    while True:
        # Solicitar e verificar e-mail e senha
        email = input("Digite o seu e-mail: ")
        senha = input("Digite a sua senha: ")

        mycursor = mydb.cursor()
        usuario_autenticado = autenticar_usuario(mycursor, email, senha)

        if usuario_autenticado:
            print("\nOlá! Selecione o ATM que você quer monitorar:")
            
            # Exibir ATMs disponíveis
            exibir_atms_disponiveis(mycursor)
            
            # Permitir ao usuário escolher um ATM para monitoramento
            atm_escolhido = input("Escolha o ATM pelo ID para monitorar: ")
            
            print("\nMonitoramento iniciado.")

            while True:
                # Coleta de dados da máquina
                cpu_percent = psutil.cpu_percent()
                ram_percent = psutil.virtual_memory().percent
                disk_percent = psutil.disk_usage('/').percent

                # Lista de variáveis que carregam os dados colhidos que serão inseridos nessa iteração EM ORDEM
                dados_insert_cpu = [cpu_percent]
                dados_insert_ram = [ram_percent]
                dados_insert_disk = [disk_percent]

                # Retorna a versão atual do SQL / infos de sistema do banco
                db_info = mydb.get_server_info()

                # Abre cursor permitindo inserção
                mycursor = mydb.cursor()

                # Inserção dados CPU
                sql_query_cpu = "INSERT INTO leitura (DataRegistro, Valor, Componente_ID, ATMComp_ID, APIID) VALUES (current_timestamp(), %s, 3, %s, 2)"
                mycursor.execute(sql_query_cpu, (dados_insert_cpu[0], atm_escolhido))
                mydb.commit()

                # Inserção dados RAM
                sql_query_ram = "INSERT INTO leitura (DataRegistro, Valor, Componente_ID, ATMComp_ID, APIID) VALUES (current_timestamp(), %s, 1, %s, 2)"
                mycursor.execute(sql_query_ram, (dados_insert_ram[0], atm_escolhido))
                mydb.commit()

                # Inserção dados DISCO
                sql_query_disk = "INSERT INTO leitura (DataRegistro, Valor, Componente_ID, ATMComp_ID, APIID) VALUES (current_timestamp(), %s, 2, %s, 2)"
                mycursor.execute(sql_query_disk, (dados_insert_disk[0], atm_escolhido))
                mydb.commit()

                print(f"CPU: {cpu_percent}% | RAM: {ram_percent}% | Disco: {disk_percent}%")

                # Aguarda 10 segundos antes da próxima coleta e inserção
                time.sleep(10)

        else:
            print("E-mail ou senha incorretos. Tente novamente.")

        # Fechar cursor caso aberto para evitar erros de inserção
        if mydb.is_connected():
            mycursor.close()

# Fechar a conexão com o banco de dados
mydb.close()
