# This file generates the tables, if required
import mysql.connector, logging, datetime 
from SetupCommands.Tables import Tables
from SetupCommands.Data import Data
from SetupCommands.Procedures import Procedures
from SetupCommands.Globals import Globals
import demo
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
    cursor.execute("drop database bank;")
    createDBQuery = "create database bank;"
    useDBQuery = "use bank;"

    try: 
        cursor.execute(createDBQuery)
        cursor.execute(useDBQuery)
        for table in Tables:
            desc = Tables[table]
            cursor.execute(desc)
        logger.info("Table creation completed")

        for data in Data:
            desc = Data[data]
            cursor.execute(desc)
        logger.info("Temp data inserted")

        for setting in Globals:
            desc = Globals[setting]
            cursor.execute(desc)
        logger.info("InnoDB settings changed")

        for procedure in Procedures:
            desc = Procedures[procedure]
            cursor.execute(desc)
        logger.info("Procedures created")


    except mysql.connector.Error as err:
        logger.error(err.msg)
    
    tmp = demo.ACIDDemo()
    tmp.runMenu()

if __name__ == '__main__':
    main()
    



