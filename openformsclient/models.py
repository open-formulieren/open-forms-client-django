import logging

from django.core.cache import cache
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms.fields import TypedChoiceField
from django.forms.widgets import Select
from django.utils.functional import cached_property
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
        return Client(self.api_root, self.api_token)


class OpenFormsField(models.UUIDField):
    """
    Basic field for use in Django models to render a Select widget filled with
    the available forms in Open Forms.
    """

    CACHE_KEY = "openformsclient.models.OpenFormsField.get_choices"

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
        choices = cache.get(self.CACHE_KEY)
        if choices is None:
            try:
                choices = get_form_choices()
            except Exception as e:
                logger.exception(e)
                choices = []
            else:
                cache.set(self.CACHE_KEY, choices)

        if choices:
            if include_blank:
                blank_defined = any(choice in ("", None) for choice, _ in choices)
                if not blank_defined:
                    choices = blank_choice + choices

        return choices
