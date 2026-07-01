# models/book_model.py
"""Simple local BookModel with JSON-backed storage.

Provides: search_books, add_book, update_book, delete_book.
This replaces external Book Pass logic for offline usage.
"""
import json
import os
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.json')


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def _load_books() -> List[Dict]:
    _ensure_data_dir()
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_books(books: List[Dict]):
    _ensure_data_dir()
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


class BookModel:
    def __init__(self):
        _ensure_data_dir()

    def _next_id(self, books: List[Dict]) -> int:
        if not books:
            return 1
        return max(int(b.get('id', 0)) for b in books) + 1

    def search_books(self, term: Optional[str] = None, by_barcode: bool = False) -> List[Dict]:
        books = _load_books()
        if not term:
            return books
        term_lower = str(term).lower()
        if by_barcode:
            found = [b for b in books if str(b.get('barcode','')).lower() == term_lower]
            if found:
                return found
            # fallback: maybe user typed title instead of barcode
            found_title = [b for b in books if term_lower in str(b.get('title','')).lower()]
            return found_title
        # search by id, title, author, category
        result = []
        for b in books:
            if term_lower in str(b.get('title','')).lower() or term_lower in str(b.get('author','')).lower() or term_lower in str(b.get('category','')).lower() or term_lower == str(b.get('id','')):
                result.append(b)
        return result

    def add_book(self, barcode: str, title: str, author: str, category: str, price: float, stock: int) -> Dict:
        try:
            books = _load_books()
            # prevent duplicate barcode
            for b in books:
                if b.get('barcode') and b['barcode'] == barcode:
                    return {"success": False, "message": "Duplicate barcode"}
            new_id = self._next_id(books)
            book = {
                'id': new_id,
                'barcode': barcode,
                'title': title,
                'author': author,
                'category': category,
                'price': float(price),
                'stock': int(stock)
            }
            books.append(book)
            _save_books(books)
            return {"success": True, "message": "Book added", "book": book}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def update_book(self, book_id, price: float, stock: int) -> Dict:
        try:
            books = _load_books()
            for b in books:
                if str(b.get('id')) == str(book_id):
                    b['price'] = float(price)
                    b['stock'] = int(stock)
                    _save_books(books)
                    return {"success": True, "message": "Book updated", "book": b}
            return {"success": False, "message": "Book not found"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def delete_book(self, book_id) -> Dict:
        try:
            books = _load_books()
            new_books = [b for b in books if str(b.get('id')) != str(book_id)]
            if len(new_books) == len(books):
                return {"success": False, "message": "Book not found"}
            _save_books(new_books)
            return {"success": True, "message": "Book deleted"}
        except Exception as e:
            return {"success": False, "message": str(e)}
