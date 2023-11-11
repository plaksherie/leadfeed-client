import datetime
import html
import json
import re

from leadfeed_client.const import UrlRoutes, HttpMethod
from leadfeed_client.enums.media import MediaTypeEnum
from leadfeed_client.methods.base import BaseMethod
from leadfeed_client.schemas import MessagesGetFormData, MessageType, MessageMediaType, MessageMediaImageType, \
    MessageMediaVideoType, DialogsFilterDate
from leadfeed_client.utils import get_cdn_links_from_text, is_null_field


class LeadFeedMessages(BaseMethod):
    form_data = None

    async def get(
            self,
            form_data: MessagesGetFormData,
            filter_date: DialogsFilterDate | None = None,
    ):
        self.form_data = form_data
        messages = []
        response = await self._client.async_call_api(
            endpoint=UrlRoutes.GET_DIALOG_MESSAGES.value,
            data=self.form_data.model_dump(),
            method=HttpMethod.POST,
        )
        for message in response['dialog']:
            message_date = datetime.datetime.strptime(message['data_mes'], "%Y-%m-%d %H:%M:%S")
            if filter_date:
                if message_date < filter_date.from_date:
                    continue
            text = html.unescape(message['text'])
            media_type = message['media_type']
            media_raw = message['media']
            media = None
            if not is_null_field(media_type) and not is_null_field(media_raw):
                media_ = json.loads(html.unescape(media_raw))
                if media_type == MediaTypeEnum.IMAGE.value:
                    media = MessageMediaType(
                        image=MessageMediaImageType(url=media_['url'])
                    )
                elif media_type == MediaTypeEnum.VIDEO.value:
                    media = MessageMediaType(
                        video=MessageMediaVideoType(url=media_['video']['url'])
                    )

            messages.append(MessageType(
                text=text,
                username=message['username'],
                media=media,
                media_type=message['media_type'],
                cdn_links=get_cdn_links_from_text(text),
                item_type=message['item_type'],
                date=message_date,
                owner=message['in'] == 0
            ))
        return messages
