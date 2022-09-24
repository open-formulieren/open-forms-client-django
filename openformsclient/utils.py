import logging

logger = logging.getLogger(__name__)


def get_form_choices(client=None):
    if client is None:
        from .models import Configuration

        config = Configuration.get_solo()
        client = config.client

    response = client.get_forms()
    return sorted(
        [(item["uuid"], item["name"]) for item in response],
        key=lambda entry: entry[1],
    )
