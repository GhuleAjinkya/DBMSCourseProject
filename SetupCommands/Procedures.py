Procedures = {}

Procedures["Transfer"] = '''
drop procedure if exists TransferAmount;
delimiter $$
create procedure TransferAmount (SenderID int, ReceiverID int, amount decimal(15,2), pause int)
begin
declare senderBalance decimal(15,2);
declare receiverBalance decimal(15,2);
declare senderExists int;
declare receiverExists int;
declare lastTxnID int;
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
insert into transaction (transactiontype, senderid, receiverid, status)
values ('Transfer',senderid, receiverid, 'Processing');
set lastTxnID = last_insert_id();
start transaction;
if SenderID < ReceiverID then 
select Balance into senderBalance from Account where AccountID = SenderID for update;
select Balance into receiverBalance from Account where AccountID = ReceiverID for update;
else 
select Balance into receiverBalance from Account where AccountID = ReceiverID for update;
select Balance into senderBalance from Account where AccountID = SenderID for update;
end if;
if pause > 0 then 
Do sleep(5); 
end if;
if senderBalance < amount then rollback;
signal sqlstate '45000' set message_text = 'Insufficient balance';
update transaction set status = 'Failed' where TransactionID = lastTxnID;
else 
update account set Balance = Balance - amount where AccountID = senderID;
update account set Balance = Balance + amount where AccountID = receiverID;
update transaction set status = 'Completed', 
CompletedAt = current_timestamp where TransactionID = lastTxnID;
commit;
end if;
end;
$$
delimiter ;
'''