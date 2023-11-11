import asyncio
import datetime
import logging
from typing import List

from leadfeed_client.const import UrlRoutes, HttpMethod
from leadfeed_client.methods.base import BaseMethod
from leadfeed_client.schemas import DialogsGetFormData, DialogsResponse, DialogType, DialogsFilterDate


class LeadFeedDialogs(BaseMethod):
    form_data = DialogsGetFormData(
        filter='all_dir',
        all=1,
        page=0,
    )

    async def get(
            self,
            page: int = 0,
            filter_date: DialogsFilterDate | None = None,
    ) -> DialogsResponse:
        self.form_data.page = page
        response = await self._client.async_call_api(
            endpoint=UrlRoutes.GET_DIALOGS.value,
            data=self.form_data.model_dump(),
            method=HttpMethod.POST,
        )
        dialogs = []
        for dialog in response['dialogs']:
            last_message_date = datetime.datetime.fromtimestamp(dialog['data_mes_u'])
            if filter_date:
                if last_message_date < filter_date.from_date:
                    continue
            dialogs.append(DialogType(
                thread_id=dialog['thread_id'],
                pk=dialog['pk'],
                inst_user=dialog['inst_user'],
                user_id=dialog['user_id'],
                name=dialog['name'],
                data_mes_u=last_message_date,
            ))
        dialogs = DialogsResponse(
            dialogs=dialogs,
            next_page=response['next_page']
        )
        logging.debug(f'Страница диалогов {page + 1}')
        return dialogs

    async def all(
            self,
            filter_date: DialogsFilterDate | None = None,
            timeout_between_page: int = 1
    ) -> List[DialogType]:
        all_dialogs = []
        next_page = -1
        page = 0
        while next_page != 0:
            dialogs = await self.get(page, filter_date=filter_date)
            all_dialogs.extend(dialogs.dialogs)
            next_page = dialogs.next_page
            page = dialogs.next_page
            if len(dialogs.dialogs) != 10:
                next_page = 0
            else:
                await asyncio.sleep(timeout_between_page)

        return all_dialogs
