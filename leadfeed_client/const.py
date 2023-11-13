from enum import Enum, StrEnum, IntEnum
from typing import Dict, TypedDict
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from aiohttp.hdrs import CONTENT_TYPE, USER_AGENT

DEFAULT_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/121.0.0.0 Safari/537.36')

BASE_API_URL = 'https://leadfeed.ru'
LEADFEED_CDN_MEDIA = 'https://cdnnew.leadfeed.ru/bvc'


class UrlRoutes(Enum):
    LOGIN = '/dashboard'
    GET_DIALOGS = '/ajax_chat/get_dialogs'
    GET_DIALOG_MESSAGES = '/ajax_chat/get_dialog'


class ClientKwarg(StrEnum):
    """
    kwargs that are used by the client.

    These are used to construct the client and will affect all requests.

    HEADERS:
        Used to set the base headers for all requests.
    BASE_URL:
        Used to override the base url for all requests.
    TIMEOUT:
        Used to set the timeout for all requests. Defaults to 20
    CLIENT_NAME:
        This name will be used as the user agent header.
    """

    HEADERS = "headers"
    BASE_URL = "base_url"
    TIMEOUT = "timeout"
    CLIENT_NAME = "client_name"


class ClientRequestKwarg(StrEnum):
    """
    kwargs that are used by requests.

    HEADERS:
        Used to set the headers of the request.
    METHOD:
        Used to set the method of the request. Defaults to GET.
    PARAMS:
        Used to set the params of the request.
    """

    HEADERS = "headers"
    METHOD = "method"
    PARAMS = "params"


class HttpStatusCode(IntEnum):
    """HTTP Status codes."""

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE = 203
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    RATELIMIT = 403
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class HttpMethod(StrEnum):
    """HTTP Methods."""

    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"
    PUT = "PUT"


class HttpContentType(StrEnum):
    """HTTP Content Types."""

    BASE_HTML = "text/html"
    BASE_JSON = "application/json"
    BASE_ZIP = "application/zip"
    BASE_GZIP = "application/x-gzip"
    BASE_FORM = 'application/x-www-form-urlencoded'

    JSON = "application/json;charset=utf-8"
    TEXT_PLAIN = "text/plain;charset=utf-8"
    TEXT_HTML = "text/html; charset=utf-8"


HTTP_STATUS_CODE_GOOD_LIST: list[HttpStatusCode] = [
    HttpStatusCode.OK,
    HttpStatusCode.CREATED,
    HttpStatusCode.ACCEPTED,
    HttpStatusCode.NON_AUTHORITATIVE,
]

BASE_API_HEADERS: Dict[str, str] = {
    CONTENT_TYPE: HttpContentType.BASE_FORM.value,
    USER_AGENT: DEFAULT_USER_AGENT,
}


try:
    selenium_service = Service(executable_path=ChromeDriverManager().install())
    selenium_options = webdriver.ChromeOptions()
except Exception as e:
    selenium_service = Service(executable_path=EdgeChromiumDriverManager().install())
    selenium_options = webdriver.EdgeOptions()
