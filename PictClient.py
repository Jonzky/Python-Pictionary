### This is a very basic implementation to ensure the User/SQL queries are handled correctly
### Prior to incorparating the GUI in PyGame

class Client():


	def __init__(self):
		
		print("passed")
		self.main()

	def main(self):
	
		selection = input("newuser, user or forgotten >> ")
		
		if selection == "newuser":
			self.newuser()
		else:
			self.user()	
		
		
	def newuser(self):
		
		self.name = input("name >> ")
		self.username = input("username >> ")
		self.password = input("password >> ")
		self.email = input("email >> ")

	def user(self):
		
		self.username = input("username >> ")
		self.password = input("password >> ")
	
	def forgotten(self):
	
		self.username = input("username >> ")
		
Client()		
		
		

