from django.contrib import admin
from django.db import models
from django.forms import modelform_factory
from django.forms.widgets import Select
from django.test import TestCase

from openformsclient.models import Configuration, OpenFormsSlugField, OpenFormsUUIDField


class Dummy(models.Model):
    form_uuid = OpenFormsUUIDField()
    form_slug = OpenFormsSlugField()

    class Meta:
        app_label = "tests"


class DummyAdmin(admin.ModelAdmin):
    pass


class ConfigurationTests(TestCase):
    def setUp(self):
        self.config = Configuration.get_solo()

    def test_client(self):
        self.config.api_root = "https://example.com/api/v1/"
        self.config.api_token = "token"

        client = self.config.client
        self.assertEqual(client.api_root, self.config.api_root)
        self.assertEqual(client.api_token, self.config.api_token)

    def test_save_updates_api_endpoint(self):
        self.config.api_root = "https://example.com/api/v5"
        self.config.save()

        self.config.refresh_from_db()

        self.assertEqual(self.config.api_root, "https://example.com/api/v5/")


class OpenFormsFieldTests(TestCase):
    def test_slug_form_field_widget(self):
        DummyForm = modelform_factory(Dummy, fields=["form_slug"])
        form = DummyForm()
        form_field = form.fields["form_slug"]

        self.assertIsInstance(form_field.widget, Select)

    def test_slug_form_field_admin_widget(self):
        model_admin = DummyAdmin(Dummy, admin.site)
        form_field = model_admin.formfield_for_dbfield(
            Dummy._meta.get_field("form_slug"), request=None
        )

        self.assertIsInstance(form_field.widget, Select)

    def test_uuid_form_field_widget(self):
        DummyForm = modelform_factory(Dummy, fields=["form_uuid"])
        form = DummyForm()
        form_field = form.fields["form_uuid"]

        self.assertIsInstance(form_field.widget, Select)

    def test_uuid_form_field_admin_widget(self):
        model_admin = DummyAdmin(Dummy, admin.site)
        form_field = model_admin.formfield_for_dbfield(
            Dummy._meta.get_field("form_uuid"), request=None
        )

        self.assertIsInstance(form_field.widget, Select)
