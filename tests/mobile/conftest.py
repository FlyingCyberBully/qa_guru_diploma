import os
from contextlib import contextmanager

import allure
import pytest
import requests
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from selene import browser, support

from wiki_mobile.config import get_mobile_config, BStackConfig


@contextmanager
def _allure_step(title, **kwargs):
    """Wrapper around allure.step that ignores extra kwargs (e.g. params)."""
    with allure.step(title):
        yield


@pytest.fixture(scope='function', autouse=True)
def mobile_driver():
    """Configure Appium driver for mobile tests (local or BrowserStack)."""
    context = os.getenv('MOBILE_CONTEXT', 'bstack')
    config = get_mobile_config(context)

    options = UiAutomator2Options()

    if isinstance(config, BStackConfig):
        capabilities = config.to_capabilities()
        options.load_capabilities(capabilities)
        remote_url = config.remote_url
    else:
        options.set_capability('platformName', config.platform_name)
        options.set_capability('deviceName', config.device_name)
        options.set_capability('app', config.app)
        options.set_capability('appWaitActivity', config.app_wait_activity)
        remote_url = config.remote_url

    driver = appium_webdriver.Remote(remote_url, options=options)

    browser.config.driver = driver
    browser.config.timeout = config.timeout
    browser.config._wait_decorator = support._logging.wait_with(
        context=_allure_step
    )

    yield browser

    _attach_allure_artifacts(context, config, driver.session_id)

    driver.quit()
    # Reset selene browser so subsequent test suites (UI) get a fresh driver
    browser.config.driver = None


def _attach_allure_artifacts(context, config, session_id):
    """Attach screenshot and (optionally) BrowserStack video to Allure."""
    try:
        allure.attach(
            body=browser.driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG,
            extension='.png',
        )
    except Exception:
        pass

    try:
        allure.attach(
            body=browser.driver.page_source,
            name='page_source',
            attachment_type=allure.attachment_type.XML,
            extension='.xml',
        )
    except Exception:
        pass

    if isinstance(config, BStackConfig):
        _attach_bstack_video(config, session_id)


def _attach_bstack_video(config: BStackConfig, session_id: str):
    """Fetch and attach BrowserStack video to Allure."""
    try:
        bstack_session = requests.get(
            f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
            auth=(config.bstack_user, config.bstack_key),
            timeout=15,
        ).json()
        video_url = bstack_session.get('automation_session', {}).get('video_url', '')
        if video_url:
            html = (
                '<html><body>'
                f'<video width="100%" height="100%" controls autoplay>'
                f'<source src="{video_url}" type="video/mp4">'
                '</video></body></html>'
            )
            allure.attach(
                body=html,
                name='video',
                attachment_type=allure.attachment_type.HTML,
                extension='.html',
            )
    except Exception:
        pass
