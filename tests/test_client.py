from urllib.parse import urljoin

import pytest
import vcr
from requests.exceptions import HTTPError

from openformsclient.client import Client

from .data.forms import test_form

CASSETTE_PATH_FORMS = "fixtures/cassettes/forms.yaml"
CASSETTE_PATH_INVALID = "fixtures/cassettes/invalid.yaml"
VCR_DEFAULTS = {
    "record_mode": "none",  # use new_episodes to record casettes
    "filter_headers": ["authorization"],
}


def test_client_has_config(client):
    bogus_client = Client("", "", "")

    assert client.has_config()
    assert not bogus_client.has_config()


@vcr.use_cassette(CASSETTE_PATH_FORMS, **VCR_DEFAULTS)
def test_client_is_healthy(client):
    health, msg = client.is_healthy()
    assert health
    assert msg == ""


@vcr.use_cassette(CASSETTE_PATH_FORMS, **VCR_DEFAULTS)
def test_get_forms(client):
    results = client.get_forms()["results"]

    assert test_form in results


@vcr.use_cassette(CASSETTE_PATH_INVALID, **VCR_DEFAULTS)
def test_get_forms_unauthorized(bogus_client):
    url = urljoin(bogus_client.api_root, "public/forms")
    msg = f"401 Client Error: Unauthorized for url: {url}"

    with pytest.raises(HTTPError, match=msg):
        bogus_client.get_forms()


@vcr.use_cassette(CASSETTE_PATH_FORMS, **VCR_DEFAULTS)
def test_get_single_form(client):
    result = client.get_form(uuid_or_slug=test_form["uuid"])

    assert result["uuid"] == test_form["uuid"]
    assert result["name"] == test_form["name"]


@vcr.use_cassette(CASSETTE_PATH_FORMS, **VCR_DEFAULTS)
def test_get_single_form_not_found(client):
    bogus_uuid = "aaaa-bbbb-cccc-dddd"
    url = urljoin(client.api_root, f"forms/{bogus_uuid}")
    msg = f"404 Client Error: Not Found for url: {url}"

    with pytest.raises(HTTPError, match=msg):
        client.get_form(uuid_or_slug=bogus_uuid)


@vcr.use_cassette(CASSETTE_PATH_INVALID, **VCR_DEFAULTS)
def test_get_single_form_unauthorized(bogus_client):
    url = urljoin(bogus_client.api_root, f"forms/{test_form['uuid']}")
    msg = f"401 Client Error: Unauthorized for url: {url}"

    with pytest.raises(HTTPError, match=msg):
        bogus_client.get_form(uuid_or_slug=test_form["uuid"])
