from tkinter import *
from tkinter.messagebox import showwarning as errorbox
from tkinter.messagebox import showinfo as infobox
import os, sys

#Will need to work out the right dimensions based on number of widgets...
w, h = 1000, 600

class RegistrationWindow():
	
	def __init__(self):
	
		self.frame = Tk()
		self.frame.title("Registration form")
#		self.frame.pack()
#		self.grid()
		
		self.make_widgets()
		
		
	def make_widgets(self):	
		
		self.Nickname = Entry(self.frame)
		self.Username = Entry(self.frame)
		self.Password = Entry(self.frame, show="*")
		self.Email = Entry(self.frame)
		self.Submit = Button(self.frame, text='Submit', command=self.submit)
		self.Clear = Button( self.frame, text='Clear', command=self.clear)
		#L... is the label equivilant to the entry (text box)
		
		self.LNickname = Label(self.frame,text="Nickname:")
		self.LUsername = Label(self.frame,text="Username:")
		self.LPassword = Label(self.frame,text="Password:")
		self.LEmail = Label(self.frame,text="Email")
		
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
#		errorbox("An error has occured!", "Please check all entries are valid")

	
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
		
import pictsql
b = pictsql.SQLManager()
b.path = './data'
b.main()

b.field = 'username'


a = RegistrationWindow()
a.frame.mainloop()
