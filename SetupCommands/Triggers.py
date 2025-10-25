# add trigger to set last update field in Account table and manage processing in txn table
Triggers = {}

Triggers["UpdateAccAfterTxn"] = '''create trigger accUpdate after update on transaction for each row
begin
if new.status = 'Completed' then 
update account acc set acc.UpdatedAt = current_timestamp where new.senderID = acc.accountid;
update account acc set acc.UpdatedAt = current_timestamp where new.receiverID = acc.accountid;
end if;
end;
'''