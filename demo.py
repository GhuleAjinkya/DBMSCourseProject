import mysql.connector

def simulateTransfer():
    db = mysql.connector.connect(user='root',password='Ajinkya!1')
    cursor = db.cursor()
    cursor.execute("use bank;")
    try:
        cursor.callproc("TransferAmount",[1,2,14000,1])
    except Exception as e:
        print("error: ", e)
     
    
        
        