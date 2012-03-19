import pictsql

a = pictsql.SQLManager()

a.path = './data'
a.main()

test_execution = ("""insert into user(username,password,email)
values ('usernametest12','password1','JonZakay22@aol.com')""")


user_table = ('''CREATE TABLE IF NOT EXISTS user
(id INTEGER PRIMARY KEY AUTOINCREMENT, 
username VARCHAR(25) NOT NULL,
password VARCHAR(25) NOT NULL,
timeplayed INTEGER DEFAULT 0 NOT NULL,
email VARCHAR(25) NOT NULL,
score VARCHAR(25) DEFAULT '0' NOT NULL,
UNIQUE (username),
UNIQUE (email))''')

a.create_table(user_table)
a.add_user('user', 't1est1', 'test1', 'tes11t1')
#a.execute(test_execution)
#a.check_username('user', 'username', 'usernametest')
