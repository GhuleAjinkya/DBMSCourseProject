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
declare txnID int;
declare sID int;
declare rID int;
declare amt int;
declare senderLockName varchar(50);
declare receiverLockName varchar(50);
declare done int;
declare txnCursor cursor for
    select TransactionID, SenderID, ReceiverID, Amount from Transaction 
        where status = 'Processing' and 
        InitiatedAt <= now() - interval 30 second;

declare continue handler for not found set done = 1;
open txnCursor;
retry_loop: loop
    fetch txnCursor into txnID, sID, rID, amt;
    if done = 1 then leave retry_loop; 
    end if;
    set senderLockName = concat('account_', sID);
    set receiverLockName = concat('account_', rID);
    if IS_FREE_LOCK(senderLockName) = 1 and IS_FREE_LOCK(receiverLockName) = 1 then
        update Transaction set status = 'Failed' where TransactionID = txnID;
        call retryTransfer(sID,rID,amt,txnID);
    end if;
end loop;
close txnCursor;
end ;
$$
delimiter ;
'''