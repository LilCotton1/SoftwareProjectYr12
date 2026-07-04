import tkinter as tk
from tkinter import ttk
from auth import signup
from auth import login
from tkinter import messagebox
from student_menu import StudentMenu
from admin_menu import AdminMenu

class LoginWindow():
    def __init__(self):
        #root window
        self.root = tk.Tk()
        self.root.title("Account Manager")
        self.root.geometry("420x320")

        #Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #Frames
        frame1 = ttk.Frame(notebook, width = 420, height = 300)
        frame2 = ttk.Frame(notebook, width = 420, height = 300)


        #Add frames to notebook
        notebook.add(frame1, text="Login")
        notebook.add(frame2, text="Sign up")


        #Login widgets
        ttk.Label(frame1, text="Username").pack()
        self.loginun = ttk.Entry(frame1)
        self.loginun.pack()
        ttk.Label(frame1, text="Password").pack()
        self.loginpw = ttk.Entry(frame1, show="*")
        self.loginpw.pack()
        ttk.Button(frame1, text="Login", command=self.login_clicked).pack()

        #Signup widgets
        ttk.Label(frame2, text = "Username").pack()
        self.signupun = ttk.Entry(frame2)
        self.signupun.pack()
        ttk.Label(frame2, text = "Password").pack()
        self.signuppw = ttk.Entry(frame2, show = "*")
        self.signuppw.pack()
        ttk.Label(frame2, text = "Confirm password").pack()
        self.checkpw = ttk.Entry(frame2, show = "*")
        self.checkpw.pack()
        ttk.Button(frame2, text = "Sign up", command=self.signup_clicked).pack()
        
        self.root.mainloop()
    
    def signup_clicked(self):
        username = self.signupun.get()
        password = self.signuppw.get()
        confirm = self.checkpw.get()

        if password != confirm:
            messagebox.showinfo("Login failed", "Incorrect username or password")
            return
        success = signup(username, password)

        if success:
            messagebox.showinfo("Account created", "Account created successfully")
        
        else:
            messagebox.showinfo("Username already exists", "Username already exists")
    
    def login_clicked(self):

        username = self.loginun.get()
        password = self.loginpw.get()

        role = login(username, password)

        if role == "student":
            print("Open Student Menu")
            StudentMenu(username)

        elif role == "admin":
            print("Open Admin Dashboard")
            AdminMenu()

        else:
            print("Incorrect username or password")