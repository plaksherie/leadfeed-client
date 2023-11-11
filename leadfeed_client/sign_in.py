import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from leadfeed_client.const import UrlRoutes, BASE_API_URL
from leadfeed_client.utils import get_chrome_driver


class LeadFeedSignIn:
    selector_login_form = '#loginform'
    selector_field_login = '[name="login"]'
    selector_field_password = '[name="password"]'
    selector_sign_in_final = '.sidebar--logo'
    cookie_session_id_key = 'sesid'

    def __init__(
            self,
            login: str,
            password: str,
            delay_login: int
    ) -> None:
        self.login = login
        self.password = password
        self.delay_login = delay_login

    def start(
            self,
    ) -> str | None:
        chrome_driver = get_chrome_driver()
        chrome_driver.get(BASE_API_URL + UrlRoutes.LOGIN.value)
        form = WebDriverWait(chrome_driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_login_form))
        )
        form.find_element(By.CSS_SELECTOR, self.selector_field_login).send_keys(self.login)
        form.find_element(By.CSS_SELECTOR, self.selector_field_password).send_keys(self.password)
        WebDriverWait(chrome_driver, self.delay_login).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_sign_in_final))
        )
        sesid = None
        for cookie in chrome_driver.get_cookies():
            if cookie['name'] == self.cookie_session_id_key:
                sesid = cookie['value']
                break
        chrome_driver.close()
        chrome_driver.quit()
        return sesid
