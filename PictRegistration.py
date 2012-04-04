from tkinter import *
from tkinter.messagebox import showwarning as errorbox
from tkinter.messagebox import showinfo as infobox
import os, sys, time, threading
from PictClient import ClientConnection

global ClientConnnected
ClientConnected = False

class ServerWindow(Frame):

	def __init__(self, master=None):

		Frame.__init__(self, master)
		self.grid()
		self.master.title("Python Pictionary")
		self.connected = False		
		self.make_widgets()	
		print(self.winfo_toplevel())
		
	def make_widgets(self):	
		
		self.Address = Entry(self)
		self.Address.insert(0, '127.0.0.1')
		self.Port = Entry(self)
				
		self.Submit = Button(self, text='Submit', command=self.submit)
		self.Clear = Button( self, text='Clear', command=self.clear)
		#L... is the label equivilant to the entry (text box)
		
		self.LAddress = Label(self,text="Sever Address:")
		self.LPort = Label(self,text="Sever port:")
		
		self.Address.grid(row=0, column=1)
		self.Port.grid(row=1, column=1)
		self.LAddress.grid(row=0, column=0)
		self.LPort.grid(row=1, column=0)		
		self.Submit.grid(row=0, column=2)
		self.Clear.grid(row=1, column=2)

	
	def clear(self):
	
		self.Address.delete(0, END)
		self.Port.delete(0, END)
		a = LoginWindow()
		a.mainloop()
		self.quit()
		
	def submit(self):
		
		self.EAddress = self.Address.get()
		self.EPort = int(self.Port.get())


		while not self.connected:
			self.client_socket = ClientConnection()			
			self.client_socket.easy_host = self.EAddress
			self.client_socket.host_port = self.EPort
			self.client_socket.daemon = True
			try:
				self.client_socket.start()
				self.connected = True
				self.quit()
				time.sleep(5)
				print("conncncn")
				time.sleep(1)
			except ValueError:	
				errorbox("Unable to connect", "Please check the server address/port is correct and/or you are connected to the internet")

		self.Registration = RegistrationWindow(self)		
		while True:
	
			if self.Registration.completed == True:
				self.client_socket.send_data(self.Registration.data)
				break
			else:
				pass

class RegistrationWindow(Frame, threading.Thread):

	def __init__(self, master=None):
		

		print("Ping")
		Frame.__init__(self, master)
		print("Where?")
		self.grid()
		self.completed = False
		self.master.title("Registration form")		
		self.make_widgets()
		
		
	def make_widgets(self):	
		
		self.Nickname = Entry(self)
		self.Username = Entry(self)
		self.Password = Entry(self, show="*")
		self.Email = Entry(self)
		self.Submit = Button(self, text='Submit', command=self.submit)
		self.Clear = Button( self, text='Clear', command=self.clear)
		#L... is the label equivilant to the entry (text box)
		
		self.LNickname = Label(self,text="Nickname:")
		self.LUsername = Label(self,text="Username:")
		self.LPassword = Label(self,text="Password:")
		self.LEmail = Label(self,text="Email")
		
		self.Nickname.grid(row=0, column=1)
		self.Username.grid(row=1, column=1)
		self.Password.grid(row=2, column=1)
		self.Email.grid(row=3, column=1)
		self.LNickname.grid(row=0, column=0)
		self.LUsername.grid(row=1, column=0)
		self.LPassword.grid(row=2, column=0)
		self.LEmail.grid(row=3, column=0)
		self.Clear.grid(row=1, column=2)
		self.Submit.grid(row=2, column=2)
	
	def clear(self):
	
		self.Nickname.delete(0, END)
		self.Username.delete(0, END)
		self.Password.delete(0, END)
		self.Email.delete(0, END)
	
	def check_entry(self):
		
		if len(self.EUsername) <=2:
			errorbox("Invalid username!", "Your username needs to be over 2 characters.")
			return
		if len(self.ENickname) <=2:
			errorbox("Invalid nickname!", "Your nickname needs to be over 2 characters.")
			return 				
			
		if b.check_field('username', self.EUsername) == False:
			pass
		else:	
			errorbox("Username already taken!", "This username has been taken already, please choose another.")
			return
		if b.check_field('email', self.EEmail) == False:
			b.add_user('user', self.EUsername, self.EPassword, self.EEmail)
			infobox("Account created!", "The account has successfuly been created.")
		else:
			errorbox("Email already taken!", "An account has already been created with this email, contact an adminisrator if you do not have access to the account.")
			return				
	def submit(self):
		
		self.ENickname = self.Nickname.get().lower()
		self.EUsername = self.Username.get().lower()
		self.EPassword = self.Password.get().lower()
		self.EEmail = self.Email.get().lower()
		self.check_entry()


class LoginWindow():
	
	def __init__(self, master=None):
	
		Frame.__init__(self, master)
		self.grid()
		self.master.title("Login form")		
		self.make_widgets()
		
		
	def make_widgets(self):	
		  
		self.Username = Entry(self)
		self.Password = Entry(self, show="*")
		self.Submit = Button(self, text='Submit', command=self.submit)
		self.Clear = Button( self, text='Clear', command=self.clear)
		#L... is the label equivilant to the entry (text box)
		
		self.LUsername = Label(self,text="Username:")
		self.LPassword = Label(self,text="Password:")

		self.Username.grid(row=1, column=1)
		self.Password.grid(row=2, column=1)
		self.LUsername.grid(row=1, column=0)
		self.LPassword.grid(row=2, column=0)
		self.Clear.grid(row=1, column=2)
		self.Submit.grid(row=2, column=2)
	
	def clear(self):
	
		self.Username.delete(0, END)
		self.Password.delete(0, END)
	
	def check_entry(self):
		
		if len(self.EUsername) <=2:
			errorbox("Invalid username!", "Your username needs to be over 2 characters.")
			return
		if b.check_field('username', self.EUsername) == False:
			pass
		else:	
			errorbox("Username already taken!", "This username has been taken already, please choose another.")
			return
	def submit(self):
		
		self.EUsername = self.Username.get().lower()
		self.EPassword = self.Password.get().lower()		
		self.check_entry()
		
import pictsql
b = pictsql.SQLManager()
b.path = './data'
b.main()

b.field = 'username'


a = RegistrationWindow()
a.mainloop()

#userwindow = ServerWindow()
#userwindow.mainloop()
