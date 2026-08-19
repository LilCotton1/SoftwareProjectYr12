import customtkinter as ctk

from auth import signup
from auth import login

from student_menu import StudentMenu
from admin_menu import AdminMenu


class LoginWindow:
    def __init__(self):
        # Main Window
        self.root = ctk.CTk()

        self.root.title("Canteen Ordering System")
        self.root.geometry("840x475")
        self.root.configure(fg_color="#23272D")

        # Tabs
        self.tabview = ctk.CTkTabview(self.root, width=500, height=400, fg_color="#23272D", segmented_button_fg_color="#343739", segmented_button_selected_color="#029CFF", segmented_button_selected_hover_color="#1e538d")

        self.tabview.place(x=170, y=30)

        self.tabview.add("Login")
        self.tabview.add("Sign Up")

        # Login frontend
        login_frame = self.tabview.tab("Login")

        ctk.CTkLabel(login_frame, text="Welcome Back", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(35, 25))

        self.loginun = ctk.CTkEntry(login_frame, placeholder_text="Username", width=314, height=40)
        self.loginun.pack(pady=8)

        self.loginpw = ctk.CTkEntry(login_frame, placeholder_text="Password", width=314, height=40, show="*")
        self.loginpw.pack(pady=8)

        ctk.CTkButton(login_frame, text="Login", width=150, height=40, fg_color="#029CFF", hover_color="#1e538d", command=self.login_clicked).pack(pady=20)

        # Sign Up frontend
        signup_frame = self.tabview.tab("Sign Up")

        ctk.CTkLabel(signup_frame, text="Create Account", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(15, 15))


        self.signupun = ctk.CTkEntry(signup_frame, placeholder_text="Username", width=314, height=40)
        self.signupun.pack(pady=5)


        self.signuppw = ctk.CTkEntry(signup_frame, placeholder_text="Password", width=314, height=40, show="*")
        self.signuppw.pack(pady=5)


        self.checkpw = ctk.CTkEntry(signup_frame, placeholder_text="Confirm Password", width=314, height=40, show="*")
        self.checkpw.pack(pady=5)


        self.signup_code = ctk.CTkEntry(signup_frame, placeholder_text="Registration Code", width=314, height=40)
        self.signup_code.pack(pady=5)


        self.show_password = ctk.CTkCheckBox(signup_frame, text="Show Password", command=self.toggle_password)
        self.show_password.pack(pady=8)


        ctk.CTkButton(signup_frame, text="Sign Up", width=150, height=40, fg_color="#029CFF", hover_color="#1e538d", command=self.signup_clicked).pack(pady=10)

        self.root.mainloop()

    # Popups
    def popup(self, title, message):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("350x180")
        popup.resizable(False, False)

        ctk.CTkLabel(popup, text=message, wraplength=300, font=ctk.CTkFont(size=14)).pack(pady=35)

        ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack()

        popup.grab_set()

    # Toggle Password Visibility
    def toggle_password(self):
        if self.show_password.get():
            self.signuppw.configure(show="")
            self.checkpw.configure(show="")
        else:
            self.signuppw.configure(show="*")
            self.checkpw.configure(show="*")

    # Sign Up Backend
    def signup_clicked(self):
        username = self.signupun.get()
        password = self.signuppw.get()
        confirm = self.checkpw.get()
        code = self.signup_code.get()

        correct_code = "CODE123"

        if username == "" or password == "" or confirm == "" or code == "":
            self.popup("Sign Up Failed", "Please fill in all fields.")
            return

        if code != correct_code:
            self.popup("Sign Up Failed", "Incorrect registration code.")
            return

        if password != confirm:
            self.popup("Sign Up Failed", "Passwords do not match.")
            return

        success = signup(username, password)

        if success:
            self.popup("Account Created", "Account created successfully!")

            self.signupun.delete(0, "end")
            self.signuppw.delete(0, "end")
            self.checkpw.delete(0, "end")
            self.signup_code.delete(0, "end")

            self.tabview.set("Login")

        else:

            self.popup("Sign Up Failed", "Username already exists.")

    # Login
    def login_clicked(self):
        username = self.loginun.get()
        password = self.loginpw.get()

        if username == "" or password == "":
            self.popup("Login Failed", "Please enter your username and password.")
            return

        role = login(username, password)

        if role == "student":

            self.root.destroy()
            StudentMenu(username)

        elif role == "admin":

            self.root.destroy()
            AdminMenu()

        else:

            self.popup("Login Failed", "Incorrect username or password.")


if __name__ == "__main__":
    LoginWindow()