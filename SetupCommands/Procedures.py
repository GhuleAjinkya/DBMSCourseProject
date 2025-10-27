Procedures = {}

Procedures["Transfer"] = '''
delimiter $$
create procedure TransferAmount (SenderID int, ReceiverID int, amount decimal(15,2), pause int)
begin
declare senderBalance decimal(15,2);
declare senderExists int;
declare receiverExists int;
declare lastTxnID int;
declare senderLockName varchar(50);
declare receiverLockName varchar(50);

if amount <= 0 then signal sqlstate '45000' set message_text = 'Amount must be positive';
end if;
if SenderID = ReceiverID then signal sqlstate '45000' set message_text = 'Cannot transfer to same account';
end if;
select count(*) into senderExists from Account where AccountID = senderID;
if senderExists = 0 then signal sqlstate '45000' set message_text = 'Sender account doesnt exists';
end if;
select count(*) into receiverExists from Account where AccountID = receiverID;
if receiverExists = 0 then signal sqlstate '45000' set message_text = 'Receiver account doesnt exists';
end if;

set senderLockName = concat('account_', SenderID);
set receiverLockName = concat('account_', ReceiverID);
if SenderID < ReceiverID then
    do GET_LOCK(senderLockName, -1);
    do GET_LOCK(receiverLockName, -1);
else
    do GET_LOCK(receiverLockName, -1);
    do GET_LOCK(senderLockName, -1);
end if;

insert into transaction (transactiontype, senderid, receiverid, status, Amount)
values ('Transfer',senderid, receiverid, 'Processing', amount);
set lastTxnID = last_insert_id();

start transaction;
if SenderID < ReceiverID then 
select Balance into senderBalance from Account where AccountID = SenderID for update;
select Balance from Account where AccountID = ReceiverID for update;
else 
select Balance from Account where AccountID = ReceiverID for update;
select Balance into senderBalance from Account where AccountID = SenderID for update;
end if;
if pause > 0 then   
Do sleep(pause); 
end if;
if senderBalance < amount then
update transaction set status = 'Failed' where TransactionID = lastTxnID;
commit;
signal sqlstate '45000' set message_text = 'Insufficient balance';
else 
update account set Balance = Balance - amount where AccountID = senderID;
update account set Balance = Balance + amount where AccountID = receiverID;
update transaction set status = 'Completed', 
CompletedAt = current_timestamp where TransactionID = lastTxnID;
commit;
end if;

if IS_USED_LOCK(senderLockName) is not null then do RELEASE_LOCK(senderLockName); 
end if;
if IS_USED_LOCK(receiverLockName) is not null then do RELEASE_LOCK(receiverLockName); 
end if;
end;
$$
delimiter ;
'''

Procedures["retry"] = '''
delimiter $$
create procedure RetryTransfer (SenderID int, ReceiverID int, Amount int, trxID int)
begin
    declare senderBalance int;
    declare lastTxnID int;
    insert into transaction (transactiontype, senderid, receiverid, status, Amount)
    values ('Transfer',senderid, receiverid, 'Processing', amount);
    set lastTxnID = last_insert_id();

    start transaction;
    if SenderID < ReceiverID then 
        select Balance into senderBalance from Account where AccountID = SenderID for update;
        select Balance from Account where AccountID = ReceiverID for update;
    else 
        select Balance from Account where AccountID = ReceiverID for update;
        select Balance into senderBalance from Account where AccountID = SenderID for update;
    end if;
    if senderBalance < amount then
        update transaction set status = 'Failed' where TransactionID = lastTxnID;
        commit;
    else 
        update account set Balance = Balance - amount where AccountID = senderID;
        update account set Balance = Balance + amount where AccountID = receiverID;
        update transaction set status = 'Completed', CompletedAt = current_timestamp 
        where TransactionID = lastTxnID;
        commit;
    end if;
    insert into RetriedTransactions (TransactionID) values (trxID);
end ;
$$
delimiter ;
'''

