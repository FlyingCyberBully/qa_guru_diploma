import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


class ArticleScreen:
    def __init__(self):
        self.close_dialog = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/closeButton')
        )
        self.action_bar = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/action_bar_root')
        )

    @allure.step('Dismiss dialog if present')
    def dismiss_dialog(self):
        try:
            self.close_dialog.should(be.visible)
            self.close_dialog.click()
        except Exception:
            pass
        return self

    @allure.step('Verify article screen is displayed')
    def should_be_visible(self):
        self.dismiss_dialog()
        self.action_bar.should(be.visible)
        return self

    @allure.step('Verify article title contains: "{expected_title}"')
    def should_have_title(self, expected_title: str):
        self.action_bar.should(have.text(expected_title))
        return self
