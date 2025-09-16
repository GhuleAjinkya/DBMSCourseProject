# This file generates schema and populates it with data, if required
'''
for the DBMS CP the other idea we're going to present to sir is transaction management system. 
The idea is to write basically make a system that simulates real transactions and write the error 
management part of it. We log all transactions and make sure they're done with commits using begin. 
If a transaction fails, we write the query that initiates rollback. We simulate multiple users 
accessing the same bank account using multithreading and make sure system behaves correctly.
On a crash(power failure, server failure, network connection failure) data is stored properly.
the temporary idea is two have 2 layers: the upper layer will only had read privileges to the db, 
will run basic checks (like if the money being sent is even present, if there are other processing 
being run, crash management). After it has made sure that if transaction happens nothing bad will happen, 
it will send data to lower layer with write permission which will actually run the update command
'''
import mysql.connector, logging, datetime 
from mysql.connector import errorcode
logger = logging.getLogger(__name__)

def main():
    timestamp = datetime.datetime.now().strftime("%H-%M_%d-%m-%Y")
    logging.basicConfig(filename=f'logs/{timestamp}_logs.txt', level=logging.INFO, format='%(asctime)s %(message)s')
    logger.info("setup.py running")
    databaseSetup()

# Runs mysql create statements
def databaseSetup(): 

    logger.info("Setting up database structure")
    db = mysql.connector.connect(user='root',password='Ajinkya!1')
    cursor = db.cursor()

    createDBQuery = "create database if not exists bank;"
    useDBQuery = "use bank;"

    Tables = {}

    Tables["Customer"] =  ''' Create table if not exists Customer (
    CustomerID int auto_increment primary key,
    Name varchar(25) not null,
    Email varchar(30) unique not null,
    Phone varchar(13) unique not null,
    Address text not null,
    DOB date); '''

    Tables["AccountType"] = '''create table if not exists AccountType (
    TypeID int auto_increment primary key,
    TypeName enum('Current','Savings','Salary','Fixed Deposit') not null,
    MinBalance decimal(15,2) default 0.00,
    OverdraftLimit decimal(15,2) default 0.00,
    InterestRate decimal(5,4) default 0.0000);'''

    Tables["Account"] = ''' Create table if not exists Account (
    AccountID int auto_increment primary key,
    AccountType int not null,
    CustomerID int not null,
    Balance decimal(15,2) not null default 0.00,
    foreign key (AccountType) references accounttype(typeID),
    foreign key (CustomerID) references Customer(CustomerID)); '''

    Tables["Transaction"] = ''' Create table if not exists Transaction (
    TransactionID int auto_increment primary key,
    TransactionType enum('Transfer', 'Deposit', 'Withdrawal', 'Fee', 'Interest') not null,
    SenderID int not null,
    ReceiverID int,
    Status enum('Processing', 'Completed', 'Failed'),
    InitiatedAt timestamp default current_timestamp,
    CompletedAt timestamp,
    foreign key (SenderID) references Account(AccountID),
    foreign key (ReceiverID) references Account(AccountID));'''

    Tables["Deadlock"] = ''' Create table if not exists Deadlock (
    DeadlockID int auto_increment primary key,
    VictimID int not null,
    ResolutionAction enum('Rollback','Timeout','Manual'),
    DetectedAt timestamp default current_timestamp,
    ResolvedAt timestamp,
    Foreign key (VictimID) references Transaction(TransactionID)
    );'''

    Tables["Log"] = ''' Create table if not exists Log (
    LogID int auto_increment primary key,
    ActionType varchar(50) not null,
    LogTime timestamp default current_timestamp,
    Description text);'''

    cursor.execute("begin;")
    try: 
        cursor.execute(createDBQuery)
        cursor.execute(useDBQuery)
        for table in Tables:
            desc = Tables[table]
            cursor.execute(desc)
            print(f"Created table: {table}")
        logger.info("Table creation complete")
        cursor.execute("commit;")
    except mysql.connector.Error as err:
        logger.error(err.msg)
        cursor.execute("rollback;")


if __name__ == '__main__':
    main()
    



