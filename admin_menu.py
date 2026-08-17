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

        #Creating tabs
        self.create_dashboard()

        self.root.mainloop()

    #Dashboard
    def create_dashboard(self):
        dashboard = self.tabs.tab("Dashboard")
        ctk.CTkLabel(dashboard, text="Dashboard", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=25)

        #Statistic frame
        stats_frame = ctk.CTkFrame(dashboard, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)

        #User Frame
        users_frame = ctk.CTkFrame(stats_frame, fg_color="#343739", width=250, height=150)
        users_frame.pack(side="left", fill="both", expand=True, padx=10)
        users_frame.pack_propagate(False)

        #Amount of users
        ctk.CTkLabel(users_frame, text="Users", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 5))
        self.user_count_label = ctk.CTkLabel(users_frame, text=str(len(self.users)), font=ctk.CTkFont(size=30, weight="bold"), text_color="#029CFF")
        self.user_count_label.pack()

        #Menu frame
        menu_frame = ctk.CTkFrame(stats_frame, fg_color="#343739", width=250, height=150)
        menu_frame.pack(side="left", fill="both", expand=True, padx=10)
        menu_frame.pack_propagate(False)

        #Amount of menu items
        ctk.CTkLabel(menu_frame, text="Menu Items", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 5))
        self.menu_count_label = ctk.CTkLabel(menu_frame, text=str(len(self.menu)), font=ctk.CTkFont(size=30, weight="bold"), text_color="#029CFF")
        self.menu_count_label.pack()

        #Orders frame
        order_frame = ctk.CTkFrame(stats_frame, fg_color="#343739", width=250, height=150)
        order_frame.pack(side="left", fill="both", expand=True, padx=10)
        order_frame.pack_propagate(False)

        #Amount of orders
        ctk.CTkLabel(order_frame, text="Orders", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 5))
        self.order_count_label = ctk.CTkLabel(order_frame, text=str(len(self.menu)), font=ctk.CTkFont(size=30, weight="bold"), text_color="#029CFF")
        self.order_count_label.pack()

        
    #Logout
    def logout(self):

        self.root.destroy()