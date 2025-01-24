# test_integration.py
import unittest

import requests

BASE_URL = "http://127.0.0.1:5000"


class TestIntegration(unittest.TestCase):
    def test_add_and_get_users(self):
        # Aggiungere un nuovo utente
        user = {"name": "John Doe", "email": "john.doe@example.com"}
        response = requests.post(f"{BASE_URL}/users", json=user)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json(), user)

        # Recuperare la lista degli utenti
        response = requests.get(f"{BASE_URL}/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn(user, response.json())


if __name__ == "__main__":
    unittest.main()
