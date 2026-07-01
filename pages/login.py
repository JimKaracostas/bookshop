# pages/login.py

import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, root, login_callback):
        self.root = root
        self.root.title("Σύνδεση - Σύστημα Βιβλιοπωλείου")
        self.root.geometry("400x300")
        self.root.resizable(True, True) # Πλέον resizable!

        self.login_callback = login_callback

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(expand=True)

        self.title_label = tk.Label(self.frame, text="Καλώς ήρθατε", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.username_label = tk.Label(self.frame, text="Όνομα Χρήστη:", font=("Helvetica", 10))
        self.username_label.grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(self.frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=5, padx=5)

        self.password_label = tk.Label(self.frame, text="Κωδικός:", font=("Helvetica", 10))
        self.password_label.grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(self.frame, width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5)

        self.role_label = tk.Label(self.frame, text="Ρόλος:", font=("Helvetica", 10))
        self.role_label.grid(row=3, column=0, sticky="e", pady=5)
        self.role_var = tk.StringVar(value="Πωλητής")
        self.role_menu = tk.OptionMenu(self.frame, self.role_var, "Πωλητής", "Διαχειριστής", "Πελάτης")
        self.role_menu.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        self.login_button = tk.Button(self.frame, text="Σύνδεση", width=15, command=self.on_login)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.root.bind('<Return>', lambda event: self.on_login())

    def on_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Προειδοποίηση", "Παρακαλώ συμπληρώστε όλα τα πεδία.")
            return

        role = self.role_var.get()
        self.login_callback(username, password, role)

    def show_error(self, message):
        messagebox.showerror("Σφάλμα", message)