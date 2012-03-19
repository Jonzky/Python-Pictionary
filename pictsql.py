### Manages SQL

import sqlite3, os

class SQLManager():

	def __init__(self):
				
		self.path = ""
		self.database = ""
		
	def main(self):
	
		if self.path or self.database == "":
			
			print("Error")
		
		if not os.path.exists(self.path):
			os.makedirs("./data")
		
		self.connection = sqlite3.connect('./data/example')
		self.con = self.connection.cursor()
	
	def create_table(self, table):
		
		self.con.execute(table)	
		
	def execute(self, execution):
		
		self.con.execute(execution)
		self.connection.commit()

	def retrieve_data(self, execution):
	
		self.con.execute(execution)
		self.data = self.con.fetchall()

		print(self.data)
	
	def add_user(self, table, username, password, email):
		
		a = """insert into {}(username,password,email)
		values (?,?,?)""".format(table)
		data = (username, password, email,)
		self.con.execute(a, data)	
		self.connection.commit()
		
	def check_username(self, table, field, value):
		
		a = "SELECT score FROM user WHERE username = ?", ('usernametest')
		name = (value,)
		
		exec_str = 'select * from {} where {}=?'.format(table, field)
		self.con.execute(exec_str, name)
		data = self.con.fetchone()

		if data is None:
			return False
		else:
			return True	

def tests():

	user_table = ('''CREATE TABLE IF NOT EXISTS user
(id INTEGER PRIMARY KEY AUTOINCREMENT, 
username VARCHAR(25) NOT NULL,
password VARCHAR(25) NOT NULL,
timeplayed INTEGER DEFAULT 0 NOT NULL,
email VARCHAR(25) NOT NULL,
score VARCHAR(25) DEFAULT '0' NOT NULL,
UNIQUE (username),
UNIQUE (email))''')

	test_execution = ("""insert into user
          values ('usernametest','password1',1,'JonZakay@aol.com',10)""")


