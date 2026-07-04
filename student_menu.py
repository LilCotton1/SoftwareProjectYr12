import tkinter as tk
from tkinter import ttk
from menu_manager import load_menu

class StudentMenu():
    def __init__(self, username):
        self.username = username
        #Menu
        self.root = tk.Tk()
        self.root.title("Menu")
        self.root.geometry("800x600")
        self.menu = load_menu()

        #Welcome thingy
        tk.Label(self.root, text = f"Welcome, {self.username}").pack()

        #Search
        tk.Label(self.root, text = "Search").pack(pady="30")
        entry = tk.Entry(self.root).pack()

        #Treeview for the menu
        self.tree = ttk.Treeview(self.root, columns=("Name", "Price", "Stock", "Category", "Description", "Daily Special"), show = "headings")
        self.tree.heading("Name", text = "Name")
        self.tree.heading("Price", text = "Price")
        self.tree.heading("Stock", text = "Stock")
        self.tree.heading("Category", text = "Category")
        self.tree.heading("Description", text = "Description")
        self.tree.heading("Daily Special", text = "Daily Special")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for item, info in self.menu.items():
            self.tree.insert(
                "",
                tk.END, values=(item, f"${info['price']:.2f}", info["stock"], info["category"], info["description"], "Yes" if info["daily_special"] else "No",))

        #Logout button
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)
        self.root.mainloop()

    #Logout function
    def logout(self):
        self.root.destroy()