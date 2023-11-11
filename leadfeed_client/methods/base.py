from leadfeed_client.client import LeadFeedClient


class BaseMethod:
    def __init__(
            self,
            client: LeadFeedClient
    ) -> None:
        self._client = client
