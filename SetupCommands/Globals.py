Globals = {}

Globals["logEveryCommit"] = '''
set global innodb_flush_log_at_trx_commit = 1;
'''

Globals["syncLogsAfterCommit"] = '''
set global sync_binlog = 1;
'''

Globals["seperateTableData"] = '''
set global innodb_file_per_table = 1;
'''

Globals["transactionLevel"] = '''
set global transaction isolation level serializable;
'''

