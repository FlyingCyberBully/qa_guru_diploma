import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config import settings
from utils import attach


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    """Configure browser for UI tests (local or Selenoid)."""
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        f'--window-size={settings.window_width},{settings.window_height}'
    )

    if settings.remote_url:
        selenoid_capabilities = {
            'browserName': settings.browser_name,
            'browserVersion': settings.browser_version,
            'selenoid:options': {
                'enableVNC': True,
                'enableVideo': True,
            },
        }
        options.set_capability('selenoid:options', selenoid_capabilities['selenoid:options'])

        login = settings.selenoid_login
        password = settings.selenoid_password
        remote = settings.remote_url

        if login and password:
            remote = remote.replace('://', f'://{login}:{password}@')

        driver = webdriver.Remote(
            command_executor=remote,
            options=options,
        )
        browser.config.driver = driver
    else:
        # Ensure clean state (e.g. after mobile tests set browser.config.driver)
        browser.config.driver = None
        browser.config.driver_options = options

    browser.config.base_url = settings.ui_base_url
    browser.config.timeout = 10.0

    yield browser

    try:
        attach.add_screenshot()
    except Exception:
        pass

    try:
        attach.add_html()
    except Exception:
        pass

    if settings.remote_url:
        try:
            session_id = browser.driver.session_id
            attach.add_video(session_id, settings.remote_url)
        except Exception:
            pass

    browser.quit()
