### Manages SQL

import sqlite3, os
import threading

class SQLManager(threading.Thread):

	def __init__(self):
				
		self.path = "./data"
		self.database = ""
		self.table = "user"
		
	def main(self):
		
		if not os.path.exists(self.path):
			os.makedirs("./data")
		
		self.connection = sqlite3.connect('./data/example', check_same_thread = False)
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
		
	def check_field(self, field, value):
		
		name = (value,)	
		exec_str = 'select * from {} where {}=?'.format(self.table, field)
		self.con.execute(exec_str, name)
		data = self.con.fetchone()

		if data is None:
			return False
		else:
			return True
	
	def user_login(self, username, password):	

		data = (username, password)
		exec_str = 'select * from {} where username=? and password=?'.format(self.table)
		a = self.con.execute(exec_str, data)		
		if len(a) != 0:
			for row in a:
				print(row)
		else:
			print("nonw")
def tests():

	user_table = ('''CREATE TABLE IF NOT EXISTS user
(id INTEGER PRIMARY KEY AUTOINCREMENT, 
username VARCHAR(25) NOT NULL,
password VARCHAR(25) NOT NULL,
timeplayed INTEGER DEFAULT 0 NOT NULL,
email VARCHAR(25) NOT NULL,1
score VARCHAR(25) DEFAULT '0' NOT NULL,
UNIQUE (username),
UNIQUE (email))''')

	test_execution = ("""insert into user
          values ('usernametest','password1',1,'JonZakay@aol.com',10)""")


