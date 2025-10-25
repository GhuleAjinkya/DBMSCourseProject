Events = {}

Events["backup"] = '''
drop database if exists BankBackup;
create database BankBackup;
delimiter $$
create event backupAccountsAndTxns on schedule every 1 minute
do 
begin 
create table if not exists BankBackup.AccountBackup like Bank.Account;
create table if not exists BankBackup.TransactionBackup like Bank.Transaction;
insert into BankBackup.TransactionBackup 
select * from Bank.transaction old where old.CompletedAt >= now() - interval 1 minute and 
old.transactionID not in (select transactionID from bankBackup.transactionBackup);
insert into BankBackup.AccountBackup
select * from bank.account acc where acc.accountid not in (select accountID from BankBackup.AccountBackup);
update bankbackup.accountbackup b join bank.account a on b.AccountID = a.AccountID set 
b.Balance = a.Balance, 
b.AccountType = a.AccountType, 
b.CustomerID = a.CustomerID,
b.UpdatedAt = a.UpdatedAt
where a.UpdatedAt >= now() - interval 1 minute or a.UpdatedAt is null;
end;
$$
delimiter ;
'''

Events["RetryProcessing"] = '''
delimiter $$
create event RetryTxnStuckAtProcessing on schedule every 30 second do
begin

'''