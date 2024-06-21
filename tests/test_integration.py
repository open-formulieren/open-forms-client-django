import datetime
from uuid import UUID

from django.forms import modelform_factory
from django.test import TestCase

import requests_mock
import time_machine

from openformsclient.models import Configuration
from testapp.models import Page


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
                {
                    "uuid": "1b0d0675-2caf-48e8-beda-c32c6732b63c",
                    "slug": "test-2",
                    "name": "Test 2",
                },
                {
                    "uuid": "f4423c99-6341-442e-aedc-b47779579f4d",
                    "slug": "test-1",
                    "name": "Test 1",
                },
            ],
        )

    def test_values_in_slug_form_field(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_slug"])
        page_form = PageForm()

        self.assertListEqual(
            list(page_form.fields["form_slug"].choices),
            [
                ("", "---------"),
                ("test-1", "Test 1"),
                ("test-2", "Test 2"),
            ],
        )

    def test_values_in_uuid_form_field(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_uuid"])
        page_form = PageForm()

        self.assertListEqual(
            list(page_form.fields["form_uuid"].choices),
            [
                ("", "---------"),
                ("f4423c99-6341-442e-aedc-b47779579f4d", "Test 1"),
                ("1b0d0675-2caf-48e8-beda-c32c6732b63c", "Test 2"),
            ],
        )

    def test_uuid_form_field_valid_value(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_uuid"])
        page_form = PageForm(data={"form_uuid": "f4423c99-6341-442e-aedc-b47779579f4d"})

        self.assertTrue(page_form.is_valid())
        page_form.save()

        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(
            Page.objects.get().form_uuid, UUID("f4423c99-6341-442e-aedc-b47779579f4d")
        )

    def test_uuid_form_field_invalid_value(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_uuid"])
        page_form = PageForm(data={"form_uuid": "3285e94f-adae-4a5c-a467-30690a279364"})

        self.assertFalse(page_form.is_valid())

    def test_uuid_form_field_blank_null(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_uuid"])
        page_form = PageForm(data={"form_uuid": ""})

        self.assertTrue(page_form.is_valid())
        page_form.save()

        self.assertEqual(Page.objects.count(), 1)
        self.assertIsNone(Page.objects.get().form_uuid)

    def test_slug_form_field_valid_value(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_slug"])
        page_form = PageForm(data={"form_slug": "test-1"})

        self.assertTrue(page_form.is_valid())
        page_form.save()

        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(Page.objects.get().form_slug, "test-1")

    def test_slug_form_field_invalid_value(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_slug"])
        page_form = PageForm(data={"form_slug": "test-3"})

        self.assertFalse(page_form.is_valid())

    def test_slug_form_field_blank(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_slug"])
        page_form = PageForm(data={"form_slug": ""})

        self.assertTrue(page_form.is_valid())
        page_form.save()

        self.assertEqual(Page.objects.count(), 1)
        self.assertEqual(Page.objects.get().form_slug, "")

    def test_form_retrieval_cache(self, m):
        self._prepare_mock(m)

        PageForm = modelform_factory(Page, fields=["form_slug"])
        page_form = PageForm()

        with time_machine.travel(0) as traveller:
            list(page_form.fields["form_slug"].choices)
            list(page_form.fields["form_slug"].choices)

            self.assertEqual(m.call_count, 1)

            traveller.shift(datetime.timedelta(seconds=60))

            list(page_form.fields["form_slug"].choices)

            self.assertEqual(m.call_count, 2)
