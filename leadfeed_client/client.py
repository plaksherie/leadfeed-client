import asyncio
from typing import Dict, Any, Unpack

import aiohttp

from leadfeed_client.const import HttpMethod, ClientRequestKwarg, ClientKwarg, HttpStatusCode, HttpContentType
from leadfeed_client.exceptions import ClientConnectionException
from leadfeed_client.models.request_data import ClientRequestDataModel


class LeadFeedClient:

    def __init__(
            self,
            session: aiohttp.ClientSession,
            sesid: str,
            **kwargs: Unpack[ClientKwarg],
    ) -> None:
        self._base_request_data = ClientRequestDataModel(
            sesid=sesid,
            kwargs=kwargs,
        )
        self.sesid = sesid
        self._session = session
        self._loop = asyncio.get_running_loop()

    async def async_call_api(
            self,
            endpoint: str,
            *,
            data: Dict[str, Any] | str | None = None,
            headers: Dict[str, Any] | None = None,
            method: HttpMethod = HttpMethod.GET,
            params: Dict[str, Any] | None = None,
            timeout: int | None = None,
            **kwargs: Dict[ClientRequestKwarg, Any],
    ):
        request_arguments: Dict[str, Any] = {
            "url": self._base_request_data.request_url(endpoint),
            "method": kwargs.get(ClientRequestKwarg.METHOD, method).lower(),
            "params": params or kwargs.get(ClientRequestKwarg.PARAMS),
            "timeout": timeout or self._base_request_data.timeout,
            "data": data,
            "headers": {
                **(headers or {}),
                **self._base_request_data.headers,
                **(headers or {}),
                **kwargs.get("headers", {}),
            },
        }

        try:
            result = await self._session.request(**request_arguments)
        except (aiohttp.ClientError, asyncio.CancelledError) as exception:
            raise ClientConnectionException(
                "Request exception for "
                f"'{self._base_request_data.request_url(endpoint)}' with - {exception}"
            ) from exception

        except asyncio.TimeoutError:
            raise ClientConnectionException(
                f"Timeout of {self._base_request_data.timeout} reached while "
                f"waiting for {self._base_request_data.request_url(endpoint)}"
            ) from None

        if result.content_type == HttpContentType.BASE_HTML:
            return await result.json(encoding="utf-8", content_type=None)
        else:
            return await result.json(encoding="utf-8")
