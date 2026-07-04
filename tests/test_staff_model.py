import unittest
import sys
from unittest.mock import patch, MagicMock

sys.modules['supabase'] = MagicMock()

from models.staff_model import StaffModel

class TestStaffModel(unittest.TestCase):

    @patch('models.staff_model.supabase')
    def test_check_username_exists(self, mock_supabase):
        mock_response = MagicMock()
        mock_response.data = [{'id': 1}]
        
        mock_table = MagicMock()
        mock_select = MagicMock()
        mock_eq = MagicMock()
        
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_select
        mock_select.eq.return_value = mock_eq
        mock_eq.execute.return_value = mock_response
        
        result = StaffModel.check_username_exists("testuser")
        self.assertTrue(result)
        
        mock_response.data = []
        result2 = StaffModel.check_username_exists("unknown")
        self.assertFalse(result2)

    @patch('models.staff_model.supabase')
    def test_hire_staff(self, mock_supabase):
        mock_table = MagicMock()
        mock_insert = MagicMock()
        
        mock_supabase.table.return_value = mock_table
        mock_table.insert.return_value = mock_insert
        
        result = StaffModel.hire_staff("new_staff", "password123")
        self.assertTrue(result)
        mock_supabase.table.assert_called_with("users")
        mock_insert.execute.assert_called_once()

    @patch('models.staff_model.supabase')
    def test_fire_staff(self, mock_supabase):
        mock_table = MagicMock()
        mock_update = MagicMock()
        mock_eq = MagicMock()
        
        mock_supabase.table.return_value = mock_table
        mock_table.update.return_value = mock_update
        mock_update.eq.return_value = mock_eq
        
        result = StaffModel.fire_staff("old_staff")
        self.assertTrue(result)
        mock_supabase.table.assert_called_with("users")
        mock_table.update.assert_called_with({"is_active": False})
        mock_update.eq.assert_called_with("username", "old_staff")
        mock_eq.execute.assert_called_once()

if __name__ == '__main__':
    unittest.main()
