from django.test import TestCase

import requests_mock

from openformsclient.models import Configuration
from openformsclient.utils import get_form_choices


@requests_mock.Mocker()
class UtilsTests(TestCase):
    def setUp(self):
        self.config = Configuration.objects.create(
            api_root="https://example.com/api/v1/",
            api_token="token",
        )

    def test_get_form_choices_without_client(self, m):
        m.get(
            f"{self.config.api_root}forms",
            json=[
                {"uuid": "1b0d0675-2caf-48e8-beda-c32c6732b63c", "name": "Test 2"},
                {"uuid": "f4423c99-6341-442e-aedc-b47779579f4d", "name": "Test 1"},
            ],
        )

        result = get_form_choices()

        self.assertListEqual(
            result,
            [
                ("f4423c99-6341-442e-aedc-b47779579f4d", "Test 1"),
                ("1b0d0675-2caf-48e8-beda-c32c6732b63c", "Test 2"),
            ],
        )

    def test_get_form_choices_with_client(self, m):
        m.get(
            f"{self.config.api_root}forms",
            json=[
                {"uuid": "1b0d0675-2caf-48e8-beda-c32c6732b63c", "name": "Test 2"},
                {"uuid": "f4423c99-6341-442e-aedc-b47779579f4d", "name": "Test 1"},
            ],
        )

        result = get_form_choices(self.config.client)

        self.assertListEqual(
            result,
            [
                ("f4423c99-6341-442e-aedc-b47779579f4d", "Test 1"),
                ("1b0d0675-2caf-48e8-beda-c32c6732b63c", "Test 2"),
            ],
        )
