# models/inventory_model.py

# IMPORTS
# pyrefly: ignore [missing-import]
from supabase import create_client, Client

SUPABASE_URL = "https://fhewndsaybrqvkmmfzir.supabase.co/"
SUPABASE_KEY = "sb_publishable_qqHWxwErRpou7wVGv911_w_ZYuOJKJ6"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class InventoryModel:
    @staticmethod
    def check_book_exists(book_title: str) -> bool:
        """Ελέγχει αν ο τίτλος/κωδικός του βιβλίου υπάρχει ήδη στη βάση."""
        try:
            response = supabase.table("books").select("id").eq("title", book_title).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Σφάλμα ελέγχου αποθέματος: {e}")
            return False