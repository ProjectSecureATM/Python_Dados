import psutil
import time 
import platform
import mysql.connector

'''
def mysql_connection(host, user, passwd, database=None):
    
    return connection

#connection = mysql_connection("localhost","root","5505", "python_dados")
'''

i = 0
while i<50:
    CPU1 = psutil.cpu_percent()
    CPU2 = 1.1 * CPU1
    CPU3 = CPU2 / 0.95
    
    MEMO1 = psutil.virtual_memory().percent
    MEMO2 = 1.15 * MEMO1
    MEMO3 = MEMO2 / 1.05 
    
    meu_so = platform.system()
    if(meu_so == "Linux"):
        DISCO1 = psutil.disk_usage('/').percent
    elif(meu_so == "Windows"):
        DISCO1 = psutil.disk_usage('C:\\').percent   
        
    DISCO2 = 0.95 * DISCO1
    DISCO3 = 3 * DISCO2

    print("SO que eu uso : ",meu_so)
    
    print("\nCPU1:",CPU1)
    print("\nCPU2:",CPU2)
    print("\nCPU2:",CPU3)

    mydb = mysql.connector.connect(host = 'localhost',user = 'root',passwd = '5505',database = 'python_dados')
    cursor = mydb.cursor()

    query = 'INSERT INTO CPUS(CPU1, CPU2, CPU3) VALUES(%s, %s,%s)'
    param = [CPU1, CPU2, CPU3]
    cursor.execute(query, param)
    mydb.commit()

    print("\nMEMO1:",MEMO1)
    print("\nMEMO2:",MEMO2)
    print("\nMEMO3:",MEMO3)

    query = 'INSERT INTO MEMO(MEMO1, MEMO2, MEMO3) VALUES(%s, %s,%s)'
    param2 = [MEMO1, MEMO2, MEMO3]
    cursor.execute(query, param2)
    mydb.commit()

    print("\nDISCO1:",DISCO1)
    print("\nDISCO2:",DISCO2)
    print("\nDISCO3:",DISCO3)

    query = 'INSERT INTO DISCO(DISCO1, DISCO2, DISCO3) VALUES(%s, %s,%s)'
    param3 = [DISCO1, DISCO2, DISCO3]
    cursor.execute(query, param2)
    mydb.commit()
    print("---------------------------------")
    i += 1
    time.sleep(5)
