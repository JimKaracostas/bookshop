import unittest
from mockito import when, mock, unstub
import models.inventory_model as im
from models.inventory_model import InventoryModel

class TestInventoryModel(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_check_book_exists(self):
        mock_response = mock()
        mock_response.data = [{'id': 1}]
        
        mock_table = mock()
        mock_select = mock()
        mock_eq = mock()
        
        when(im.supabase).table('books').thenReturn(mock_table)
        when(mock_table).select('id').thenReturn(mock_select)
        when(mock_select).eq('title', 'Existing Book').thenReturn(mock_eq)
        when(mock_eq).execute().thenReturn(mock_response)
        
        result = InventoryModel.check_book_exists("Existing Book")
        self.assertTrue(result)
        
        mock_response_empty = mock()
        mock_response_empty.data = []
        mock_eq_empty = mock()
        when(mock_select).eq('title', 'Unknown Book').thenReturn(mock_eq_empty)
        when(mock_eq_empty).execute().thenReturn(mock_response_empty)
        
        result2 = InventoryModel.check_book_exists("Unknown Book")
        self.assertFalse(result2)

if __name__ == '__main__':
    unittest.main()
