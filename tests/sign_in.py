import os

from leadfeed_client import LeadFeedSignIn
from leadfeed_client.const import selenium_wire_storage
from tests.loader import config


sign_in = LeadFeedSignIn(
    config.leadfeed.login,
    config.leadfeed.password,
    config.selenium.delay_sign_in,
)


def test():
    sesid = sign_in.start()
    print(sesid)


if __name__ == '__main__':
    test()
