from django.test import TestCase

import requests_mock
from requests.exceptions import HTTPError

from openformsclient.client import Client


@requests_mock.Mocker()
class ClientTests(TestCase):
    def setUp(self):
        self.api_root = "https://example.com/api/v1/"
        self.api_token = "token"
        self.client = Client(self.api_root, self.api_token)

    def test_is_healthy(self, m):
        m.head(
            f"{self.api_root}forms",
            request_headers={"Authorization": f"Token {self.api_token}"},
        )

        health, msg = self.client.is_healthy()
        self.assertTrue(health)
        self.assertEqual(msg, "")

    def test_is_healthy_invalid_response(self, m):
        m.head(f"{self.api_root}forms", status_code=500)  # Doesn't really matter
        m.get(f"{self.api_root}forms", text="Woops")

        health, msg = self.client.is_healthy()
        self.assertFalse(health)
        self.assertEqual(msg, "Server did not return a valid response (HTTP 500).")

    def test_is_healthy_invalid_token(self, m):
        m.head(f"{self.api_root}forms", status_code=401)
        m.get(
            f"{self.api_root}forms",
            json={
                "type": "https://example.com/fouten/AuthenticationFailed/",
                "code": "authentication_failed",
                "title": "Ongeldige authenticatiegegevens.",
                "status": 401,
                "detail": "Ongeldige token.",
                "instance": "urn:uuid:8dddcb04-a412-451a-a7c5-f77d1aef36f5",
            },
        )

        health, msg = self.client.is_healthy()
        self.assertFalse(health)
        self.assertEqual(msg, "Ongeldige token.")

    def test_get_forms(self, m):
        m.get(f"{self.api_root}forms", json=[])

        result = self.client.get_forms()
        self.assertListEqual(result, [])

    def test_get_forms_with_error(self, m):
        m.get(f"{self.api_root}forms", status_code=401)

        with self.assertRaises(HTTPError):
            self.client.get_forms()

    def test_get_form(self, m):
        m.get(f"{self.api_root}forms/myform", json={})

        result = self.client.get_form("myform")
        self.assertDictEqual(result, {})

    def test_get_form_with_error(self, m):
        m.get(f"{self.api_root}forms/myform", status_code=401)

        with self.assertRaises(HTTPError):
            self.client.get_form("myform")
