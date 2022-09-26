import sys
from unittest.mock import MagicMock

from django.template import Context, Template
from django.test import TestCase

from openformsclient.models import Configuration


class TemplateTagsTests(TestCase):
    def setUp(self):
        self.config = Configuration.objects.create(
            api_root="https://forms.example.com/api/v1/",
            api_token="secret-token",
            sdk_css_url="https://forms.example.com/sdk.css",
            sdk_js_url="https://forms.example.com/sdk.js",
            use_sentry=False,
        )

    def test_openforms_form(self):
        html = """
        {% load openforms %}
        {% openforms_form myform %}
        """
        form_id = "f4423c99-6341-442e-aedc-b47779579f4d"
        result = Template(html).render(Context({"myform": form_id}))

        self.assertIn('id="openforms-root"', result)
        self.assertIn(f'data-base-url="{self.config.api_root}"', result)
        self.assertIn(f'data-form-id="{form_id}"', result)
        self.assertIn("getElementById('openforms-root'", result)
        self.assertNotIn("data-csp-nonce", result)
        self.assertNotIn("data-lang", result)
        self.assertNotIn("data-sentry-dsn", result)
        self.assertNotIn("data-sentry-env", result)

    def test_openforms_form_with_extra_args(self):
        html = """
        {% load openforms %}
        {% openforms_form myform csp_nonce=mynonce lang="nl" %}
        """
        form_id = "f4423c99-6341-442e-aedc-b47779579f4d"
        nonce = "foobar"
        result = Template(html).render(Context({"myform": form_id, "mynonce": nonce}))

        self.assertIn(f'data-csp-nonce="{nonce}"', result)
        self.assertIn('data-lang="nl"', result)

    def test_openforms_form_with_sentry_but_no_sentry_installed(self):
        self.config.use_sentry = True
        self.config.save()

        # Emulate that Sentry is not installed (even if it is installed locally)
        import builtins

        original_import = builtins.__import__

        def custom_import(name, globals, locals, fromlist, level):
            if name == "sentry_sdk":
                raise ImportError
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = custom_import
        # Emulate prep done.

        html = """
        {% load openforms %}
        {% openforms_form myform %}
        """
        form_id = "f4423c99-6341-442e-aedc-b47779579f4d"
        result = Template(html).render(Context({"myform": form_id}))

        self.assertIn(f'data-form-id="{form_id}"', result)
        self.assertNotIn("data-sentry-dsn", result)
        self.assertNotIn("data-sentry-env", result)

        # Restore original if present.
        builtins.__import__ = original_import

    def test_openforms_form_with_sentry_and_sentry_installed(self):
        self.config.use_sentry = True
        self.config.save()

        sentry_options = {
            "dsn": "https://sentry.example.com",
            "environment": "test",
        }

        # Emulate that Sentry is installed with our options.
        sentry_sdk = None
        if "sentry_sdk" in sys.modules:
            sentry_sdk = sys.modules["sentry_sdk"]
            del sys.modules["sentry_sdk"]

        sentry_sdk_mock = MagicMock()
        sentry_sdk_mock.Hub.current.client.options = sentry_options
        sys.modules["sentry_sdk"] = sentry_sdk_mock
        # Emulation prep done.

        html = """
        {% load openforms %}
        {% openforms_form myform %}
        """
        form_id = "f4423c99-6341-442e-aedc-b47779579f4d"
        result = Template(html).render(Context({"myform": form_id}))

        self.assertIn(f'data-form-id="{form_id}"', result)
        self.assertIn(f'data-sentry-dsn="{sentry_options["dsn"]}"', result)
        self.assertIn(f'data-sentry-env="{sentry_options["environment"]}"', result)

        del sys.modules["sentry_sdk"]

        # Restore original if present
        if sentry_sdk is not None:
            sys.modules["sentry_sdk"] = sentry_sdk

    def test_openforms_sdk_css(self):
        html = """
        {% load openforms %}
        {% openforms_sdk_css %}
        """
        result = Template(html).render(Context({}))

        self.assertIn(f'href="{self.config.sdk_css_url}"', result)

    def test_openforms_sdk_js(self):
        html = """
        {% load openforms %}
        {% openforms_sdk_js %}
        """
        result = Template(html).render(Context({}))

        self.assertIn(f'src="{self.config.sdk_js_url}"', result)

    def test_openforms_sdk_media(self):
        html = """
        {% load openforms %}
        {% openforms_sdk_media %}
        """
        result = Template(html).render(Context({}))

        self.assertIn(f'href="{self.config.sdk_css_url}"', result)
        self.assertIn(f'src="{self.config.sdk_js_url}"', result)
