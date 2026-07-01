import unittest
from unittest.mock import patch
import os
import json
import tempfile
from models.book_model import BookModel, _save_books, _load_books

class TestBookModel(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, 'test_books.json')
        
        # Patch the file path
        self.patcher = patch('models.book_model.BOOKS_FILE', self.test_file)
        self.patcher.start()
        
        # Initialize file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
            
        self.model = BookModel()

    def tearDown(self):
        self.patcher.stop()
        self.test_dir.cleanup()

    def test_add_book(self):
        result = self.model.add_book("123456", "Test Book", "Test Author", "Fiction", 15.5, 10)
        self.assertTrue(result['success'])
        self.assertEqual(result['book']['title'], "Test Book")
        self.assertEqual(result['book']['barcode'], "123456")
        
        # Test duplicate barcode
        result2 = self.model.add_book("123456", "Another Book", "Author", "Category", 10.0, 5)
        self.assertFalse(result2['success'])
        self.assertEqual(result2['message'], "Duplicate barcode")

    def test_search_books(self):
        self.model.add_book("111", "Book A", "Author A", "Cat A", 10.0, 5)
        self.model.add_book("222", "Book B", "Author B", "Cat B", 20.0, 2)
        
        # Search by term
        results = self.model.search_books("Book A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Book A")
        
        # Search by barcode
        results_barcode = self.model.search_books("222", by_barcode=True)
        self.assertEqual(len(results_barcode), 1)
        self.assertEqual(results_barcode[0]['barcode'], "222")
        
        # Empty search
        all_books = self.model.search_books()
        self.assertEqual(len(all_books), 2)

    def test_update_book(self):
        add_result = self.model.add_book("333", "Book C", "Author C", "Cat C", 10.0, 5)
        book_id = add_result['book']['id']
        
        update_result = self.model.update_book(book_id, 12.5, 8)
        self.assertTrue(update_result['success'])
        self.assertEqual(update_result['book']['price'], 12.5)
        self.assertEqual(update_result['book']['stock'], 8)
        
        # Test update non-existent book
        fake_update = self.model.update_book(999, 10.0, 10)
        self.assertFalse(fake_update['success'])

    def test_delete_book(self):
        add_result = self.model.add_book("444", "Book D", "Author D", "Cat D", 10.0, 5)
        book_id = add_result['book']['id']
        
        delete_result = self.model.delete_book(book_id)
        self.assertTrue(delete_result['success'])
        
        books = self.model.search_books()
        self.assertEqual(len(books), 0)
        
        # Test delete non-existent book
        fake_delete = self.model.delete_book(999)
        self.assertFalse(fake_delete['success'])

if __name__ == '__main__':
    unittest.main()
