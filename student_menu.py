import tkinter as tk
from tkinter import ttk

class StudentMenu():
    def __init__(self, username):
        self.username = username
        #Menu
        self.root = tk.Tk()
        self.root.title("Menu")
        self.root.geometry("800x600")

        #Welcome thingy
        tk.Label(self.root, text = f"Welcome, {self.username}").pack()

        #Search
        tk.Label(self.root, text = "Search").pack(pady="30")
        entry = tk.Entry(self.root).pack()

        #Logout button
        tk.Button(self.root, text = "Logout", command = self.logout).pack(pady="80")

    #Logout function
    def logout(self):
        self.root.destroy()


        self.root.mainloop()