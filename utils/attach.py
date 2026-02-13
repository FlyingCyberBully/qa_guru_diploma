import allure
from allure_commons.types import AttachmentType
from selene import browser


def add_screenshot():
    allure.attach(
        body=browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png',
    )


def add_logs():
    logs = browser.driver.get_log('browser')
    log_text = '\n'.join(str(entry) for entry in logs)
    allure.attach(
        body=log_text,
        name='browser_logs',
        attachment_type=AttachmentType.TEXT,
        extension='.log',
    )


def add_html():
    allure.attach(
        body=browser.driver.page_source,
        name='page_source',
        attachment_type=AttachmentType.HTML,
        extension='.html',
    )


def add_video(session_id: str, selenoid_url: str = ''):
    if not selenoid_url:
        return
    video_url = f'{selenoid_url}/video/{session_id}.mp4'
    html = (
        '<html><body>'
        f'<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video></body></html>'
    )
    allure.attach(
        body=html,
        name=f'video_{session_id}',
        attachment_type=AttachmentType.HTML,
        extension='.html',
    )
