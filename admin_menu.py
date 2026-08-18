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
        self.create_menu()

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
            ctk.CTkButton(user_frame, text="Delete", width=80, fg_color="#d9534f", hover_color="#a83232", command=lambda username=username: self.delete_user(username)).pack(side="right", padx=5)

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

    #Edit user
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

        #Save change function
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

    #Delete user
    def delete_user(self, username):
        #custom popup to confirm deletion
        popup = ctk.CTkToplevel(self.root)
        popup.title("Delete Account")
        popup.geometry("400x220")
        popup.resizable(False, False)
        popup.grab_set()

        #Labels
        ctk.CTkLabel(popup, text="Delete Account?", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(popup, text=f"Are you sure you want to delete\n'{username}'?", font=ctk.CTkFont(size=14)).pack(pady=10)

        #Frame
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=20)

        #Confirm delete function
        def confirm_delete():
            del self.users[username]
            save_users(self.users)
            self.users = load_users()
            self.display_accounts(self.users)
            popup.destroy()

            self.popup("Account Deleted", f"The account '{username}' has been deleted.")

        #Buttons
        ctk.CTkButton(button_frame, text="Yes, Delete", width=120, fg_color="#d9534f", hover_color="#a83232", command=confirm_delete).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancel", width=120, fg_color="#505557", hover_color="#3d4143", command=popup.destroy).pack(side="left", padx=10)

    #Menu management
    def create_menu(self):
        menu_tab = self.tabs.tab("Menu")
        ctk.CTkLabel(menu_tab, text="Menu Management", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=15)

        #Buttons
        button_frame = ctk.CTkFrame(menu_tab, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(button_frame, text="Add Item", width=120, command=self.add_menu_item).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Refresh", width=120, command=self.refresh_menu).pack(side="left", padx=5)

        #Menu frame
        self.menu_frame = ctk.CTkScrollableFrame(menu_tab)
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.display_menu(self.menu)

    #Displays menu
    def display_menu(self, menu):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        for item, info in self.menu.items():
            item_frame = ctk.CTkFrame(self.menu_frame, fg_color="#343739")
            item_frame.pack(fill="x", padx=5, pady=5)

            #Labels
            ctk.CTkLabel(item_frame, text=item, font=ctk.CTkFont(size=17, weight="bold")).pack(side="left", padx=15, pady=15)
            ctk.CTkLabel(item_frame, text=f"Price: ${info['price']:.2f}").pack(side="left", padx=15)
            ctk.CTkLabel(item_frame, text=f"Stock: {info['stock']}").pack(side="left", padx=15)
            ctk.CTkLabel(item_frame, text=f"Category: {info['category']}").pack(side="left", padx=15)
            if info["daily_special"]:
                ctk.CTkLabel(item_frame, text="Daily Special").pack(side="left", padx=15)

            #Buttons
            ctk.CTkButton(item_frame, text="Edit", width=80, command=lambda item=item: self.edit_menu_item(item)).pack(side="right", padx=5)
            
    #Add menu item
    def add_menu_item(self):
        window = ctk.CTkToplevel(self.root)
        window.title("Add Menu Item")
        window.geometry("400x650")
        window.resizable(False, False)

        #Labels
        ctk.CTkLabel(window, text="Add Menu Item", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        #Entry boxes
        name_entry = ctk.CTkEntry(window, placeholder_text="Item Name", width=200)
        name_entry.pack(pady=10)
        price_entry = ctk.CTkEntry(window, placeholder_text="Price", width=200)
        price_entry.pack(pady=10)
        stock_entry = ctk.CTkEntry(window, placeholder_text="Stock", width=200)
        stock_entry.pack(pady=10)
        category_entry = ctk.CTkEntry(window, placeholder_text="Category", width=200)
        category_entry.pack(pady=10)
        daily_special_entry = ctk.CTkCheckBox(window, text="Daily Special", width=200)
        daily_special_entry.pack(pady=10)

        #Add item function
        def add_item():
            name = name_entry.get()
            try:
                price = float(price_entry.get())
                stock = int(stock_entry.get())
            except ValueError:
                self.popup("Invalid Input", "Price must be a number and stock must be an integer.")
                return
            category = category_entry.get()

            if not name or not category:
                self.popup("Invalid Input", "Name and category cannot be empty.")
                return

            if price < 0 or stock < 0:
                self.popup("Invalid Input", "Price and stock cannot be negative.")
                return

            self.menu[name] = {
                "price": price,
                "stock": stock,
                "category": category,
                "daily_special": daily_special_entry.get()
            }
            save_menu(self.menu)
            self.display_menu(self.menu)
            window.destroy()

            self.popup("Item Added", f"The item '{name}' has been added to the menu.")

        #Buttons
        ctk.CTkButton(window, text="Add Item", command=add_item, width=180).pack(pady=20)
        ctk.CTkButton(window, text="Cancel", command=window.destroy, width=180, fg_color="#505557", hover_color="#3d4143").pack()

    #Edit menu items
    def edit_menu_item(self, item):
        window = ctk.CTkToplevel(self.root)
        window.title(f"Edit Menu Item - {item}")
        window.geometry("400x650")
        window.resizable(False, False)

        #Labels
        ctk.CTkLabel(window, text=f"Edit Menu Item - {item}", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        #Entry boxes
        price_entry = ctk.CTkEntry(window, placeholder_text="Price", width=200)
        price_entry.insert(0, str(self.menu[item]["price"]))
        price_entry.pack(pady=10)
        stock_entry = ctk.CTkEntry(window, placeholder_text="Stock", width=200)
        stock_entry.insert(0, str(self.menu[item]["stock"]))
        stock_entry.pack(pady=10)
        category_drop = ctk.CTkComboBox(window, values=["Main", "Side", "Drink"], width=200)
        category_drop.set(self.menu[item]["category"])
        category_drop.pack(pady=10)
        daily_special_entry = ctk.CTkCheckBox(window, text="Daily Special", width=200)
        daily_special_entry.set(self.menu[item]["daily_special"])
        daily_special_entry.pack(pady=10)

        #Save changes function
        def save_changes():
            try:
                price = float(price_entry.get())
                stock = int(stock_entry.get())
                category = category_drop.get()
                daily_special = daily_special_entry.get()

                self.menu[item] = {
                    "price": price,
                    "stock": stock,
                    "category": category,
                    "daily_special": daily_special
                }
                save_menu(self.menu)
                self.display_menu(self.menu)
                window.destroy()
                self.popup("Item Updated", f"The item '{item}' has been updated.")

            except ValueError:
                self.popup("Invalid Input", "Price must be a number and stock must be an integer.")

        #Buttons
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

    #Refresh menu
    def refresh_menu(self):
        self.menu = load_menu()
        self.display_menu(self.menu)
    #Logout
    def logout(self):

        self.root.destroy()