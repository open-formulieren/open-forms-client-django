from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from solo.admin import SingletonModelAdmin

from .models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "api_root",
                    "api_token",
                    "status",
                )
            },
        ),
        (
            _("SDK"),
            {
                "fields": (
                    "sdk_css_url",
                    "sdk_js_url",
                ),
            },
        ),
        (
            _("Advanced"),
            {
                "fields": ("use_sentry",),
            },
        ),
    )
    readonly_fields = ("status",)

    @admin.display
    def status(self, obj):
        from django.contrib.admin.templatetags.admin_list import _boolean_icon

        healthy, message = obj.client.is_healthy()
        return format_html("{} {}", _boolean_icon(healthy), message)
