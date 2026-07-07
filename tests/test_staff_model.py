import unittest
from mockito import when, mock, unstub, ANY, verify
import models.staff_model as sm
from models.staff_model import StaffModel

class TestStaffModel(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_check_username_exists(self):
        mock_response = mock()
        mock_response.data = [{'id': 1}]
        
        mock_table = mock()
        mock_select = mock()
        mock_eq = mock()
        
        when(sm.supabase).table('users').thenReturn(mock_table)
        when(mock_table).select('id').thenReturn(mock_select)
        when(mock_select).eq('username', 'testuser').thenReturn(mock_eq)
        when(mock_eq).execute().thenReturn(mock_response)
        
        result = StaffModel.check_username_exists("testuser")
        self.assertTrue(result)
        
        mock_response_empty = mock()
        mock_response_empty.data = []
        mock_eq_empty = mock()
        when(mock_select).eq('username', 'unknown').thenReturn(mock_eq_empty)
        when(mock_eq_empty).execute().thenReturn(mock_response_empty)
        
        result2 = StaffModel.check_username_exists("unknown")
        self.assertFalse(result2)

    def test_hire_staff(self):
        mock_table = mock()
        mock_insert = mock()
        
        when(sm.supabase).table('users').thenReturn(mock_table)
        when(mock_table).insert(ANY).thenReturn(mock_insert)
        when(mock_insert).execute().thenReturn(None)
        
        result = StaffModel.hire_staff("new_staff", "password123")
        self.assertTrue(result)
        verify(mock_insert).execute()

    def test_fire_staff(self):
        mock_table = mock()
        mock_delete = mock()
        mock_eq = mock()
        
        when(sm.supabase).table('users').thenReturn(mock_table)
        when(mock_table).delete().thenReturn(mock_delete)
        when(mock_delete).eq("username", "old_staff").thenReturn(mock_eq)
        when(mock_eq).execute().thenReturn(None)
        
        result = StaffModel.fire_staff("old_staff")
        self.assertTrue(result)
        verify(mock_eq).execute()

if __name__ == '__main__':
    unittest.main()
