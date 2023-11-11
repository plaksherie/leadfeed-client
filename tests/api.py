import asyncio
import datetime
import logging

from leadfeed_client import LeadFeed
from leadfeed_client.schemas import MessagesGetFormData, DialogsFilterDate
from tests.loader import config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)d #%(levelname)-8s "
           "[%(asctime)s] - %(name)s - %(message)s",
)


async def dialogs():
    leadfeed = LeadFeed(
        config.leadfeed.sesid
    )
    all_dialogs = await leadfeed.dialogs.all(
        filter_date=DialogsFilterDate(
            from_date=datetime.datetime(2023, 11, 9, 17, 39, 0)
        )
    )
    print(all_dialogs)


async def messages():
    leadfeed = LeadFeed(
        config.leadfeed.sesid
    )
    get_messages = await leadfeed.messages.get(
        MessagesGetFormData(
            inst_user='62108841494',
            pk='58057136675',
            thread_id='7781feff2acafb6a7836e08a9ebdb8a3'
        ),
        filter_date=DialogsFilterDate(
            from_date=datetime.datetime(2023, 11, 9, 3, 39, 0)
        )
    )
    print(get_messages)


async def dialog():
    leadfeed = LeadFeed(
        config.leadfeed.sesid
    )
    page = await leadfeed.dialogs.get(
        filter_date=DialogsFilterDate(
            from_date=datetime.datetime(2023, 11, 11, 1, 9, 0)
        )
    )
    print(page)


if __name__ == '__main__':
    # asyncio.run(dialogs())
    # asyncio.run(dialog())
    asyncio.run(messages())
