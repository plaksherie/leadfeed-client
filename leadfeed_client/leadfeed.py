import aiohttp

from leadfeed_client.client import LeadFeedClient
from leadfeed_client.methods.dialogs import LeadFeedDialogs
from leadfeed_client.methods.messages import LeadFeedMessages


class LeadFeed:
    _close_session = False

    def __init__(
            self,
            sesid: str,
            session: aiohttp.ClientSession = None
    ) -> None:
        if session is None:
            session = aiohttp.ClientSession()
            self._close_session = True

        self._session = session
        self._client = LeadFeedClient(sesid=sesid, session=session)

        self._dialogs = LeadFeedDialogs(self._client)
        self._messages = LeadFeedMessages(self._client)

    @property
    def dialogs(self) -> LeadFeedDialogs:
        return self._dialogs

    @property
    def messages(self) -> LeadFeedMessages:
        return self._messages

    async def __aenter__(self) -> "LeadFeed":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close_session()

    async def close_session(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()
