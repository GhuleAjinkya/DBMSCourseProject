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
InterestRate decimal(5,4) default 0.0000,
check (MinBalance >= 0),
check (OverdraftLimit >= 0),
check (InterestRate >= 0));'''

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
foreign key (ReceiverID) references Account(AccountID),
check (CompletedAt is null or CompletedAt >= InitiatedAt));'''

Tables["Deadlock"] = ''' Create table if not exists Deadlock (
DeadlockID int auto_increment primary key,
VictimID int not null,
ResolutionAction enum('Rollback','Timeout','Manual'),
DetectedAt timestamp default current_timestamp,
ResolvedAt timestamp,
Foreign key (VictimID) references Transaction(TransactionID),
check (ResolvedAt is null or ResolvedAt >= DetectedAt));'''

Tables["Log"] = ''' Create table if not exists Log (
LogID int auto_increment primary key,
ActionType varchar(50) not null,
LogTime timestamp default current_timestamp,
Description text);'''