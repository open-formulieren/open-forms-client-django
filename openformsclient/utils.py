import logging

logger = logging.getLogger(__name__)


def get_form_choices(client=None, use_uuids=False):
    if client is None:
        from .models import Configuration

        config = Configuration.get_solo()
        client = config.client

    if not client.has_config():
        return []

    response = client.get_forms()

    key = "uuid" if use_uuids else "slug"
    return sorted(
        [(item[key], item["name"]) for item in response],
        key=lambda entry: entry[1],
    )
