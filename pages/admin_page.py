# pages/admin_page.py

import tkinter as tk

class AdminPage:
    def __init__(self, root, current_user, callbacks):
        self.root = root
        self.current_user = current_user
        self.callbacks = callbacks
        
        self.root.title("Πάνελ Διαχειριστή - Σύστημα Διαχείρισης Βιβλιοπωλείου")
        self.root.geometry("600x500")
        
        self.frame = tk.Frame(self.root, padx=30, pady=30)
        self.frame.pack(fill="both", expand=True)
        
        welcome_msg = f"Καλώς ήρθατε, {self.current_user.get('username', 'Admin')}"
        self.title_label = tk.Label(self.frame, text=welcome_msg, font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=20)
        
        # Κουμπιά Μενού
        self.btn_inventory = tk.Button(self.frame, text="Διαχείριση Αποθέματος (UC004)", 
                                      font=("Helvetica", 12), width=35, height=2,
                                      command=self.callbacks.get('show_inventory'))
        self.btn_inventory.pack(pady=10)
        
        self.btn_staff = tk.Button(self.frame, text="Διαχείριση Προσωπικού (UC005)", 
                                   font=("Helvetica", 12), width=35, height=2,
                                   command=self.callbacks.get('show_staff'))
        self.btn_staff.pack(pady=10)
        
        self.btn_logout = tk.Button(self.frame, text="Αποσύνδεση", 
                                    font=("Helvetica", 12, "bold"), width=35, height=2,
                                    bg="#d9534f", fg="white",
                                    command=self.callbacks.get('logout'))
        self.btn_logout.pack(pady=20)
