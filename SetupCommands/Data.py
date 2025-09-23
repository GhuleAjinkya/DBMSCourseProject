Data = {}

Data["Customer"] = '''
insert into Customer (Name, Email, Phone, Address, DOB) values
('John Doe', 'John@example.com', '9876543210', '123 Main St', '1990-05-15'),
('Jane Doe', 'Jane@example.com', '9123456789', '456 Oak St', '1985-11-23');
'''
Data["AccountType"] = '''
insert into AccountType (TypeName, MinBalance, OverdraftLimit, InterestRate) values
('Current', 5000.00, 10000.00, 0.0000),
('Savings', 1000.00, 0.00, 0.0250),
('Salary', 0.00, 0.00, 0.0100),
('Fixed Deposit', 10000.00, 0.00, 0.0550);
'''
Data["Account"] = '''
insert into Account (AccountType, CustomerID, Balance) values
(1, 1, 15000.00), 
(2, 2, 5000.00),
(1,1,2000),
(2,2,3000);
'''