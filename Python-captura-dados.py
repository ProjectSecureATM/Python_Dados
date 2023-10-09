import math
import psutil
import time
import platform
import mysql.connector
import ping3
import socket
from cred import usr, pswd

 
def converter_segundos_para_horas_minutos_segundos(segundos):
    horas = segundos // 3600  # 1 hora = 3600 segundos
    segundos_restantes = segundos % 3600
    minutos = segundos_restantes // 60
    segundos_final = math.ceil(segundos_restantes % 60)

    return horas, minutos, segundos_final

def bytes_para_gb(bytes_value):
    return bytes_value / (1024 ** 3)

mydb = mysql.connector.connect(host = 'localhost',user = 'root',passwd = 'ph993387998',database = 'SecureATM')
cursor = mydb.cursor()
fk_atm = 1

while(True):

    print("\n-----------------------------------------")
    componente = input("Qual plano você deseja analisar? \n1: Standard (CPU, Memória, Disco \n-----------------------------------------\n")

    print("\n-----------------------------------------")

    while(True):
        fk_atm = 1
        tentativas = 0
        resposta = input("Quer ver os dados? (s/n): ")
        
        if resposta == "s":
            while tentativas < 3:
                try:
                    mydb = mysql.connector.connect(host = 'localhost',user = usr, password = pswd, database = 'SecureATM')
                    if mydb.is_connected():
                        cursor = mydb.cursor()
                        print("Banco conectado")
                except mysql.connector.Error as e:
                    print("Erro ao conectar com o MySQL", e)
                    

                print("\nComponente = CPU\n")
                print("-----------------------------------------")
                print("\nSituação geral: ")
                print("-----------------------------------------")
                    
                ps = psutil.cpu_times()
                    
                
                porcentagem_utilizacao = psutil.cpu_percent(percpu = False)
                numeroCpu = psutil.cpu_count()  
                frequenciaCpuMhz = psutil.cpu_freq(percpu=False)
                velocidade = "{:.2f}".format(frequenciaCpuMhz.current / 1000)
                processos = len(psutil.pids())


                print("\nUtilização:")
                print("Porcentagem sendo utilizada da CPU: ", porcentagem_utilizacao, "%")
                print()

                print("Outros:")
                print("\nFrequencia das CPUs no sistema:", velocidade, "GHz")
                print()

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [porcentagem_utilizacao, fk_atm, 1]
                cursor.execute(query, param)

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [velocidade, fk_atm, 2]
                cursor.execute(query, param)

                

                print("\n-----------------------------------------")
                print("\nComponente = Disco\n")
                print("-----------------------------------------")

                print("\nSituação geral: ")
                print("-----------------------------------------")
                particoes = psutil.disk_partitions()
                disco = psutil.disk_usage
                        

                porcentagem_uso = disco.percent
                capacidade_total = "{:.2f}".format(bytes_para_gb(disco.total))
                capacidade_usada = "{:.2f}".format(bytes_para_gb(disco.used))
                capacidade_livre = "{:.2f}".format(bytes_para_gb(disco.free))

                print("Uso de Disco:")
                print(f"Nome do Disco:", nome_disco)
                print(f"Total:", capacidade_total, "bytes")
                print(f"Usado:", capacidade_usada, "bytes")
                print(f"Livre:", capacidade_livre, "bytes")
                print(f"Percentual de Uso:", porcentagem_uso, "%")
                print()

               

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [porcentagem_uso, fk_atm, 11]
                cursor.execute(query, param)
                
                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [capacidade_total, fk_atm, 12]
                cursor.execute(query, param)

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [capacidade_usada, fk_atm, 13]
                cursor.execute(query, param)


                print("\n-----------------------------------------")
                print("\nComponente selecionado = Memória\n")
                print("-----------------------------------------")

                memoria_virtual = psutil.virtual_memory()
                total = "{:.2f}".format(bytes_para_gb(memoria_virtual.total))
                livre = "{:.2f}".format(bytes_para_gb(memoria_virtual.available))
                usado = "{:.2f}".format(bytes_para_gb(memoria_virtual.used))
                porcentagem_uso = memoria_virtual.percent
                print("Memória Virtual:")
                print("Total:", total,"GB")
                print("Disponível:", livre,"GB")
                print("Usado:", usado,"GB")
                print("Percentual de Uso:", porcentagem_uso,"%")
                print()

                swap = psutil.swap_memory()
                print("Swap:")
                print("Total: {:.2f} GB".format(bytes_para_gb(swap.total)))
                print("Usado: {:.2f} GB".format(bytes_para_gb(swap.used)))
                print("Livre: {:.2f} GB".format(bytes_para_gb(swap.free)))
                print("Percentual de Uso:", swap.percent,"%")
                print()


                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [total, fk_atm, 6]
                cursor.execute(query, param)

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [usado, fk_atm, 7]
                cursor.execute(query, param)

                query = 'INSERT INTO leitura(valor, fk_atm, fk_componente) VALUES(%s, %s,%s)'
                param = [porcentagem_uso, fk_atm, 8]
                cursor.execute(query, param)

                
                tentativas += 1

        else:
            break
            
            
            mydb.commit()
            time.sleep(20)

                
            if(mydb.is_connected()):
                mydb.close()




