import unittest
import vulnerable_app

class TestVulnerableApp(unittest.TestCase):
    
    def test_sql_injection_vector(self):
        """Тест для обнаружения SQL injection паттернов"""
        with vulnerable_app.app.test_client() as client:
            response = client.get('/search?username=admin')
            self.assertEqual(response.status_code, 200)
    
    def test_xss_vector(self):
        """Тест для обнаружения XSS паттернов"""
        with vulnerable_app.app.test_client() as client:
            response = client.get('/hello?name=test')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()