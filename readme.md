Transaction Management System

The goal of this project is to create a transaction management system that demonstrates ACID principles, concurrency control and deadlock handling by simulating transfers.

Features:
    1. Transaction Manager: Automatically uses begin, commit and rollback with each query
    2. Logging: Logs about the code are generated and logs regarding all database action are stored in the Log table
    3. Atomic Transfers: Both credit and debit operations go through or transaction is marked as having failed
    4. Concurrency Simulation: Multithreading to get multiple connections to DB to cause
    concurrent transactions
    5. Deadlock Detection: Uses wait-for graph to detect and resolve deadlocks by rollbacks and timeouts
    6. Read-Only Connection: Makes sure transaction is doable by checking if balance is present, no other transactions are going through, etc.
    7. Write Connection: After recieving confirmation that transaction is legal, this connection runs the update queries
    8. Error Management: For worst-case scenarios like server-side power failure, network-connection failure, etc which could insert bad data into the database, rollbacks are initiated to preserve atomicity and consistency.

Code Flow:
    1. Setup
        - Create database and populate with data
    2. Transaction Simulation Part A
        - Read relevant rows to perform dry-run
        - On detecting issues like insufficient funds, abort transaction early
        - If transaction can succeed, details are passed to write layer
    3. Transaction Simulation Part B
        - Connect to database and lock rows using 'FOR UPDATE'
        - Runs concurrency control to make sure state of database hasnt changed after Part A read by checking row level locks
        - Goes through with transaction if state matches
        - Runs deadlock detection using wait-for graph to find transactions that lock each other. One of these is aborted/timed out so others go through
    4. Final Output
        - After all constraints have been verified and any deadlocks have been removed, final update query is run and bank balances are updated
        - Transaction is committed and a new valid database stage has been reached