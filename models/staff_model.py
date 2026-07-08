# models/staff_model.py

# IMPORTS
from supabase import create_client, Client

SUPABASE_URL = "https://fhewndsaybrqvkmmfzir.supabase.co/"
SUPABASE_KEY = "sb_publishable_qqHWxwErRpou7wVGv911_w_ZYuOJKJ6"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class StaffModel:
    @staticmethod
    def check_username_exists(username: str) -> bool:
        """Ελέγχει αν το username υπάρχει ήδη για να αποτραπεί διπλή εγγραφή."""
        try:
            response = supabase.table("users").select("id").eq("username", username).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Σφάλμα ελέγχου username: {e}")
            return False

    @staticmethod
    def hire_staff(username: str, password: str, role: str = "seller") -> bool:
        """Προσθέτει νέο υπάλληλο στον πίνακα users."""
        try:
            data = {
                "username": username,
                "password": password,
                "role": role,
                "is_active": True,
                "is_logged_in": False
            }
            supabase.table("users").insert(data).execute()
            return True
        except Exception as e:
            print(f"Σφάλμα προσθήκης υπαλλήλου: {e}")
            return False

    @staticmethod
    def fire_staff(username: str) -> bool:
        """Διαγράφει οριστικά τον λογαριασμό του υπαλλήλου."""
        try:
            supabase.table("users").delete().eq("username", username).execute()
            return True
        except Exception as e:
            print(f"Σφάλμα διαγραφής υπαλλήλου: {e}")
            return False