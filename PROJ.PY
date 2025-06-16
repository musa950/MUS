import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re


class BankingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mock Banking App")
        self.root.geometry("400x600")
        self.root.configure(bg="#1a1a2e")

        # Mock user database
        self.users = {
            "lappiabockarie@gmail.com": {
                "password": "Shadow1$",
                "first_name": "Lappia",
                "last_name": "Bockarie",
                "username": "Lappia001",
                "phone": "+232 76 940 408",
                "dob": "2022-02-22",
                "balance": 15000.00,
                "income": 3000.00,
                "expenses": 1200.00
            }
        }

        self.current_user = None
        self.transactions = [
            {"name": "Esther Howard", "category": "Shopping", "amount": -300.00, "date": "13 Feb 2022, 7:30PM"},
            {"name": "Wade Warren", "category": "Medicine", "amount": -100.50, "date": "12 Feb 2022, 9:20AM"},
            {"name": "Kristin Watson", "category": "Sport", "amount": -110.50, "date": "10 Feb 2022, 1:10PM"},
            {"name": "Jacob Jones", "category": "Shopping", "amount": -250.00, "date": "7 Feb 2022, 8:10AM"},
            {"name": "Ralph Edwards", "category": "Travel", "amount": -499.00, "date": "4 Feb 2022, 6:00PM"},
            {"name": "Brooklyn Simmons", "category": "Salon", "amount": -50.99, "date": "4 Feb 2022, 3:00PM"}
        ]

        self.show_login_screen()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display the login screen"""
        self.clear_window()
        self.root.title("Login - Banking App")

        # Main frame
        main_frame = tk.Frame(self.root, bg="#1a1a2e")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Welcome Back",
                               font=("Arial", 24, "bold"), fg="white", bg="#1a1a2e")
        title_label.pack(pady=20)

        # Email field
        tk.Label(main_frame, text="Email Address", font=("Arial", 12),
                 fg="white", bg="#1a1a2e").pack(anchor="w", pady=(10, 5))

        self.email_entry = tk.Entry(main_frame, font=("Arial", 12), width=30,
                                    bg="#2d2d44", fg="white", relief="flat", bd=10)
        self.email_entry.pack(pady=(0, 10), ipady=8)
        self.email_entry.insert(0, "lappiabockarie@gmail.com")  # Pre-filled for demo

        # Password field
        tk.Label(main_frame, text="Password", font=("Arial", 12),
                 fg="white", bg="#1a1a2e").pack(anchor="w", pady=(10, 5))

        self.password_entry = tk.Entry(main_frame, font=("Arial", 12), width=30,
                                       show="*", bg="#2d2d44", fg="white", relief="flat", bd=10)
        self.password_entry.pack(pady=(0, 10), ipady=8)
        self.password_entry.insert(0, "Shadow1$")  # Pre-filled for demo

        # Sign In button
        signin_btn = tk.Button(main_frame, text="Sign In", font=("Arial", 14, "bold"),
                               bg="#4a69bd", fg="white", relief="flat", width=25,
                               command=self.sign_in)
        signin_btn.pack(pady=20, ipady=10)

        # Sign Up button
        signup_btn = tk.Button(main_frame, text="Sign Up", font=("Arial", 12),
                               bg="#2d2d44", fg="white", relief="flat", width=25,
                               command=self.show_signup_screen)
        signup_btn.pack(pady=10, ipady=8)

        # Forgot password
        forgot_label = tk.Label(main_frame, text="Forgot Password?",
                                font=("Arial", 10), fg="#4a69bd", bg="#1a1a2e", cursor="hand2")
        forgot_label.pack(pady=10)

    def sign_in(self):
        """Handle sign in process"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if email in self.users and self.users[email]["password"] == password:
            self.current_user = email
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    def show_signup_screen(self):
        """Display the sign up screen"""
        self.clear_window()
        self.root.title("Sign Up - Banking App")

        # Scrollable frame
        canvas = tk.Canvas(self.root, bg="#1a1a2e")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Title
        title_label = tk.Label(scrollable_frame, text="Sign Up",
                               font=("Arial", 24, "bold"), fg="white", bg="#1a1a2e")
        title_label.pack(pady=20)

        # Form fields
        fields = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("Date of Birth (YYYY-MM-DD)", "dob"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password")
        ]

        self.signup_entries = {}

        for label_text, field_name in fields:
            tk.Label(scrollable_frame, text=label_text, font=("Arial", 12),
                     fg="white", bg="#1a1a2e").pack(anchor="w", padx=20, pady=(10, 5))

            show_char = "*" if "password" in field_name else None
            entry = tk.Entry(scrollable_frame, font=("Arial", 12), width=30,
                             show=show_char, bg="#2d2d44", fg="white", relief="flat", bd=10)
            entry.pack(padx=20, pady=(0, 10), ipady=8)
            self.signup_entries[field_name] = entry

        # Sign Up button
        signup_btn = tk.Button(scrollable_frame, text="Create Account",
                               font=("Arial", 14, "bold"), bg="#4a69bd", fg="white",
                               relief="flat", width=25, command=self.create_account)
        signup_btn.pack(pady=20, ipady=10)

        # Back to login
        back_btn = tk.Button(scrollable_frame, text="Back to Login",
                             font=("Arial", 12), bg="#2d2d44", fg="white",
                             relief="flat", width=25, command=self.show_login_screen)
        back_btn.pack(pady=10, ipady=8)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_account(self):
        """Handle account creation"""
        # Get all form data
        data = {}
        for field, entry in self.signup_entries.items():
            data[field] = entry.get().strip()

        # Validation
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill all fields!")
            return

        if data["password"] != data["confirm_password"]:
            messagebox.showerror("Error", "Passwords don't match!")
            return

        if data["email"] in self.users:
            messagebox.showerror("Error", "Email already exists!")
            return

        # Create new user
        self.users[data["email"]] = {
            "password": data["password"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "username": data["first_name"][:3] + "001",
            "phone": data["phone"],
            "dob": data["dob"],
            "balance": 1000.00,  # Starting balance
            "income": 0.00,
            "expenses": 0.00
        }

        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()

    def show_dashboard(self):
        """Display the main dashboard"""
        self.clear_window()
        self.root.title("Dashboard - Banking App")
        self.root.geometry("500x700")

        user_data = self.users[self.current_user]

        # Header frame
        header_frame = tk.Frame(self.root, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=20, pady=10)

        # Greeting
        greeting = tk.Label(header_frame, text=f"Good morning {user_data['first_name']}!",
                            font=("Arial", 18, "bold"), fg="white", bg="#1a1a2e")
        greeting.pack(anchor="w")

        # Balance card
        balance_frame = tk.Frame(self.root, bg="#4a69bd", relief="raised", bd=2)
        balance_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(balance_frame, text="Your total balance", font=("Arial", 12),
                 fg="white", bg="#4a69bd").pack(pady=(10, 5))

        balance_label = tk.Label(balance_frame, text=f"${user_data['balance']:,.2f}",
                                 font=("Arial", 28, "bold"), fg="white", bg="#4a69bd")
        balance_label.pack(pady=(0, 10))

        # Income/Expense row
        stats_frame = tk.Frame(self.root, bg="#1a1a2e")
        stats_frame.pack(fill="x", padx=20, pady=10)

        # Income
        income_frame = tk.Frame(stats_frame, bg="#2d2d44")
        income_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(income_frame, text="Income", font=("Arial", 12),
                 fg="white", bg="#2d2d44").pack(pady=5)
        tk.Label(income_frame, text=f"${user_data['income']:,.2f}",
                 font=("Arial", 16, "bold"), fg="#2ecc71", bg="#2d2d44").pack(pady=5)

        # Expenses
        expense_frame = tk.Frame(stats_frame, bg="#2d2d44")
        expense_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        tk.Label(expense_frame, text="Expenses", font=("Arial", 12),
                 fg="white", bg="#2d2d44").pack(pady=5)
        tk.Label(expense_frame, text=f"${user_data['expenses']:,.2f}",
                 font=("Arial", 16, "bold"), fg="#e74c3c", bg="#2d2d44").pack(pady=5)

        # Action buttons
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(fill="x", padx=20, pady=10)

        transfer_btn = tk.Button(button_frame, text="Transfer", font=("Arial", 12, "bold"),
                                 bg="#4a69bd", fg="white", relief="flat", width=12,
                                 command=self.show_transfer_screen)
        transfer_btn.pack(side="left", padx=(0, 10), ipady=8)

        profile_btn = tk.Button(button_frame, text="Profile", font=("Arial", 12, "bold"),
                                bg="#2d2d44", fg="white", relief="flat", width=12,
                                command=self.show_profile_screen)
        profile_btn.pack(side="left", padx=10, ipady=8)

        signout_btn = tk.Button(button_frame, text="Sign Out", font=("Arial", 12, "bold"),
                                bg="#e74c3c", fg="white", relief="flat", width=12,
                                command=self.sign_out)
        signout_btn.pack(side="right", ipady=8)

        # Transactions section
        trans_label = tk.Label(self.root, text="Recent Transactions",
                               font=("Arial", 16, "bold"), fg="white", bg="#1a1a2e")
        trans_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Transactions list
        trans_frame = tk.Frame(self.root, bg="#1a1a2e")
        trans_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create scrollable transaction list
        canvas = tk.Canvas(trans_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(trans_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add transactions
        for transaction in self.transactions:
            self.create_transaction_item(scrollable_frame, transaction)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_transaction_item(self, parent, transaction):
        """Create a transaction list item"""
        item_frame = tk.Frame(parent, bg="#2d2d44", relief="raised", bd=1)
        item_frame.pack(fill="x", pady=2)

        # Left side - name and category
        left_frame = tk.Frame(item_frame, bg="#2d2d44")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        name_label = tk.Label(left_frame, text=transaction["name"],
                              font=("Arial", 12, "bold"), fg="white", bg="#2d2d44")
        name_label.pack(anchor="w")

        category_label = tk.Label(left_frame, text=transaction["category"],
                                  font=("Arial", 10), fg="#bdc3c7", bg="#2d2d44")
        category_label.pack(anchor="w")

        date_label = tk.Label(left_frame, text=transaction["date"],
                              font=("Arial", 9), fg="#95a5a6", bg="#2d2d44")
        date_label.pack(anchor="w")

        # Right side - amount
        amount_color = "#e74c3c" if transaction["amount"] < 0 else "#2ecc71"
        amount_text = f"${transaction['amount']:,.2f}"

        amount_label = tk.Label(item_frame, text=amount_text,
                                font=("Arial", 12, "bold"), fg=amount_color, bg="#2d2d44")
        amount_label.pack(side="right", padx=10, pady=8)

    def show_transfer_screen(self):
        """Display the transfer money screen"""
        self.clear_window()
        self.root.title("Transfer Money - Banking App")
        self.root.geometry("400x500")

        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=20, pady=20)

        title_label = tk.Label(header_frame, text="Transfer Money",
                               font=("Arial", 20, "bold"), fg="white", bg="#1a1a2e")
        title_label.pack()

        # Form
        form_frame = tk.Frame(self.root, bg="#1a1a2e")
        form_frame.pack(fill="both", expand=True, padx=20)

        # Recipient
        tk.Label(form_frame, text="To", font=("Arial", 12),
                 fg="white", bg="#1a1a2e").pack(anchor="w", pady=(10, 5))

        self.recipient_entry = tk.Entry(form_frame, font=("Arial", 12), width=30,
                                        bg="#2d2d44", fg="white", relief="flat", bd=10)
        self.recipient_entry.pack(pady=(0, 10), ipady=8)

        # Amount
        tk.Label(form_frame, text="Enter Amount", font=("Arial", 12),
                 fg="white", bg="#1a1a2e").pack(anchor="w", pady=(10, 5))

        self.amount_entry = tk.Entry(form_frame, font=("Arial", 12), width=30,
                                     bg="#2d2d44", fg="white", relief="flat", bd=10)
        self.amount_entry.pack(pady=(0, 10), ipady=8)

        # Balance display
        user_data = self.users[self.current_user]
        balance_label = tk.Label(form_frame, text=f"Available Balance: ${user_data['balance']:,.2f}",
                                 font=("Arial", 10), fg="#bdc3c7", bg="#1a1a2e")
        balance_label.pack(pady=10)

        # Transfer button
        transfer_btn = tk.Button(form_frame, text="Transfer Now",
                                 font=("Arial", 14, "bold"), bg="#4a69bd", fg="white",
                                 relief="flat", width=25, command=self.process_transfer)
        transfer_btn.pack(pady=20, ipady=10)

        # Back button
        back_btn = tk.Button(form_frame, text="Back to Dashboard",
                             font=("Arial", 12), bg="#2d2d44", fg="white",
                             relief="flat", width=25, command=self.show_dashboard)
        back_btn.pack(pady=10, ipady=8)

    def process_transfer(self):
        """Handle money transfer"""
        recipient = self.recipient_entry.get().strip()
        amount_str = self.amount_entry.get().strip()

        if not recipient or not amount_str:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")
            return

        user_data = self.users[self.current_user]
        if amount > user_data['balance']:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        # Process transfer (mock)
        user_data['balance'] -= amount
        user_data['expenses'] += amount

        # Add to transactions
        new_transaction = {
            "name": recipient,
            "category": "Transfer",
            "amount": -amount,
            "date": datetime.now().strftime("%d %b %Y, %I:%M%p")
        }
        self.transactions.insert(0, new_transaction)

        messagebox.showinfo("Success", f"Successfully sent ${amount:.2f} to {recipient}")
        self.show_dashboard()

    def show_profile_screen(self):
        """Display the profile screen"""
        self.clear_window()
        self.root.title("Profile - Banking App")
        self.root.geometry("400x600")

        user_data = self.users[self.current_user]

        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a2e")
        header_frame.pack(fill="x", padx=20, pady=20)

        title_label = tk.Label(header_frame, text="Profile",
                               font=("Arial", 20, "bold"), fg="white", bg="#1a1a2e")
        title_label.pack()

        # Profile info
        info_frame = tk.Frame(self.root, bg="#1a1a2e")
        info_frame.pack(fill="both", expand=True, padx=20)

        profile_fields = [
            ("Username", user_data['username']),
            ("First Name", user_data['first_name']),
            ("Last Name", user_data['last_name']),
            ("Email", self.current_user),
            ("Phone", user_data['phone']),
            ("Date of Birth", user_data['dob'])
        ]

        for label, value in profile_fields:
            # Label
            tk.Label(info_frame, text=label, font=("Arial", 12, "bold"),
                     fg="white", bg="#1a1a2e").pack(anchor="w", pady=(15, 5))

            # Value in a styled frame
            value_frame = tk.Frame(info_frame, bg="#2d2d44", relief="raised", bd=1)
            value_frame.pack(fill="x", pady=(0, 5))

            tk.Label(value_frame, text=value, font=("Arial", 12),
                     fg="#bdc3c7", bg="#2d2d44").pack(anchor="w", padx=10, pady=8)

        # Back button
        back_btn = tk.Button(info_frame, text="Back to Dashboard",
                             font=("Arial", 12, "bold"), bg="#4a69bd", fg="white",
                             relief="flat", width=25, command=self.show_dashboard)
        back_btn.pack(pady=30, ipady=10)

    def sign_out(self):
        """Handle sign out"""
        self.current_user = None
        self.root.geometry("400x600")
        self.show_login_screen()

    def run(self):
        """Start the application"""
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = BankingApp()
    app.run()