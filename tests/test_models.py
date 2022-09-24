from django.contrib import admin
from django.db import models
from django.forms import modelform_factory
from django.forms.widgets import Select
from django.test import TestCase

from openformsclient.models import Configuration, OpenFormsField


class Dummy(models.Model):
    form = OpenFormsField()

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
    def test_form_field_widget(self):
        DummyForm = modelform_factory(Dummy, fields=["form"])
        form = DummyForm()
        form_field = form.fields["form"]

        self.assertIsInstance(form_field.widget, Select)

    def test_form_field_admin_widget(self):
        model_admin = DummyAdmin(Dummy, admin.site)
        form_field = model_admin.formfield_for_dbfield(
            Dummy._meta.get_field("form"), request=None
        )

        self.assertIsInstance(form_field.widget, Select)
