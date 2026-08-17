import customtkinter as ctk
from tkinter import messagebox

from auth import load_users, save_users
from menu_manager import load_menu, save_menu


class AdminMenu():

    def __init__(self):

        #Data
        self.users = load_users()
        self.menu = load_menu()

        #Orders
        self.orders = []

        #Main window
        self.root = ctk.CTk()
        self.root.title("Canteen Ordering System - Admin")
        self.root.geometry("1100x750")
        self.root.configure(fg_color="#23272D")

        #Header
        header = ctk.CTkFrame(self.root, height=70, fg_color="#343739", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="Admin Dashboard", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=25, pady=20)

        ctk.CTkButton(header, text="Logout", width=100, fg_color="#d9534f", hover_color="#a83232", command=self.logout).pack(side="right", padx=20)

        #Tabs
        self.tabs = ctk.CTkTabview(self.root, width=1000, height=600)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabs.add("Dashboard")
        self.tabs.add("Accounts")
        self.tabs.add("Menu")
        self.tabs.add("Orders")

        self.root.mainloop()

        
    #Logout
    def logout(self):

        self.root.destroy()