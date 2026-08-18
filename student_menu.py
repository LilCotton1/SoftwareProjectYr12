import customtkinter as ctk

from menu_manager import load_menu
from auth import get_balance
from auth import add_balance
from auth import load_users
from auth import save_users


class StudentMenu():
    def __init__(self, username):

        self.username = username

        #Menu
        self.menu = load_menu()

        #Balance
        self.balance = get_balance(self.username)

        if self.balance is None:
            self.balance = 0.00

        #Cart
        self.cart = []

        #Order history
        self.order_history = []

        #Main window
        self.root = ctk.CTk()
        self.root.title("Canteen Ordering System")
        self.root.geometry("900x650")
        self.root.configure(fg_color="#23272D")

        #Header
        header = ctk.CTkFrame(self.root, height=70, fg_color="#343739")
        header.pack(fill="x")
        header.pack_propagate(False)

        #Welcome
        ctk.CTkLabel(header, text=f"Welcome, {self.username}", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=20)

        #Cart
        self.cart_button = ctk.CTkButton(header, text="Cart (0)", command=self.open_cart, width=120)
        self.cart_button.pack(side="right", padx=20)

        #Tabs
        self.tabs = ctk.CTkTabview(self.root, width=850, height=500)
        self.tabs.pack(padx=20, pady=10, fill="both", expand=True)

        self.tabs.add("Menu")
        self.tabs.add("Dashboard")

        #Create tabs
        self.create_menu()
        self.create_dashboard()

        self.root.mainloop()

    #Menu
    def create_menu(self):
        menu_tab = self.tabs.tab("Menu")

        #Search
        search_frame = ctk.CTkFrame(menu_tab, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search menu...", width=400)
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(search_frame, text="Search", command=self.search_menu, width=100).pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="Clear", command=self.clear_search, width=100, fg_color="#505557", hover_color="#3d4143").pack(side="left", padx=5)

        #Menu frame
        self.menu_frame = ctk.CTkScrollableFrame(menu_tab, fg_color="#23272D")
        self.menu_frame.pack(fill="both", expand=True, padx=15, pady=5)

        #Display menu
        self.display_menu(self.menu)

    #Display menu
    def display_menu(self, menu):

        #Clear menu
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

    #Display menu
    def display_menu(self, menu):

        #Clear menu
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        #Display items
        for item, info in menu.items():

            #Item card
            item_frame = ctk.CTkFrame(self.menu_frame, fg_color="#343739", corner_radius=10)
            item_frame.pack(fill="x", padx=5, pady=8)

            #Name
            ctk.CTkLabel(item_frame, text=item, font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))

            #Description
            ctk.CTkLabel(item_frame, text=info["description"], text_color="#CCCCCC").pack(anchor="w", padx=20, pady=3)

            #Category
            ctk.CTkLabel(item_frame, text=f"Category: {info['category']}").pack(anchor="w", padx=20, pady=5)

            #Bottom frame
            bottom_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            bottom_frame.pack(fill="x", padx=20, pady=(10, 15))

            #Price
            ctk.CTkLabel(bottom_frame, text=f"${info['price']:.2f}", text_color="#029CFF", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

            #Stock
            ctk.CTkLabel(bottom_frame, text=f"Stock: {info['stock']}").pack(side="left", padx=20)

            #Daily special
            if info["daily_special"]:
                ctk.CTkLabel(bottom_frame, text="DAILY SPECIAL", text_color="#FFD700", font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")

            #Add to cart
            add_button = ctk.CTkButton(bottom_frame, text="Add to Cart", width=120, command=lambda item=item, info=info: self.add_to_cart(item, info))
            add_button.pack(side="right")

            #Out of stock
            if info["stock"] <= 0:
                add_button.configure(text="Out of Stock", state="disabled", fg_color="#505557")
    #Search menu
    def search_menu(self):

        search = self.search_entry.get().lower()

        filtered_menu = {}

        for item, info in self.menu.items():

            if search in item.lower() or search in info["category"].lower() or search in info["description"].lower():
                filtered_menu[item] = info

        self.display_menu(filtered_menu)

    #Clear search
    def clear_search(self):

        self.search_entry.delete(0, "end")
        self.display_menu(self.menu)

    #Add item to cart
    def add_to_cart(self, item, info):

        for cart_item in self.cart:

            if cart_item["item"] == item:

                if cart_item["quantity"] >= info["stock"]:
                    self.popup("Stock Limit", "You cannot add more of this item.")
                    return

                cart_item["quantity"] += 1
                self.update_cart_button()
                return

        self.cart.append({"item": item, "price": info["price"], "quantity": 1})

        self.update_cart_button()

    #Update cart button
    def update_cart_button(self):

        total_items = 0

        for item in self.cart:
            total_items += item["quantity"]

        self.cart_button.configure(text=f"Cart ({total_items})")

    #Open cart
    def open_cart(self):

        cart_window = ctk.CTkToplevel(self.root)
        cart_window.title("Shopping Cart")
        cart_window.geometry("600x600")

        #Cart title
        ctk.CTkLabel(cart_window, text="Shopping Cart", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        #Cart frame
        cart_frame = ctk.CTkScrollableFrame(cart_window, width=500, height=350)
        cart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        #Empty cart
        if not self.cart:
            ctk.CTkLabel(cart_frame, text="Your cart is empty.").pack(pady=30)
            return

        #Total
        total = 0

        #Display cart
        for cart_item in self.cart:

            item_total = cart_item["price"] * cart_item["quantity"]
            total += item_total

            item_frame = ctk.CTkFrame(cart_frame, fg_color="#343739")
            item_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(item_frame, text=cart_item["item"], font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)

            ctk.CTkLabel(item_frame, text=f"x{cart_item['quantity']}").pack(side="left", padx=10)

            ctk.CTkLabel(item_frame, text=f"${item_total:.2f}").pack(side="left", padx=10)

            ctk.CTkButton(item_frame, text="Remove", width=80, fg_color="#d9534f", hover_color="#a83232", command=lambda item=cart_item["item"]: self.remove_from_cart(item, cart_window)).pack(side="right", padx=10)

        #Total label
        ctk.CTkLabel(cart_window, text=f"Total: ${total:.2f}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=5)

        #Balance
        ctk.CTkLabel(cart_window, text=f"Balance: ${self.balance:.2f}").pack(pady=5)

        #Checkout
        ctk.CTkButton(cart_window, text="Place Order", width=200, command=lambda: self.checkout(total, cart_window)).pack(pady=15)

    #Remove item from cart
    def remove_from_cart(self, item, cart_window):

        for cart_item in self.cart:

            if cart_item["item"] == item:

                cart_item["quantity"] -= 1

                if cart_item["quantity"] <= 0:
                    self.cart.remove(cart_item)

                break

        self.update_cart_button()

        cart_window.destroy()

        self.open_cart()

    #Checkout
    def checkout(self, total, cart_window):

        if not self.cart:
            self.popup("Checkout", "Your cart is empty.")
            return

        if self.balance < total:
            self.popup("Checkout Failed", "You do not have enough money.")
            return

        users = load_users()

        if self.username not in users:
            self.popup("Checkout Failed", "Account could not be found.")
            return

        #Deduct balance
        self.balance -= total

        users[self.username]["balance"] = self.balance

        save_users(users)

        #Create order
        order = {
            "items": [],
            "total": total
        }

        for cart_item in self.cart:

            order["items"].append({
                "item": cart_item["item"],
                "quantity": cart_item["quantity"],
                "price": cart_item["price"]
            })

        #Save order
        self.order_history.append(order)

        #Clear cart
        self.cart.clear()

        self.update_cart_button()

        cart_window.destroy()

        self.root.after(50, lambda: self.popup("Order Successful", f"Your order has been placed!\n\nTotal: ${total:.2f}"))

    #Dashboard
    def create_dashboard(self):

        dashboard = self.tabs.tab("Dashboard")

        #Title
        ctk.CTkLabel(dashboard, text="Student Dashboard", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=20)

        #Account
        ctk.CTkLabel(dashboard, text=f"Account: {self.username}").pack(pady=5)

        #Balance frame
        balance_frame = ctk.CTkFrame(dashboard, fg_color="#343739")
        balance_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(balance_frame, text="Account Balance", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 5))

        self.balance_label = ctk.CTkLabel(balance_frame, text=f"${self.balance:.2f}", font=ctk.CTkFont(size=28, weight="bold"), text_color="#029CFF")
        self.balance_label.pack(pady=5)

        #Add money
        ctk.CTkButton(balance_frame, text="Add Money", command=self.add_money, width=150).pack(pady=(5, 15))

        #Manage account frame
        account_frame = ctk.CTkFrame(dashboard, fg_color="#343739")
        account_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(account_frame, text="Manage Account", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        #Change password
        ctk.CTkButton(account_frame, text="Change Password", command=self.change_password).pack(pady=5)

        #Change username
        ctk.CTkButton(account_frame, text="Change Username", command=self.change_username).pack(pady=5)

        #Order history
        ctk.CTkButton(dashboard, text="View Order History", command=self.view_order_history, width=200).pack(pady=15)

        #Logout
        ctk.CTkButton(dashboard, text="Logout", command=self.logout, width=200, fg_color="#d9534f", hover_color="#a83232").pack(pady=10)

    #Add money
    def add_money(self):

        payment_window = ctk.CTkToplevel(self.root)
        payment_window.title("Add Money")
        payment_window.geometry("400x500")
        payment_window.resizable(False, False)

        #Title
        ctk.CTkLabel(payment_window, text="Add Money", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        #Amount
        amount_entry = ctk.CTkEntry(payment_window, placeholder_text="Amount", width=280)
        amount_entry.pack(pady=10)

        #Card number
        card_entry = ctk.CTkEntry(payment_window, placeholder_text="Card Number", width=280)
        card_entry.pack(pady=10)

        #Expiry
        expiry_entry = ctk.CTkEntry(payment_window, placeholder_text="Expiry (MM/YY)", width=280)
        expiry_entry.pack(pady=10)

        #CVV
        cvv_entry = ctk.CTkEntry(payment_window, placeholder_text="CVV", width=280, show="*")
        cvv_entry.pack(pady=10)

        #Information
        ctk.CTkLabel(payment_window, text="This is a simulated payment.\nCard details are not saved.", text_color="#AAAAAA").pack(pady=10)

        #Process payment
        def process_payment():

            amount = amount_entry.get()
            card = card_entry.get()
            expiry = expiry_entry.get()
            cvv = cvv_entry.get()

            #Check amount
            try:
                amount = float(amount)
            except ValueError:
                self.popup("Payment Failed", "Please enter a valid amount.")
                return

            if amount <= 0:
                self.popup("Payment Failed", "Amount must be greater than $0.")
                return

            #Remove spaces
            card = card.replace(" ", "")

            #Check card number
            if not card.isdigit() or len(card) != 16:
                self.popup("Payment Failed", "Card number must contain 16 digits.")
                return

            #Check expiry
            if len(expiry) != 5 or expiry[2] != "/" or not expiry[:2].isdigit() or not expiry[3:].isdigit():
                self.popup("Payment Failed", "Expiry must be in MM/YY format.")
                return

            month = int(expiry[:2])

            if month < 1 or month > 12:
                self.popup("Payment Failed", "Invalid expiry month.")
                return

            #Check CVV
            if not cvv.isdigit() or len(cvv) != 3:
                self.popup("Payment Failed", "CVV must contain 3 digits.")
                return

            #Add balance
            success = add_balance(self.username, amount)

            if not success:
                self.popup("Payment Failed", "Unable to add money.")
                return

            #Update balance
            self.balance += amount

            self.balance_label.configure(text=f"${self.balance:.2f}")

            #Close window
            payment_window.destroy()

            self.root.after(50, lambda: self.popup("Payment Successful", f"${amount:.2f} has been added to your account."))

        #Process button
        ctk.CTkButton(payment_window, text="Add Money", command=process_payment, width=180).pack(pady=15)

        #Cancel
        ctk.CTkButton(payment_window, text="Cancel", command=payment_window.destroy, width=180, fg_color="#505557", hover_color="#3d4143").pack(pady=5)

    #Change password
    def change_password(self):
        self.popup("Change Password", "Password changing will be added later.")

    #Change username
    def change_username(self):
        self.popup("Change Username", "Username changing will be added later.")

    #Order history
    def view_order_history(self):

        history_window = ctk.CTkToplevel(self.root)
        history_window.title("Order History")
        history_window.geometry("600x500")

        #Title
        ctk.CTkLabel(history_window, text="Order History", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        #No orders
        if not self.order_history:
            ctk.CTkLabel(history_window, text="No previous orders.").pack(pady=30)
            return

        #History frame
        history_frame = ctk.CTkScrollableFrame(history_window, width=500, height=350)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        #Display orders
        for number, order in enumerate(self.order_history, start=1):

            order_frame = ctk.CTkFrame(history_frame, fg_color="#343739")
            order_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(order_frame, text=f"Order #{number}", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=10)

            for item in order["items"]:

                ctk.CTkLabel(order_frame, text=f"{item['item']} x{item['quantity']} - ${item['price']:.2f}").pack(anchor="w", padx=25, pady=2)

            ctk.CTkLabel(order_frame, text=f"Total: ${order['total']:.2f}").pack(anchor="w", padx=15, pady=10)

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