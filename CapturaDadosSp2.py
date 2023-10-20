import psutil
import time
import mysql.connector

            # preecher campos abaixo com as configs específicas do bd 
mydb = mysql.connector.connect(host = 'localhost',port = "3306",user = "root", password = "root", database = 'secureatm')

    
while(True):
            #FK do ATM associado a leitura em banco
        fk_atm = 1
        tentativas = 0
        print("-----------------------------------------")
        resposta = input("|        Quer ver os dados? (s/n):         |\n----------------------------------------- \n")
        if resposta == "s":
            while tentativas < 3:
                cpuPercent= psutil.cpu_percent()
                ramPercent= psutil.virtual_memory().percent
                diskPercent= psutil.disk_usage('/').percent
                if mydb.is_connected():
                    print("-----------------------------------------")
                    print("|               Banco conectado               |\n----------------------------------------- ")
                    print("-------------------------------------------")
                    print("| Porcentagem de uso de CPU: {:.2f}%".format(cpuPercent)," |\n------------------------------------------- ")
                    print("---------------------------------------------")
                    print("| Porcentagem de uso de RAM: {:.2f}%".format(ramPercent)," |\n--------------------------------------------- ")
                    print("-------------------------------------------------------------")
                    print("| Porcentagem de Memória em disco ocupada: {:.2f}".format(diskPercent)," |\n------------------------------------------------------------- ")
               #lista de variaveis que carregam os dados colhidos que serão inseridos nessa iteração EM ORDEM
                    dadosInsertCpu = [cpuPercent]
                    dadosInsertRam = [ramPercent]
                    dadosInsertDisk = [diskPercent]
               #Restorna a versão atual do SQL / infos de sistema do banco            
                    db_info = mydb.get_server_info()
               #Abre cursor permitindo inserção            
                    mycursor = mydb.cursor()
               #inserção stringificada (id=null, time, %s= valor, 1=componenteID, 1=ATM_ID)
                    sql_query = "INSERT INTO leitura VALUES (null, current_timestamp(), %s, 1, 1)"
                    if not sql_query:
                            print("erro ao inserir no banco")
               #cursor executa a query e é feito o commit da transação
                    mycursor.execute(sql_query, dadosInsertCpu)
                    mydb.commit()
               #inserção stringificada (id=null, time, %s= valor, 2=componenteID, 1=ATM_ID)
                    sql_query = "INSERT INTO leitura VALUES (null, current_timestamp(), %s, 2, 1)"
               #cursor executa a query e é feito o commit da transação
                    mycursor.execute(sql_query, dadosInsertRam)
                    mydb.commit()
                    #inserção stringificada (id=null, time, %s= valor, 3=componenteID, 1=ATM_ID)
                    sql_query = "INSERT INTO leitura VALUES (null, current_timestamp(), %s, 3, 1)"
               #cursor executa a query e é feito o commit da transação
                    mycursor.execute(sql_query, dadosInsertDisk)
                    mydb.commit()
               #avanço do while de 3 vezes            
                    tentativas+=1
               #Fechar cursor caso aberto para evitar erros de inserção
                    if(mydb.is_connected()):
                        mycursor.close()
                        mydb.close()
        else: break
    
