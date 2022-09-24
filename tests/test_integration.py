from django.contrib import admin
from django.db import models
from django.forms import modelform_factory
from django.forms.widgets import Select
from django.test import TestCase

import requests_mock

from openformsclient.models import Configuration, OpenFormsField


class Page(models.Model):
    form = OpenFormsField()

    class Meta:
        app_label = "tests"


@requests_mock.Mocker()
class IntegrationTests(TestCase):
    def setUp(self):
        self.config = Configuration.objects.create(
            api_root="https://example.com/api/v1/",
            api_token="token",
        )

    def _prepare_mock(self, m):
        m.get(
            f"{self.config.api_root}forms",
            json=[
                {"uuid": "1b0d0675-2caf-48e8-beda-c32c6732b63c", "name": "Test 2"},
                {"uuid": "f4423c99-6341-442e-aedc-b47779579f4d", "name": "Test 1"},
            ],
        )

    def test_values_in_form_field(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form"])
        page_form = PageForm()

        self.assertListEqual(
            page_form.fields["form"].choices,
            [
                ("f4423c99-6341-442e-aedc-b47779579f4d", "Test 1"),
                ("1b0d0675-2caf-48e8-beda-c32c6732b63c", "Test 2"),
            ],
        )

    def test_valid_value_in_form_field(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form"])
        page_form = PageForm(data={"form": "f4423c99-6341-442e-aedc-b47779579f4d"})

        self.assertTrue(page_form.is_valid())

    def test_invalid_value_in_form_field(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form"])
        page_form = PageForm(data={"form": "3285e94f-adae-4a5c-a467-30690a279364"})

        self.assertFalse(page_form.is_valid())
