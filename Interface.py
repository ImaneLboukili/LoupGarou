from Tkinter import *

class Partie:
	
	
	
	def __init__(self, root):
		self.user = ""
		
		self.root = root
		self.s = Label(text ="Bienvenue", font=(('Times'),20))
		self.s.grid(row=2,column=0)


		self.N = Label(text ="Nouvelle partie de Loup Garou\n \nVeuillez entrer votre nom")
		self.N.grid(row=3,column=0)

		self.e = Entry(self.root)
		self.e.focus_set()
		self.e.grid(row=4, column=0)


		self.b = Button(self.root, text="OK", width=10, command=self.getname)
		self.b.grid(row=5, column=0)

		
		TI = Button(text="Play", width =50, command=lambda: self.Vote(self.user))
		TI.grid(row=6, column=0)

		root.mainloop()
		
	def getname(self):
		self.user = self.e.get()
		print self.user
		
	def Vote(self, user):
		top=Toplevel()
		top.title("Let's vote...")
		notiLabel = Label(top, text ="Qui souhaitez vous tuer, "+self.user+" ?", font=('Times', 20))
		notiLabel.grid(row=0,column=0, sticky=W)
		
		notiLabel = Label(top, text ="Chat", font=('Times', 16), height = 20)
		notiLabel.grid(row=1,column=0, sticky=W)
		
		field = Entry(top)
		field.focus_set()
		field.grid(row=2, column=0)

		listbox = Listbox(top)
		listbox.grid(row=1,column=1, sticky=W)

		listbox.insert(END, "list of users")
		b = Button(top, text="You die")
		b.grid(row=2, column=1)

		for item in ["Imane", "Louise", "Pierre", "Oceane"]:
			listbox.insert(END, item)
			
	
root=Tk()
root.title("Loup Garou")

game = Partie(root)
