import customtkinter as ctk

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
        self.create_accounts()

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


    #Shows all accounts
    def create_accounts(self):

        account_tab = self.tabs.tab("Accounts")

        ctk.CTkLabel(account_tab, text="Account Management", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=15)

        #Search frame
        search_frame = ctk.CTkFrame(account_tab, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)

        #Entry box to input specific usernames
        self.account_search = ctk.CTkEntry(search_frame, placeholder_text="Search username...", width=300)
        self.account_search.pack(side="left", padx=5)

        #Buttons to search and to clear
        ctk.CTkButton(search_frame, text="Search", command=self.search_accounts, width=100).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Clear", command=self.clear_account_search, width=100, fg_color="#505557", hover_color="#3d4143").pack(side="left", padx=5)

        #Users frame
        self.accounts_frame = ctk.CTkScrollableFrame(account_tab)
        self.accounts_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.display_accounts(self.users)

    #Displays every user
    def display_accounts(self, users):
        for widget in self.accounts_frame.winfo_children():
            widget.destroy()
        for username, info in users.items():
            user_frame = ctk.CTkFrame(self.accounts_frame, fg_color="#343739")
            user_frame.pack(fill="x", padx=5, pady=5)
            role = info.get("role", "student")
            balance = info.get("balance", 0.00)

            #Labels
            ctk.CTkLabel(user_frame, text=username, font=ctk.CTkFont(size=17, weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkLabel(user_frame, text=f"Role: {role}").pack(side="left", padx=15)
            ctk.CTkLabel(user_frame, text=f"Balance: ${balance:.2f}").pack(side="left", padx=15)
            ctk.CTkButton(user_frame, text="Edit", width=80, command=lambda username=username: self.edit_user(username)).pack(side="right", padx=5)

    #Search accounts
    def search_accounts(self):
        search = self.account_search.get().lower()
        
        filtered = {}

        for username, info in self.users.items():
            if search in username.lower():
                filtered[username] = info

        self.display_accounts(filtered)

    #Clear search
    def clear_account_search(self):
        self.account_search.delete(0, "end")
        self.display_accounts(self.users)

    def edit_user(self, username):
        window = ctk.CTkToplevel(self.root)
        window.title(f"Edit Account")
        window.geometry("400x300")
        window.resizable(False, False)

        #Labels
        ctk.CTkLabel(window, text="Edit Account", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(window, text=f"Username: {username}", font=ctk.CTkFont(size=16)).pack(pady=10)

        #Role selection via dropdown menu
        role_drop = ctk.CTkOptionMenu(window, values=["student", "admin"], width=200)
        role_drop.set(self.users[username].get("role", "student"))
        role_drop.pack(pady=10)

        #Add balance entry
        balance_entry = ctk.CTkEntry(window, placeholder_text="Add balance", width=200)
        balance_entry.insert(0, str(self.users[username].get("balance", 0.00)))
        balance_entry.pack(pady=10)

        #Save button
        def save_changes():
            new_role = role_drop.get().lower()
            new_balance = float(balance_entry.get())

            if new_role not in ["student", "admin"]:
                self.popup("Error", "Invalid role selected.")
                return
            if new_balance < 0:
                self.popup("Invalid Balance", "Balance cannot be negative.")
                return
            
            self.users[username]["role"] = new_role
            self.users[username]["balance"] = new_balance
            save_users(self.users)
            self.display_accounts(self.users)
            window.destroy()

        #Save and cancel buttons
        ctk.CTkButton(window, text="Save Changes", command=save_changes, width=180).pack(pady=20)
        ctk.CTkButton(window, text="Cancel", command=window.destroy, width=180, fg_color="#505557", hover_color="#3d4143").pack()

    #Popup
    def popup(self, title, message):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("350x200")
        popup.resizable(False, False)

        #Message
        ctk.CTkLabel(popup, text=message, wraplength=300, font=ctk.CTkFont(size=14)).pack(pady=40)

        #OK button
        ctk.CTkButton(popup, text="OK", command=popup.destroy, width=100).pack()
    #Logout
    def logout(self):

        self.root.destroy()