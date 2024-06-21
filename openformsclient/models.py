import logging

from django.core.cache import cache
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.fields import TypedChoiceField
from django.forms.widgets import Select
from django.utils.functional import cached_property, lazy
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

from .client import Client
from .utils import get_form_choices

logger = logging.getLogger(__name__)


class Configuration(SingletonModel):
    """
    The Open Forms configuration to retrieve and render forms.
    """

    api_root = models.URLField(
        _("API root URL"),
        help_text=_(
            "The root URL of the Open Forms API. Example: https://forms.example.com/api/v1/"
        ),
    )
    api_token = models.CharField(
        _("API Token"),
        max_length=128,
        blank=True,
        help_text=_(
            "The Open Forms API token value. Example: 7ab84e80b3d68d52a5f9e1712e3d0eda27d21e58"
        ),
    )
    client_timeout = models.PositiveIntegerField(
        _("Client request timeout"),
        default=5,
        help_text=_("The timeout that is used for requests (in seconds)"),
    )

    sdk_css_url = models.URLField(
        _("SDK CSS URL"),
        blank=True,
        help_text=_(
            "The Open Forms SDK stylesheet URL. Example: https://forms.example.com/static/sdk/open-forms-sdk.css"
        ),
    )
    sdk_js_url = models.URLField(
        _("SDK JS URL"),
        blank=True,
        help_text=_(
            "The Open Forms SDK JavaScript URL. Example: https://forms.example.com/static/sdk/open-forms-sdk.js"
        ),
    )

    use_sentry = models.BooleanField(
        _("Use Sentry"),
        default=False,
        help_text=_(
            "When enabled and Sentry is installed, Open Forms SDK errors will be sent to the configured Sentry instance."
        ),
    )

    class Meta:
        verbose_name = _("Open Forms client configuration")

    def __str__(self):
        return "Open Forms client configuration"

    def save(self, *args, **kwargs):
        if not self.api_root.endswith("/"):
            self.api_root += "/"
        return super().save(*args, **kwargs)

    @cached_property
    def client(self):
        return Client(self.api_root, self.api_token, self.client_timeout)


class OpenFormsBaseField:
    """
    Basic field for use in Django models to render a Select widget filled with
    the available forms (uuid, name) or (slug, name) in Open Forms.

    This form records the form's UUID or slug, depending on what concrete model
    class is used.
    """

    description = _("Open Forms form")
    use_uuids = None

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # We do not exclude max_length if it matches default as we want to change
        # the default in future.
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            "required": not self.blank,
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "widget": Select,
        }

        defaults["choices"] = self.get_choices(include_blank=self.blank)
        defaults["coerce"] = self.to_python

        return TypedChoiceField(**defaults)

    def get_choices(
        self,
        include_blank=True,
        blank_choice=BLANK_CHOICE_DASH,
        limit_choices_to=None,
        ordering=(),
    ):
        def _fetch():
            cache_key = f"openformsclient.models.OpenFormsBaseField.get_choices__use_uuids_{self.use_uuids}"

            choices = cache.get(cache_key)
            if choices is None:
                try:
                    choices = get_form_choices(use_uuids=self.use_uuids)
                except Exception as exc:
                    logger.exception(exc)
                    choices = []
                else:
                    cache.set(cache_key, choices, timeout=60)

            if choices:
                if include_blank:
                    blank_defined = any(choice in ("", None) for choice, _ in choices)
                    if not blank_defined:
                        choices = blank_choice + choices
            return choices

        return lazy(_fetch, list)


class OpenFormsUUIDField(OpenFormsBaseField, models.UUIDField):
    """
    Basic field for use in Django models to render a Select widget filled with
    the available forms (uuid, name) in Open Forms.

    This field records the form's UUID. This makes the choice really specific.
    Note that to allow empty records, you will need to set ``null=True`` and
    ``blank=True``.
    """

    use_uuids = True

    def get_db_prep_value(self, value, connection, prepared=False):
        # A Select widget always returns a string. If an empty string is
        # returned, we need to force it to be None since an empty string is not
        # valid UUID nor is it empty.
        if not value:
            return None
        return super().get_db_prep_value(value, connection, prepared)


class OpenFormsSlugField(OpenFormsBaseField, models.SlugField):
    """
    Basic field for use in Django models to render a Select widget filled with
    the available forms (slug, name) in Open Forms.

    This field records the form's slug. This allows an Open Forms user to
    gracefully change the form without the need to change the reference
    everywhere.
    """

    use_uuids = False

    def __init__(
        self, *args, max_length=100, db_index=False, allow_unicode=False, **kwargs
    ):
        super().__init__(
            *args,
            max_length=max_length,
            db_index=db_index,
            allow_unicode=allow_unicode,
            **kwargs,
        )
