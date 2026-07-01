# pages/sale.py

import tkinter as tk
from tkinter import ttk, messagebox
from supabase import create_client, Client

SUPABASE_URL = "https://fhewndsaybrqvkmmfzir.supabase.co/"
SUPABASE_KEY = "sb_publishable_qqHWxwErRpou7wVGv911_w_ZYuOJKJ6"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Σφάλμα Supabase: {e}")

class SellerPage:
    def __init__(self, root, logout_callback=None):
        self.root = root
        self.logout_callback = logout_callback
        self.root.title("Πάνελ Πωλητή - Σύστημα Διαχείρισης Βιβλιοπωλείου")
        self.root.geometry("850x650")
        self.root.resizable(True, True)

        self.cart_items = []
        self.total_price = 0.0

        self.header_label = tk.Label(self.root, text="Περιβάλλον Πωλητή", font=("Helvetica", 16, "bold"))
        self.header_label.pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=20, pady=10)

        # Αναζήτηση & Αγορά/Δανεισμός (UC001, UC007, UC009)
        self.tab_search = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text="Αναζήτηση & Λειτουργίες (UC001/007/009)")
        from pages.search import SearchView
        self.search_view = SearchView(self.tab_search)

        # Διαχείριση Επιστροφών (UC003)
        self.tab_returns = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_returns, text="Επιστροφές (UC003)")
        self.setup_returns_tab()

        self.tab_sales = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_sales, text="Πώληση (UC002)")
        self.setup_sales_tab()

        self.logout_button = tk.Button(self.root, text="Αποσύνδεση", font=("Helvetica", 10, "bold"), 
                                       bg="#d9534f", fg="white", width=20, command=self.on_logout)
        self.logout_button.pack(pady=10)
 
    def setup_sales_tab(self):
        top_frame = tk.Frame(self.tab_sales, pady=15)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Barcode Βιβλίου:").pack(side="left", padx=10)
        self.sale_barcode_entry = tk.Entry(top_frame, width=30)
        self.sale_barcode_entry.pack(side="left", padx=10)
        tk.Button(top_frame, text="Προσθήκη", bg="#f0ad4e", command=self.add_to_cart).pack(side="left", padx=10)

        self.cart_listbox = tk.Listbox(self.tab_sales, width=80, height=12, font=("Courier", 10))
        self.cart_listbox.pack(padx=15, pady=10, expand=True, fill="both")

        self.total_label = tk.Label(self.tab_sales, text="Σύνολο: 0.00 €", font=("Helvetica", 14, "bold"), fg="#d9534f")
        self.total_label.pack(pady=5)

        tk.Button(self.tab_sales, text="Ολοκλήρωση Πώλησης & Απόδειξη", bg="#5cb85c", fg="white", font=("Helvetica", 11, "bold"), command=self.complete_sale).pack(pady=10)

    def add_to_cart(self):
        barcode = self.sale_barcode_entry.get().strip()
        if not barcode: return
        try:
            response = supabase.table("books").select("*").eq("barcode", barcode).execute()
            books = response.data
            if not books:
                messagebox.showerror("Σφάλμα", "Λάθος Barcode.")
                return
            
            book = books[0]
            if int(book.get("stock", 0)) <= 0:
                messagebox.showwarning("Εξαντλήθηκε", "Αυτό το βιβλίο δεν υπάρχει σε απόθεμα!")
                return

            price = float(book.get("price", 0))
            self.cart_items.append(book)
            self.total_price += price

            self.cart_listbox.insert(tk.END, f"[{book.get('barcode')}] {book.get('title')} - {price} €")
            self.total_label.config(text=f"Σύνολο: {self.total_price:.2f} €")
            self.sale_barcode_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Πρόβλημα:\n{e}")

    def complete_sale(self):
        if not self.cart_items: return
        try:
            for item in self.cart_items:
                new_stock = int(item.get("stock", 1)) - 1
                supabase.table("books").update({"stock": new_stock}).eq("id", item.get("id")).execute()
            
            sale_response = supabase.table("sales").insert({"total_amount": self.total_price}).execute()
            new_sale_id = sale_response.data[0]["id"]

            for item in self.cart_items:
                supabase.table("sale_items").insert({
                    "sale_id": new_sale_id,       
                    "book_id": item.get("id"),    
                    "quantity": 1,               
                    "price_at_time": item.get("price") 
                }).execute()
            
            messagebox.showinfo("Επιτυχία", f"Η πώληση ολοκληρώθηκε!\nΣυνολικό ποσό: {self.total_price:.2f} €")
            self.cart_items.clear()
            self.cart_listbox.delete(0, tk.END)
            self.total_price = 0.0
            self.total_label.config(text="Σύνολο: 0.00 €")
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Η πώληση απέτυχε:\n{e}")

    def setup_returns_tab(self):
        ret_frame = tk.Frame(self.tab_returns, pady=30)
        ret_frame.pack()
        tk.Label(ret_frame, text="Barcode Βιβλίου προς Επιστροφή:", font=("Helvetica", 11)).pack(pady=10)
        self.return_entry = tk.Entry(ret_frame, width=30, font=("Helvetica", 11))
        self.return_entry.pack(pady=10)
        tk.Button(ret_frame, text="Ακύρωση Πώλησης / Επιστροφή", bg="#f0ad4e", font=("Helvetica", 11, "bold"), command=self.process_return).pack(pady=20)

    def process_return(self):
        barcode = self.return_entry.get().strip()
        if not barcode: return
        try:
            response = supabase.table("books").select("*").eq("barcode", barcode).execute()
            books = response.data
            if not books:
                messagebox.showerror("Σφάλμα", "Το βιβλίο δεν υπάρχει στη βάση.")
                return

            book = books[0]
            new_stock = int(book.get("stock", 0)) + 1
            supabase.table("books").update({"stock": new_stock}).eq("id", book.get("id")).execute()
            messagebox.showinfo("Επιτυχία", "Η επιστροφή καταγράφηκε και το απόθεμα αυξήθηκε.")
            self.return_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Πρόβλημα σύνδεσης:\n{e}")

    def on_logout(self):
        if len(self.cart_items) > 0:
            confirm = messagebox.askyesno("Προειδοποίηση", "Έχετε βιβλία στο ταμείο.\nΝα αποσυνδεθείτε;")
            if not confirm: return
        
        if self.logout_callback:
            self.logout_callback()
        else:
            self.root.destroy()