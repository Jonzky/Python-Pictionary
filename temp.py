from tkinter import *
from tkinter.messagebox import showwarning as errorbox
from tkinter.messagebox import showinfo as infobox
import os, sys, time, threading, socket
from PictClient import ClientConnection


global ClientConnnected
ClientConnected = False

class UserInterface(Frame):

	def __init__(self, master=None):

		Frame.__init__(self, master)
		self.parent = master
		self.master.title("Python Pictionary")
		self.loggedin = False
		self.connected = False
		self.make_connection()
		self.master.protocol("WM_DELETE_WINDOW", self.quit)
	
	def quit(self):
	
		self.parent.quit()

	def make_connection(self):

		self.parent.withdraw()
		self.connection_window = Toplevel(self)
		self.connection_window.protocol("WM_DELETE_WINDOW", self.quit)
		self.Address = Entry(self.connection_window)
		self.Address.insert(0, '127.0.0.1')
		self.Port = Entry(self.connection_window)
		self.Submit = Button(self.connection_window, text='Submit', command=self.submit_connection)
		self.Clear = Button( self.connection_window, text='Clear', command=self.clear_connection)
		#L... is the label equivilant to the entry (text box)
		
		self.LAddress = Label(self.connection_window,text="Sever Address:")
		self.LPort = Label(self.connection_window,text="Sever port:")
		
		self.Address.grid(row=0, column=1)
		self.Port.grid(row=1, column=1)
		self.LAddress.grid(row=0, column=0)
		self.LPort.grid(row=1, column=0)		
		self.Submit.grid(row=0, column=2)
		self.Clear.grid(row=1, column=2)

	def make_login(self):

		self.connection_window.withdraw()
		self.login_Window = Toplevel(self)		
		self.login_Window.protocol("WM_DELETE_WINDOW", self.quit)
		self.Login_Username = Entry(self.login_Window)
		self.Login_Password = Entry(self.login_Window, show="*")
		self.Login_Submit = Button(self.login_Window, text='Submit', command=self.submit_login)
		self.Login_Clear = Button(self.login_Window, text='Clear', command=self.clear_login)
		self.LUsername = Label(self.login_Window,text="Username:")
		self.LPassword = Label(self.login_Window,text="Password:")
		self.Login_Username.grid(row=1, column=1)
		self.Login_Password.grid(row=2, column=1)
		self.LUsername.grid(row=1, column=0)
		self.LPassword.grid(row=2, column=0)
		self.Login_Clear.grid(row=1, column=2)
		self.Login_Submit.grid(row=2, column=2)


	def make_registration(self):

		self.Registration_Window = Toplevel(self)		
		self.Registration.protocol("WM_DELETE_WINDOW", self.quit)
		self.Nickname = Entry(self)
		self.Username = Entry(self)
		self.Password = Entry(self, show="*")
		self.Email = Entry(self)
		self.Submit = Button(self, text='Submit', command=self.submit_reigistration)
		self.Clear = Button( self, text='Clear', command=self.clear_registration)
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

	def submit_registration(self):

		self.ENickname = self.Nickname.get().lower()
		self.EUsername = self.Username.get().lower()
		self.EPassword = self.Password.get().lower()
		self.EEmail = self.Email.get().lower()

	def submit_connection(self):

		print(self)
		self.EAddress = self.Address.get()
		
		try:		
			self.EPort = int(self.Port.get())
		except:
			errorbox("Invalid Port", "The port you entered is invalid, please eneter a valid integer")
			return			

		self.client_socket = ClientConnection(self)			
		self.client_socket.easy_host = self.EAddress
		self.client_socket.host_port = self.EPort
		self.client_socket.daemon = True

		try:
			self.client_socket.start()
			print("Socket?")
			#Timer needed otherwise the the threaded functions will not run in time.
			time.sleep(2.0)			
			if self.connected == False:
				print("False")
				raise ValueError
			time.sleep(0.5)
			self.make_login()

		except ValueError:
			errorbox("Unable to connect", "Please check the server address/port is correct and/or you are connected to the internet")
			return

	def warn_exit(self):
			
		errorbox("An error has occured!", "An error has occured and the program has been forced to shutdown, sorry for the trouble!")

	def submit_login(self):

		self.EUsername = self.Login_Username.get().lower()
		self.EPassword = self.Login_Password.get().lower()
		data = "{}|{}".format(self.EUsername, self.EPassword)
		packet = "Login^{}".format(data)
		print(packet)

		self.client_socket.send_data(packet)
		time.sleep(2)
		if self.loggedin == True:
			print("Ooooo God yes!")
			pass
		else:		
			errorbox("Invalid login details", "Please check the information is correct, if the issue persists then contact an administrator")					

	def clear_login(self):
		pass

	def clear_connection(self):
		pass
root = Tk()
a = UserInterface(root)
a.mainloop()
