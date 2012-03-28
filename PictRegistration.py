from tkinter import *
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
		self.Password = Entry(self.frame)
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
		pass

	def submit(self):
		pass		
		

a = RegistrationWindow()
a.frame.mainloop()
