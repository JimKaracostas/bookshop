# db.py

import psycopg2
import os
from dotenv import load_dotenv, find_dotenv

def setup_database():
    load_dotenv(find_dotenv())
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("Σφάλμα: Δεν βρέθηκε το DATABASE_URL. Βεβαιώσου ότι υπάρχει το αρχείο .env!")
        return

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True 
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL, 
            is_active BOOLEAN DEFAULT TRUE, 
            is_logged_in BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            barcode VARCHAR(100) UNIQUE NOT NULL, 
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            category VARCHAR(100), 
            price DECIMAL(10, 2) NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id), 
            customer_id INTEGER REFERENCES users(id), 
            total_amount DECIMAL(10, 2) NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sale_items (
            id SERIAL PRIMARY KEY,
            sale_id INTEGER REFERENCES sales(id) ON DELETE CASCADE,
            book_id INTEGER REFERENCES books(id),
            quantity INTEGER NOT NULL,          -- Διορθωμένο για να ταιριάζει με το GUI
            price_at_time DECIMAL(10, 2) NOT NULL -- Διορθωμένο για να ταιριάζει με το GUI
        );
        ''')

        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                ("admin", "admin", "MANAGER")
            )
            print("Δημιουργήθηκε ο default λογαριασμός διαχειριστή (Username: admin με Password: admin).")

        print("Το στήσιμο της βάσης δεδομένων στο Supabase ολοκληρώθηκε επιτυχώς!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Σφάλμα κατά τη δημιουργία πινάκων: {e}")

if __name__ == "__main__":
    setup_database()