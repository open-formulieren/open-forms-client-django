import logging
from typing import Tuple
from urllib.parse import urljoin

import requests
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, api_root, api_token):
        self.api_root = api_root
        self.api_token = api_token

    def _request(self, method, relative_url, **extra_kwargs):

        kwargs = {
            "headers": {"Authorization": f"Token {self.api_token}"},
            "timeout": 5,
        }
        kwargs.update(extra_kwargs)

        response = requests.request(
            method, urljoin(self.api_root, relative_url), **kwargs
        )

        return response

    def is_healthy(self) -> Tuple[bool, str]:
        """ """
        try:
            # We do a head request to actually hit a protected endpoint without
            # getting a whole bunch of data.
            response = self._request("head", "forms")
            response.raise_for_status()
            return (True, "")
        except HTTPError as e:
            # If something is wrong, we might get more information from the
            # error message provided by Open Forms.
            try:
                response = self._request("get", "forms")
                data = response.json()
                message = (
                    data.get("detail", data.get("title"))
                    or f"HTTP {response.status_code}"
                )
            except Exception:
                message = f"Server did not return a valid response (HTTP {e.response.status_code})."
        except Exception as e:
            logger.exception(e)
            message = str(e)

        return (False, message)

    def get_forms(self) -> list:
        """
        Retrieve all available forms in Open Forms API.

        :returns: The API response content as Python object.
        """
        response = self._request("get", "forms")
        response.raise_for_status()

        return response.json()

    def get_form(self, uuid_or_slug: str) -> dict:
        """
        Retrieve a specific form from the Open Forms API.

        :param uuid_or_slug: The UUID or the slug that identifies the form.
        :returns: The API response content as Python object.
        """
        response = self._request("get", f"forms/{uuid_or_slug}")
        response.raise_for_status()

        return response.json()
