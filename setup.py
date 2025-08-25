# This file generates schema and populates it with data, if required
# Refer to ER_Diagram in parent directory
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

logger = logging.getLogger(__name__)

def main():
    timestamp = datetime.datetime.now().strftime("%H-%M_%d-%m-%Y")
    logging.basicConfig(filename=f'logs/{timestamp}_logs.txt', level=logging.INFO, format='%(asctime)s %(message)s')
    logger.info("setup.py running")


if __name__ == '__main__':
    main()
    



