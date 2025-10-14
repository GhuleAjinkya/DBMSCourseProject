import time
import mysql.connector
import logging
import threading

logger = logging.getLogger(__name__)

class ACIDDemo:
    
    def __init__(self):
        self.db_config = {'user': 'limited', 'password': '1234', 'database': 'bank'}

    def get_connection(self):
        return mysql.connector.connect(**self.db_config) 
    
    def demo_isolation_deadlock(self):
        
        results = {'t1': None, 't2': None}
        
        def transaction1():
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                print("T1: Starting transfer 1→2 with delay...")
                cursor.callproc("TransferAmount", [1, 2, 500, 1]) 
                conn.commit()
                results['t1'] = 'SUCCESS'
            except Exception as e:
                results['t1'] = f'FAILED: {str(e)}'
            finally:
                cursor.close()
                conn.close()
        
        def transaction2():
            time.sleep(0.5)  # Start slightly after T1
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                print("T2: Starting transfer 2→1 with delay...")
                cursor.callproc("TransferAmount", [2, 1, 300, 1])  # pause=1
                conn.commit()
                results['t2'] = 'SUCCESS'
            except Exception as e:
                results['t2'] = f'FAILED: {str(e)}'
            finally:
                cursor.close()
                conn.close()
        
        t1 = threading.Thread(target=transaction1, name="Transfer-1-to-2")
        t2 = threading.Thread(target=transaction2, name="Transfer-2-to-1")
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        
        time.sleep(1)
        logger.info(f"T1 Result: {results['t1']}, T2 Result: {results['t2']}")

    def simulateTransfer(self, acc1, acc2, amount, delay):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("select sum(balance) from account;")
            total_before = cursor.fetchone()[0]
            cursor.callproc("TransferAmount",[acc1,acc2,amount,int(delay)])
        except mysql.connector.Error as err:
            logger.error(err.msg)
        cursor.execute("select sum(balance) from account;")
        total_after = cursor.fetchone()[0]
        logger.info(f"Total before transaction: {total_before}, Total after: {total_after}")
        
    def atomicityDemo(self):
        # add user input validation
        Acc1 = int(input("Enter creditor account ID: "))
        Acc2 = int(input("Enter debtor account ID: "))
        amount = int(input("Enter amount to transfer: "))
        delayChar = input("Add delay? (Y/N) : ")
        if (delayChar == 'Y' or delayChar == 'y'):
            addDelay = True
        else: 
            addDelay = False
        self.simulateTransfer(Acc1, Acc2, amount, addDelay)
        
    def runMenu(self):
        while True:
            print("ACID PROPERTIES DEMONSTRATION")
            print("1. Isolation Demo using deadlocks")
            print("2. Atomicity Demo")
            choice = input("\nEnter your choice: ").strip()
            if choice == '1':
                self.demo_isolation_deadlock()
            elif choice == '2':
                self.atomicityDemo()
            elif choice == '0':
                break
            else:
                print("\nInvalid choice")
            
            input("\nPress Enter to continue...")
