import unittest
from mockito import when, unstub, ANY, verify
import models.book_model as bm
from models.book_model import BookModel

class TestBookModel(unittest.TestCase):
    def setUp(self):
        when(bm)._ensure_data_dir().thenReturn(None)
        self.model = BookModel()

    def tearDown(self):
        unstub()

    def test_add_book(self):
        when(bm)._load_books().thenReturn([])
        when(bm)._save_books(ANY).thenReturn(None)
        
        result = self.model.add_book("123456", "Test Book", "Test Author", "Fiction", 15.5, 10)
        self.assertTrue(result['success'])
        self.assertEqual(result['book']['title'], "Test Book")
        self.assertEqual(result['book']['barcode'], "123456")
        
        verify(bm)._save_books(ANY)
        
        # Test duplicate
        when(bm)._load_books().thenReturn([{'id': 1, 'barcode': "123456"}])
        result2 = self.model.add_book("123456", "Another Book", "Author", "Category", 10.0, 5)
        self.assertFalse(result2['success'])
        self.assertEqual(result2['message'], "Duplicate barcode")

    def test_search_books(self):
        mock_books = [
            {'id': 1, 'barcode': '111', 'title': 'Book A', 'author': 'Author A', 'category': 'Cat A', 'price': 10.0, 'stock': 5},
            {'id': 2, 'barcode': '222', 'title': 'Book B', 'author': 'Author B', 'category': 'Cat B', 'price': 20.0, 'stock': 2}
        ]
        when(bm)._load_books().thenReturn(mock_books)
        
        results = self.model.search_books("Book A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Book A")
        
        results_barcode = self.model.search_books("222", by_barcode=True)
        self.assertEqual(len(results_barcode), 1)
        self.assertEqual(results_barcode[0]['barcode'], "222")
        
        all_books = self.model.search_books()
        self.assertEqual(len(all_books), 2)

    def test_update_book(self):
        mock_books = [{'id': 1, 'barcode': '333', 'price': 10.0, 'stock': 5}]
        when(bm)._load_books().thenReturn(mock_books)
        when(bm)._save_books(ANY).thenReturn(None)
        
        update_result = self.model.update_book(1, 12.5, 8)
        self.assertTrue(update_result['success'])
        self.assertEqual(update_result['book']['price'], 12.5)
        self.assertEqual(update_result['book']['stock'], 8)
        
        fake_update = self.model.update_book(999, 10.0, 10)
        self.assertFalse(fake_update['success'])

    def test_delete_book(self):
        mock_books = [{'id': 1, 'barcode': '444'}]
        when(bm)._load_books().thenReturn(mock_books)
        when(bm)._save_books(ANY).thenReturn(None)
        
        delete_result = self.model.delete_book(1)
        self.assertTrue(delete_result['success'])
        
        fake_delete = self.model.delete_book(999)
        self.assertFalse(fake_delete['success'])

if __name__ == '__main__':
    unittest.main()
