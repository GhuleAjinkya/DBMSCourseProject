Procedures = {}

Procedures["Transfer"] = '''
drop procedure if exists TransferAmount;
delimiter $$
create procedure TransferAmount (SenderID int, ReceiverID int, amount decimal(15,2), pause int)
begin
declare senderBalance decimal(15,2);
declare receiverBalance decimal(15,2);
declare lastTxnID int;
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