# pages/search.py

import tkinter as tk
from tkinter import messagebox

class SearchView:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        
        # Ενσωμάτωση λογικής από το codes/test.py (CustomerWindow)
        
        if hasattr(self.root, 'title'):
            self.root.title("Αναζήτηση & Διαχείριση Βιβλίων")
        if hasattr(self.root, 'geometry'):
            self.root.geometry("600x550")
        
        self.books = [] # Σε ένα κανονικό app αυτό θα ερχόταν από τη βάση

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Αναζήτηση Βιβλίου (UC001)",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        search_frame = tk.Frame(self.frame)
        search_frame.pack(pady=5)
        
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="Προσθήκη",
            command=self.add_book
        ).pack(side="left", padx=2)

        tk.Button(
            search_frame,
            text="Αναζήτηση",
            command=self.search_book
        ).pack(side="left", padx=2)

        self.book_list = tk.Listbox(self.frame, width=60, height=12)
        self.book_list.pack(pady=10)

        action_frame = tk.Frame(self.frame)
        action_frame.pack(pady=5)

        tk.Button(
            action_frame,
            text="Αγορά",
            width=15,
            command=self.buy_book
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Δανεισμός",
            width=15,
            command=self.borrow_book
        ).pack(side="left", padx=5)
        
        tk.Button(
            action_frame,
            text="Χρήση Book Pass",
            width=15,
            command=self.use_bookpass
        ).pack(side="left", padx=5)

        if self.back_callback:
            tk.Button(
                self.frame,
                text="Επιστροφή",
                bg="#5bc0de",
                command=self.back_callback
            ).pack(pady=20)

    def add_book(self):
        book = self.search_entry.get()
        if book:
            self.books.append(book)
            self.book_list.insert(tk.END, book)
            self.search_entry.delete(0, tk.END)

    def search_book(self):
        word = self.search_entry.get().lower()
        self.book_list.delete(0, tk.END)
        found = False
        for book in self.books:
            if word in book.lower():
                self.book_list.insert(tk.END, book)
                found = True
        if not found:
            messagebox.showinfo("Αναζήτηση", "Δεν βρέθηκαν βιβλία")

    def buy_book(self):
        selected = self.book_list.curselection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο")
            return
        book = self.book_list.get(selected)
        messagebox.showinfo("Αγορά", f"Αγοράστηκε το βιβλίο: {book}")

    def borrow_book(self):
        selected = self.book_list.curselection()
        if not selected:
            messagebox.showwarning("Προσοχή", "Επιλέξτε ένα βιβλίο")
            return
        book = self.book_list.get(selected)
        messagebox.showinfo("Δανεισμός", f"Δανείστηκες το βιβλίο: {book}")

    def use_bookpass(self):
        messagebox.showinfo("Book Pass", "Το Book Pass χρησιμοποιήθηκε επιτυχώς.")
