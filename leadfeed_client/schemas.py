import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from leadfeed_client.utils import is_null_field


class MediaEnum(Enum):
    VOICE = 'voice'
    VIDEO = 'video'
    PHOTO = 'photo'


class DialogsGetFormData(BaseModel):
    filter: str
    all: int
    page: int
    query: int = 0
    ts: int = 0
    uids: str = ''


class MessagesGetFormData(BaseModel):
    inst_user: str
    pk: str
    thread_id: str


class MessageMediaImageType(BaseModel):
    url: str


class MessageMediaVideoType(BaseModel):
    url: str


class MessageMediaType(BaseModel):
    image: Optional[MessageMediaImageType] = None
    video: Optional[MessageMediaVideoType] = None


class MessageItemType(Enum):
    TEXT = 'text'
    LINK = 'link'
    MEDIA = 'media'


class MessageType(BaseModel):
    text: str
    username: str
    date: datetime.datetime
    media: Union[MessageMediaType, None] = None
    media_type: Union[str, None] = None
    cdn_links: List[str]
    item_type: MessageItemType
    owner: bool

    def is_media(
            self,
    ) -> bool:
        return not is_null_field(self.media_type)


class DialogType(BaseModel):
    thread_id: str
    pk: str
    inst_user: str
    user_id: str
    name: str
    data_mes_u: datetime.datetime


class DialogsResponse(BaseModel):
    dialogs: List[DialogType]
    next_page: int


class DialogsFilterDate(BaseModel):
    from_date: datetime.datetime
