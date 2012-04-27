from tkinter import *
from tkinter.messagebox import showwarning as errorbox
from tkinter.messagebox import showinfo as infobox
import os, sys, time, threading, socket, builtins, ShootPyGame
from PictClient import ClientConnection
from PictClient import TCPConnection


global ClientConnnected, username
ClientConnected = False
connected = False


class UserInterface(Frame):

	def __init__(self, master=None):

		Frame.__init__(self, master)
		self.parent = master
		self.master.title("Python Pictionary")
		self.loggedin = False
		self.connected = False
		self.make_connection()
		self.registration_success = True
		self.registration_failed = False
		self.registration_failed_username = False
		self.registration_failed_email = False
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
		self.CreateAccount = Button(self.login_Window, text='Create an account', command=self.make_registration)
		self.LUsername = Label(self.login_Window,text="Username:")
		self.LPassword = Label(self.login_Window,text="Password:")
		self.LTitle = Label(self.login_Window, text='Login Form:')
		self.Login_Username.grid(row=1, column=1)
		self.Login_Password.grid(row=2, column=1)
		self.LUsername.grid(row=1, column=0)
		self.CreateAccount.grid(row=3, column=1)
		self.LPassword.grid(row=2, column=0)
		self.LTitle.grid(row=0, column=1)
		self.Login_Clear.grid(row=1, column=2)
		self.Login_Submit.grid(row=2, column=2)


	def make_registration(self):

		self.login_Window.withdraw()

		self.Registration_Window = Toplevel(self.login_Window)		
		self.Registration_Window.protocol("WM_DELETE_WINDOW", self.quit)
		self.Nickname = Entry(self.Registration_Window)
		self.Username = Entry(self.Registration_Window)
		self.Password = Entry(self.Registration_Window, show="*")
		self.Email = Entry(self.Registration_Window)
		self.Submit = Button(self.Registration_Window, text='Submit', command=self.submit_registration)
		self.Clear = Button(self.Registration_Window, text='Clear', command=self.clear_registration)
		self.Cancel = Button(self.Registration_Window,text='Cancel', command=self.cancel_registration)
		self.LNickname = Label(self.Registration_Window,text="Nickname:")
		self.LUsername = Label(self.Registration_Window,text="Username:")
		self.LPassword = Label(self.Registration_Window,text="Password:")
		self.LEmail = Label(self.Registration_Window,text="Email")
		self.Nickname.grid(row=0, column=1)
		self.Username.grid(row=1, column=1)
		self.Password.grid(row=2, column=1)
		self.Email.grid(row=3, column=1)
		self.Cancel.grid(row=3, column=2)
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
		self.ENick = self.Nickname.get().lower()
#		self.Registration_Window.withdraw()
#		self.login_Window.deiconify()

		data = "{}|{}|{}|{}".format(self.EUsername, self.EPassword, self.EEmail, self.ENick)
		packet = "Registration^{}".format(data)
		self.client_socket.send_data(packet)

	def submit_connection(self):

		self.EAddress = self.Address.get()
		
		try:		
			self.EPort = int(self.Port.get())
		except:
			errorbox("Invalid Port", "The port you entered is invalid, please eneter a valid integer")
			return			

		self.client_socket = ClientConnection(self, self.EAddress, self.EPort)

		try:
			self.client_socket.start()
			#Timer needed otherwise the the threaded functions will not run in time.
			time.sleep(2.0)			
			if self.connected == False:
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

		self.client_socket.send_data(packet)
		time.sleep(1)
		if self.loggedin == True:
			global username, host, port, randomint, connected
			
			connected = True
			self.client_socket.running = False
			randomint = int(self.client_socket.randomint)
			username = self.EUsername
			host, port = str(self.EAddress), int(self.EPort)

			time.sleep(1)

			self.master.quit()
#			self.login_Window.withdraw()
			self.quit()
		else:		
			errorbox("Invalid login details", "Please check the information is correct, if the issue persists then contact an administrator")					

	def clear_login(self):
		pass

	def clear_connection(self):
		pass
	def clear_registration(self):
		pass
	def cancel_registration(self):
		
		self.Registration_Window.withdraw()
		self.login_Window.deiconify()


##############Was getting too fustrated with this being the main thread in the program, try to remove 
##############Tkinter when finished and make pygame the main thread.
def start():

	root = Tk()
	a = UserInterface(root)
	a.mainloop()
	if connected == True:	
		root.destroy()
		time.sleep(2)
		a = ShootPyGame.start(host, port, randomint)
	#Not the best way to deal with this but should give pygame (which has daemon=False) to kick in.	

	

if __name__ == "__main__":
		
	start()	

