import pytest
from decouple import config

from openformsclient.client import Client

API_ROOT = config("OFC_API_ROOT", "https://open-forms.test.maykin.opengem.nl/api/v2/")
API_TOKEN = config("OFC_API_TOKEN", "hush-hush")


@pytest.fixture
def client():
    return Client(api_root=API_ROOT, api_token=API_TOKEN, client_timeout=2)


@pytest.fixture
def bogus_client():
    return Client(api_root=API_ROOT, api_token="bogus", client_timeout=2)
