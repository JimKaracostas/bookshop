# pages/inventory.py

import tkinter as tk
from tkinter import messagebox, ttk

class InventoryManagementPage:
    def __init__(self, root, callbacks=None):
        self.root = root
        self.callbacks = callbacks or {}
        self.root.title("UC004: Διαχείριση Αποθέματος")
        self.root.geometry("750x650")
        self.root.resizable(True, True)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Διαχείριση Αποθέματος", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        # Φόρμα Εισαγωγής/Επεξεργασίας
        tk.Label(self.frame, text="Barcode: ").grid(row=1, column=0, sticky="e", pady=2)
        self.barcode_entry = tk.Entry(self.frame, width=30)
        self.barcode_entry.grid(row=1, column=1, pady=2)

        tk.Label(self.frame, text="Τίτλος: ").grid(row=2, column=0, sticky="e", pady=2)
        self.title_entry = tk.Entry(self.frame, width=30)
        self.title_entry.grid(row=2, column=1, pady=2)

        tk.Label(self.frame, text="Συγγραφέας: ").grid(row=3, column=0, sticky="e", pady=2)
        self.author_entry = tk.Entry(self.frame, width=30)
        self.author_entry.grid(row=3, column=1, pady=2)

        tk.Label(self.frame, text="Κατηγορία: ").grid(row=4, column=0, sticky="e", pady=2)
        self.cat_entry = tk.Entry(self.frame, width=30)
        self.cat_entry.grid(row=4, column=1, pady=2)

        tk.Label(self.frame, text="Τιμή (€): ").grid(row=5, column=0, sticky="e", pady=2)
        self.price_entry = tk.Entry(self.frame, width=30)
        self.price_entry.grid(row=5, column=1, pady=2)

        tk.Label(self.frame, text="Απόθεμα: ").grid(row=6, column=0, sticky="e", pady=2)
        self.stock_entry = tk.Entry(self.frame, width=30)
        self.stock_entry.grid(row=6, column=1, pady=2)

        # Κουμπιά CRUD
        btn_frame = tk.Frame(self.frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Προσθήκη", width=12, bg="#5cb85c", fg="white", command=self.add_book).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Ενημέρωση Τιμής/Αποθέματος", width=25, bg="#0275d8", fg="white", command=self.update_book).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Διαγραφή", width=12, bg="#d9534f", fg="white", command=self.delete_book).pack(side="left", padx=5)

        # Πίνακας Βιβλίων
        cols = ("id", "barcode", "title", "price", "stock")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=10)
        for c in cols: self.tree.heading(c, text=c.capitalize())
        self.tree.column("id", width=30)
        self.tree.column("price", width=60)
        self.tree.column("stock", width=60)
        self.tree.grid(row=8, column=0, columnspan=2, pady=10, sticky="nsew")
        self.tree.bind('<ButtonRelease-1>', self.on_select)

        tk.Button(self.frame, text="Πίσω στο Μενού", width=20, command=self.go_back).grid(row=9, column=0, columnspan=2, pady=10)

    def add_book(self):
        if 'add' in self.callbacks:
            self.callbacks['add'](
                self.barcode_entry.get().strip(), self.title_entry.get().strip(),
                self.author_entry.get().strip(), self.cat_entry.get().strip(),
                self.price_entry.get().strip(), self.stock_entry.get().strip()
            )
            self.clear_inputs()

    def update_book(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο από τη λίστα.")
            return
        book_id = self.tree.item(sel[0])['values'][0]
        if 'update' in self.callbacks:
            self.callbacks['update'](book_id, self.price_entry.get().strip(), self.stock_entry.get().strip())
            self.clear_inputs()

    def delete_book(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο για διαγραφή.")
            return
        book_id = self.tree.item(sel[0])['values'][0]
        if 'delete' in self.callbacks:
            self.callbacks['delete'](book_id)
            self.clear_inputs()

    def go_back(self):
        if 'back' in self.callbacks: self.callbacks['back']()

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        values = self.tree.item(sel[0])['values']
        self.clear_inputs()
        self.barcode_entry.insert(0, values[1])
        self.title_entry.insert(0, values[2])
        self.price_entry.insert(0, values[3])
        self.stock_entry.insert(0, values[4])

    def clear_inputs(self):
        for entry in (self.barcode_entry, self.title_entry, self.author_entry, self.cat_entry, self.price_entry, self.stock_entry):
            entry.delete(0, tk.END)

    def populate_tree(self, books):
        for row in self.tree.get_children(): self.tree.delete(row)
        for b in books:
            self.tree.insert("", tk.END, values=(b.get("id"), b.get("barcode", ""), b.get("title", ""), b.get("price", 0), b.get("stock", 0)))