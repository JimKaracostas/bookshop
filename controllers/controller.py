# controllers/controller.py

import tkinter as tk
from tkinter import messagebox
from supabase import create_client, Client

from pages.login import LoginView
from pages.inventory import InventoryManagementPage
from pages.staff_management import StaffManagementPage
from pages.sale import SellerPage

# Προσπαθούμε να κάνουμε import το AdminPage
try:
    from pages.admin_page import AdminPage
except ImportError:
    AdminPage = None

SUPABASE_URL = "https://fhewndsaybrqvkmmfzir.supabase.co/"
SUPABASE_KEY = "sb_publishable_qqHWxwErRpou7wVGv911_w_ZYuOJKJ6"

class MainController:
    def __init__(self, root):
        self.root = root
        self.current_user = None

        try:
            self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            messagebox.showerror("Σφάλμα Βάσης", f"Αποτυχία σύνδεσης με το Supabase:\n{e}")
            self.supabase = None

        self.show_login()

    def clear_window(self):
        self.root.unbind('<Return>')
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- UC000: LOGIN ---
    def show_login(self):
        self.clear_window()
        self.login_view = LoginView(self.root, self.handle_login)

    def handle_login(self, username, password, role_choice):
        # UC000: Σύνδεση Χρήστη (LOGIN)

        # Bypass για το demo (UC000 Alternative Paths)
        if (username == "admin" and password == "admin" and role_choice == "Διαχειριστής") or \
           (username == "seller" and password == "seller" and role_choice == "Πωλητής") or \
           (role_choice == "Πελάτης"):
            
            self.current_user = {"username": username, "role": role_choice}
            if role_choice == "Διαχειριστής":
                self.show_admin_dashboard()
            elif role_choice == "Πωλητής":
                self.show_seller_dashboard()
            else:
                self.show_customer_panel()
            return

        if not self.supabase:
            self.login_view.show_error("Δεν υπάρχει σύνδεση με τη βάση δεδομένων.")
            return

        try:
            response = self.supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
            users = response.data

            if users:
                user = users[0]
                if not user.get("is_active", True):
                    self.login_view.show_error("Ο λογαριασμός σας έχει απενεργοποιηθεί.")
                    return

                db_role = str(user.get("role", "")).upper()
                mapped_role = "Πωλητής" if db_role in ["SELLER", "ΠΩΛΗΤΗΣ"] else "Διαχειριστής"
                
                if mapped_role != role_choice:
                    self.login_view.show_error(f"Ο ρόλος '{role_choice}' δεν αντιστοιχεί στο λογαριασμό.")
                    return

                self.current_user = user
                messagebox.showinfo("Επιτυχής Σύνδεση", f"Καλώς ήρθες, {username}!")

                if mapped_role == "Πωλητής":
                    self.show_seller_dashboard()
                else:
                    self.show_admin_dashboard()
            else:
                self.login_view.show_error("Λάθος όνομα χρήστη ή κωδικός!")
        except Exception as e:
            self.login_view.show_error(f"Πρόβλημα επικοινωνίας με τη βάση:\n{e}")

    def show_customer_panel(self):
        # UC009, UC007
        self.clear_window()
        from pages.search import SearchView
        self.customer_view = SearchView(self.root, back_callback=self.handle_logout)

    # --- UC100: LOGOUT ---
    def handle_logout(self):
        self.current_user = None
        self.show_login()

    # --- ΠΩΛΗΤΗΣ ---
    def show_seller_dashboard(self):
        self.clear_window()
        self.seller_view = SellerPage(self.root, logout_callback=self.handle_logout)

    # --- ΔΙΑΧΕΙΡΙΣΤΗΣ ---
    def show_admin_dashboard(self):
        self.clear_window()
        
        callbacks = {
            'logout': self.handle_logout,
            'show_inventory': self.show_inventory,
            'show_staff': self.show_staff
        }

        if AdminPage:
            try:
                self.admin_view = AdminPage(self.root, self.current_user, callbacks)
            except Exception as e:
                messagebox.showinfo("Ενημέρωση", "Το αρχείο admin_page.py υπάρχει, αλλά η κλάση AdminPage δεν έχει δομηθεί σωστά ακόμα.\n\nΠεριμένω τον κώδικά σου!")
                self.show_login()
        else:
            messagebox.showinfo("Ενημέρωση", "Το αρχείο admin_page.py είναι κενό. Εκκρεμεί η υλοποίηση του UI του Διαχειριστή.\n\nΠεριμένω τον κώδικά σου!")
            self.show_login()

    # --- UC004: INVENTORY ---
    def show_inventory(self):
        self.clear_window()
        callbacks = {
            'back': self.show_admin_dashboard,
            'add': self.inventory_add,
            'update': self.inventory_update,
            'delete': self.inventory_delete
        }
        self.inventory_view = InventoryManagementPage(self.root, callbacks)
        self.load_inventory()

    def load_inventory(self):
        try:
            response = self.supabase.table("books").select("*").execute()
            self.inventory_view.populate_tree(response.data)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης αποθέματος:\n{e}")

    def inventory_add(self, barcode, title, author, category, price, stock):
        try:
            data = {"barcode": barcode, "title": title, "author": author, "category": category, "price": float(price), "stock": int(stock)}
            self.supabase.table("books").insert(data).execute()
            messagebox.showinfo("Επιτυχία", f"Το βιβλίο προστέθηκε.")
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία προσθήκης:\n{e}")

    def inventory_update(self, book_id, price, stock):
        try:
            data = {"price": float(price), "stock": int(stock)}
            response = self.supabase.table("books").update(data).eq("id", book_id).execute()
            if not response.data:
                messagebox.showwarning("Προσοχή", "Το βιβλίο δεν βρέθηκε ή δεν ενημερώθηκε.")
            else:
                messagebox.showinfo("Επιτυχία", "Ενημερώθηκε επιτυχώς.")
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία ενημέρωσης:\n{e}")

    def inventory_delete(self, book_id):
        try:
            self.supabase.table("books").delete().eq("id", book_id).execute()
            messagebox.showinfo("Επιτυχία", "Διαγράφηκε.")
            self.load_inventory()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Δεν μπορεί να διαγραφεί (πιθανώς έχει πωλήσεις):\n{e}")

    # --- UC005: STAFF ---
    def show_staff(self):
        self.clear_window()
        callbacks = {
            'back': self.show_admin_dashboard,
            'add': self.staff_hire,
            'toggle': self.staff_fire
        }
        self.staff_view = StaffManagementPage(self.root, callbacks)
        self.load_staff()

    def load_staff(self):
        try:
            response = self.supabase.table("users").select("id, username, role, is_active").execute()
            active_staff = [user for user in response.data if user.get('is_active')]
            self.staff_view.populate_tree(active_staff)
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης:\n{e}")

    def staff_hire(self, username, password, role):
        try:
            data = {"username": username, "password": password, "role": role.upper(), "is_active": True, "is_logged_in": False}
            self.supabase.table("users").insert(data).execute()
            messagebox.showinfo("Επιτυχία", f"Δημιουργήθηκε ο λογαριασμός '{username}'.")
            self.load_staff()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία πρόσληψης:\n{e}")

    def staff_fire(self, username):
        try:
            response = self.supabase.table("users").delete().eq("username", username).execute()
            if not response.data:
                messagebox.showwarning("Προσοχή", f"Δεν βρέθηκε χρήστης με username '{username}'.")
            else:
                messagebox.showinfo("Επιτυχία", f"Ο λογαριασμός '{username}' διαγράφηκε οριστικά.")
            self.load_staff()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία διαγραφής (πιθανώς ο χρήστης έχει πωλήσεις):\n{e}")