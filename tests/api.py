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
            inst_user='61894893230',
            pk='50494207657',
            thread_id='4f47304e2889e7ff4a1ab16d37eb4809'
        ),
        # filter_date=DialogsFilterDate(
        #     from_date=datetime.datetime(2023, 11, 9, 3, 39, 0)
        # )
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
