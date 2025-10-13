import time
import mysql.connector
import logging
import threading
from tabulate import tabulate

logger = logging.getLogger(__name__)
db = mysql.connector.connect(user='limited',password='1234')
cursor = db.cursor()
cursor.execute("use bank;")

def simulateTransfer(acc1, acc2, amount, delay):
    try:
        cursor.execute("select sum(balance) from account;")
        total_before = cursor.fetchone()[0]
        cursor.callproc("TransferAmount",[acc1,acc2,amount,int(delay)])
        # call TransferAmount(3,4,100.00,0);
        # call TransferAmount(1,2,14000.00,0);
    except mysql.connector.Error as err:
        logger.error(err.msg)
    cursor.execute("select sum(balance) from account;")
    total_after = cursor.fetchone()[0]
    logger.info(f"Total before transaction: {total_before}, Total after: {total_after}")
    
def atomicityDemo():
    # add user input validation
    Acc1 = int(input("Enter creditor account ID: "))
    Acc2 = int(input("Enter debtor account ID: "))
    amount = int(input("Enter amount to transfer: "))
    delayChar = input("Add delay? (Y/N) : ")
    if (delayChar == 'Y' or delayChar == 'y'):
        addDelay = True
    else: 
        addDelay = False
    simulateTransfer(Acc1, Acc2, amount, addDelay)

class ACIDDemo:
    
    def __init__(self):
        self.db_config = {'user': 'root', 'password': 'Ajinkya!1', 'database': 'bank'}

    def get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def display_accounts(self):
        """Display current account balances"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.AccountID, c.Name, at.TypeName, a.Balance 
            FROM Account a
            JOIN Customer c ON a.CustomerID = c.CustomerID
            JOIN AccountType at ON a.AccountType = at.TypeID
            ORDER BY a.AccountID
        """)
        results = cursor.fetchall()
        print("\n" + "="*60)
        print(tabulate(results, headers=['AccountID', 'Customer', 'Type', 'Balance'], tablefmt='grid'))
        print("="*60 + "\n")
        cursor.close()
        conn.close()

    def display_transactions(self, limit=10):
        """Display recent transactions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT TransactionID, TransactionType, SenderID, ReceiverID, 
                   Status, InitiatedAt, CompletedAt
            FROM Transaction 
            ORDER BY TransactionID DESC 
            LIMIT {limit}
        """)
        results = cursor.fetchall()
        print("\n" + "="*80)
        print(tabulate(results, headers=['TxnID', 'Type', 'Sender', 'Receiver', 'Status', 'Initiated', 'Completed'], tablefmt='grid'))
        print("="*80 + "\n")
        cursor.close()
        conn.close() 
    
    def demo_isolation_deadlock(self):
        """Demonstrate isolation - deadlock scenario"""
        print("\n🟡 ISOLATION DEMO 2: Deadlock Detection and Resolution")
        print("-" * 60)
        
        self.display_accounts()
        print("Starting two concurrent transfers in opposite directions...")
        print("T1: Account 1 → Account 2")
        print("T2: Account 2 → Account 1")
        
        results = {'t1': None, 't2': None}
        
        def transaction1():
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                print("T1: Starting transfer 1→2 with delay...")
                cursor.callproc("TransferAmount", [1, 2, 500, 1])  # pause=1
                conn.commit()
                results['t1'] = 'SUCCESS'
                print("T1: ✅ Completed successfully")
            except Exception as e:
                results['t1'] = f'FAILED: {str(e)}'
                print(f"T1: ❌ Failed - {e}")
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
                print("T2: ✅ Completed successfully")
            except Exception as e:
                results['t2'] = f'FAILED: {str(e)}'
                print(f"T2: ❌ Failed - {e}")
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
        print("\n" + "="*60)
        print("RESULTS:")
        print(f"Transaction 1 (1→2): {results['t1']}")
        print(f"Transaction 2 (2→1): {results['t2']}")
        print("\n➡️ ISOLATION: MySQL detected potential deadlock and may abort one transaction")
        print("="*60)
        
        self.display_accounts()
        self.display_transactions(5)

    def echoQuery():
        query = input("Enter query to run: ")
        if (input("Run query as admin? (y/n): ") == 'y'):
            runAsAdmin = True
        else:
            runAsAdmin = False
        
        if runAsAdmin:
            db = mysql.connector.connect(user='Ajinkya',password='Ajinkya!1')
            admin = db.cursor()
            admin.execute("use bank;")
            admin.execute(query)
            output = admin.fetchall()
        else:
            cursor.execute(query)
            output = cursor.fetchall()

        # TODO helper function to print this
        
    def runMenu(self):
        while True:
            print("ACID PROPERTIES DEMONSTRATION")
            print("\n📘 ATOMICITY (All or Nothing)")
            print("  1. Demo: Successful Transfer (All operations complete)")
            print("  2. Demo: Failed Transfer (Nothing changes)")
            
            print("\n📗 CONSISTENCY (Rules are maintained)")
            print("  3. Demo: Money conservation (Total balance unchanged)")
            
            print("\n📙 ISOLATION (Transactions don't interfere)")
            print("  4. Demo: Dirty Read Prevention")
            print("  5. Demo: Deadlock Detection")
            
            print("\n📕 DURABILITY (Committed data persists)")
            print("  6. Demo: Persistence after 'restart'")
            
            print("\n  UTILITIES")
            print("  7. View Current Accounts")
            print("  8. View Recent Transactions")
            print("  9. Echo Query")
            print("  0. Exit")
            
            choice = input("\nEnter your choice (0-9): ").strip()
            # TODO make tis switch case
            if choice == '1':
                self.demo_atomicity_success()
            elif choice == '2':
                self.demo_atomicity_failure()
            elif choice == '3':
                self.demo_consistency()
            elif choice == '4':
                self.demo_isolation_dirty_read()
            elif choice == '5':
                self.demo_isolation_deadlock()
            elif choice == '6':
                self.demo_durability()
            elif choice == '7':
                self.display_accounts()
            elif choice == '8':
                self.display_transactions(10)
            elif choice == '9':
                self.echoQuery()
            elif choice == '0':
                break
            else:
                print("\nInvalid choice")
            
            input("\nPress Enter to continue...")
