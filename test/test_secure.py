import unittest
import secure_app

class TestSecureApp(unittest.TestCase):
    
    def test_safe_sql_query(self):
        """Тест безопасных SQL запросов"""
        with secure_app.app.test_client() as client:
            response = client.get('/search?username=admin')
            self.assertEqual(response.status_code, 200)
    
    def test_safe_xss_prevention(self):
        """Тест защиты от XSS"""
        with secure_app.app.test_client() as client:
            response = client.get('/hello?name=<script>alert(1)</script>')
            self.assertEqual(response.status_code, 200)
            self.assertIn('&lt;script&gt;', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()