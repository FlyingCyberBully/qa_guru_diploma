import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be


class OnboardingScreen:
    def __init__(self):
        self.title = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/primaryTextView')
        )
        self.continue_button = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_forward_button')
        )
        self.skip_button = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')
        )
        self.done_button = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_done_button')
        )

    @allure.step('Verify onboarding screen is displayed')
    def should_be_visible(self):
        self.title.should(be.visible)
        return self

    @allure.step('Skip onboarding')
    def skip(self):
        self.skip_button.click()
        return self

    @allure.step('Proceed through onboarding')
    def proceed(self):
        for _ in range(3):
            self.continue_button.click()
        self.done_button.click()
        return self

    @allure.step('Pass onboarding if present')
    def pass_if_present(self):
        try:
            self.skip_button.should(be.visible)
            self.skip()
        except Exception:
            pass
        return self
