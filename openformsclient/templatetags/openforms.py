import logging

from django import template
from django.template.loader import render_to_string

from ..models import Configuration

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def openforms_form(form_id, csp_nonce=None, base_path=None, lang=None, html_id=None):
    template_name = "openformsclient/templatetags/openforms_form.html"

    config = Configuration.get_solo()

    context = {
        "html_id": html_id or "openforms-root",
        "base_url": config.api_root,
        "form_id": form_id,
        "base_path": base_path,
        "csp_nonce": csp_nonce,
        "lang": lang,
    }

    if config.use_sentry:
        try:
            from sentry_sdk import Hub

            opts = Hub.current.client.options

            context["sentry_dsn"] = opts.get("dsn")
            context["sentry_env"] = opts.get("environment")

        except ImportError:
            logger.exception(
                "Sentry integration is enabled but Sentry is not installed."
            )

    return render_to_string(template_name, context)


@register.simple_tag
def openforms_sdk_media():
    template_name = "openformsclient/templatetags/openforms_sdk_media.html"

    config = Configuration.get_solo()

    context = {
        "sdk_js_url": config.sdk_js_url,
        "sdk_css_url": config.sdk_css_url,
    }

    return render_to_string(template_name, context)


@register.simple_tag
def openforms_sdk_js():
    template_name = "openformsclient/templatetags/openforms_sdk_js.html"

    config = Configuration.get_solo()

    context = {
        "sdk_js_url": config.sdk_js_url,
    }

    return render_to_string(template_name, context)


@register.simple_tag
def openforms_sdk_css():
    template_name = "openformsclient/templatetags/openforms_sdk_css.html"

    config = Configuration.get_solo()

    context = {
        "sdk_css_url": config.sdk_css_url,
    }

    return render_to_string(template_name, context)
