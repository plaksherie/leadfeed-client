import re
from typing import Union, List

from selenium import webdriver

from leadfeed_client.const import selenium_service, selenium_options, selenium_wire_options


def get_selenium_driver() -> webdriver.Chrome | webdriver.Edge:
    if isinstance(selenium_options, webdriver.ChromeOptions):
        return webdriver.Chrome(service=selenium_service, options=selenium_options)
    else:
        return webdriver.Edge(service=selenium_service, options=selenium_options)


def get_cdn_links_from_text(
        text: str,
) -> List[str]:
    return re.findall(r'https?://cdnnew\.leadfeed\.ru\S+', text)


def is_null_field(
        media: Union[str, None],
):
    return not media or media == 'NULL'
