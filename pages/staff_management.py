# pages/staff_management.py

import tkinter as tk
from tkinter import messagebox, ttk

class StaffManagementPage:
    def __init__(self, root, callbacks=None):
        self.root = root
        self.callbacks = callbacks or {}
        self.root.title("UC005: Διαχείριση Προσωπικού")
        self.root.geometry("650x550")
        self.root.resizable(True, True)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Διαχείριση Προσωπικού", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(self.frame, text="Username Υπαλλήλου: ", font=("Helvetica", 10)).grid(row=1, column=0, pady=5, sticky="e")
        self.emp_username_entry = tk.Entry(self.frame, width=25)
        self.emp_username_entry.grid(row=1, column=1, pady=5, sticky="w")

        tk.Label(self.frame, text="Κωδικός Πρόσβασης: ", font=("Helvetica", 10)).grid(row=2, column=0, pady=5, sticky="e")
        self.emp_password_entry = tk.Entry(self.frame, width=25)
        self.emp_password_entry.grid(row=2, column=1, pady=5, sticky="w")

        # Κουμπιά ενεργειών
        btn_frame = tk.Frame(self.frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Πρόσληψη (Νέος Χρήστης)", bg="#5cb85c", fg="white", width=25, command=self.hire_staff).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Απόλυση (Απενεργοποίηση)", bg="#d9534f", fg="white", width=25, command=self.fire_staff).pack(side="left", padx=10)

        # Λίστα
        cols = ("id", "username", "role", "active")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for c in cols: self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=40)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10, sticky="nsew")
        self.tree.bind('<ButtonRelease-1>', self.on_select)

        tk.Button(self.frame, text="Πίσω στο Μενού", width=20, command=self.go_back).grid(row=6, column=0, columnspan=2, pady=10)

    def hire_staff(self):
        username = self.emp_username_entry.get().strip()
        password = self.emp_password_entry.get().strip()
        role = "SELLER"
        
        if not username or not password:
            messagebox.showwarning("Προσοχή", "Το Username και ο Κωδικός είναι υποχρεωτικά!")
            return

        if 'add' in self.callbacks:
            self.callbacks['add'](username, password, role)
            self.clear_inputs()

    def fire_staff(self):
        username = self.emp_username_entry.get().strip()
        if not username:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ή πληκτρολογήστε ένα Username.")
            return

        if 'toggle' in self.callbacks:
            self.callbacks['toggle'](username)
            self.clear_inputs()

    def populate_tree(self, employees):
        for row in self.tree.get_children(): self.tree.delete(row)
        for e in employees:
            self.tree.insert("", tk.END, values=(e.get("id"), e.get("username"), e.get("role"), e.get("is_active")))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        values = self.tree.item(sel[0])['values']
        self.clear_inputs()
        self.emp_username_entry.insert(0, values[1])

    def clear_inputs(self):
        self.emp_username_entry.delete(0, tk.END)
        self.emp_password_entry.delete(0, tk.END)

    def go_back(self):
        if 'back' in self.callbacks: self.callbacks['back']()