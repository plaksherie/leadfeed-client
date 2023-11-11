from dataclasses import dataclass
from typing import Dict, Any, Unpack
from aiohttp.hdrs import COOKIE, USER_AGENT

from leadfeed_client.const import ClientKwarg, BASE_API_URL, BASE_API_HEADERS


@dataclass
class ClientRequestDataModel:
    """Dataclass to hold base request details."""

    kwargs: Unpack[ClientKwarg]
    sesid: str

    def request_url(self, endpoint: str) -> str:
        """Generate full request url."""
        return f"{self.base_url}{endpoint}"

    @property
    def timeout(self) -> int:
        """Return timeout."""
        return self.kwargs.get(ClientKwarg.TIMEOUT) or 20

    @property
    def base_url(self) -> str:
        """Return the base url."""
        return self.kwargs.get(ClientKwarg.BASE_URL) or BASE_API_URL

    @property
    def headers(self) -> Dict[str, str]:
        """Return base request headers."""
        headers = BASE_API_HEADERS.copy()
        if self.sesid:
            headers[COOKIE] = f"sesid={self.sesid}"
        if kwarg_headers := self.kwargs.get(ClientKwarg.HEADERS):
            headers.update(kwarg_headers)
        if client_name := self.kwargs.get(ClientKwarg.CLIENT_NAME):
            headers[USER_AGENT] = client_name
        return headers
