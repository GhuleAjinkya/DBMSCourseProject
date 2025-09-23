import mysql.connector

def simulateTransfer():
    db = mysql.connector.connect(user='root',password='Ajinkya!1')
    cursor = db.cursor()
    cursor.execute("use bank;")
    try:
        cursor.callproc("TransferAmount",[1,2,14000,1])
        # call TransferAmount(3,4,100.00,0);
        # call TransferAmount(1,2,14000.00,0);
    except Exception as e:
        print("error: ", e)
     
    
        
        