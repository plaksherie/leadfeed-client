import re
from typing import Union, List

from seleniumwire import webdriver

from leadfeed_client.const import selenium_service, selenium_options


def get_chrome_driver() -> webdriver.Chrome:
    return webdriver.Chrome(service=selenium_service, options=selenium_options)


def get_cdn_links_from_text(
        text: str,
) -> List[str]:
    return re.findall(r'https?://cdnnew\.leadfeed\.ru\S+', text)


def is_null_field(
        media: Union[str, None],
):
    return not media or media == 'NULL'
