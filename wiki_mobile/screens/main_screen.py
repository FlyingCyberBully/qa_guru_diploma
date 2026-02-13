import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be


class MainScreen:
    def __init__(self):
        self.search_container = browser.element(
            (AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')
        )
        self.nav_explore = browser.element(
            (AppiumBy.ACCESSIBILITY_ID, 'Explore')
        )
        self.nav_saved = browser.element(
            (AppiumBy.ACCESSIBILITY_ID, 'Saved')
        )
        self.more_options = browser.element(
            (AppiumBy.ACCESSIBILITY_ID, 'More options')
        )

    @allure.step('Verify main screen is displayed')
    def should_be_visible(self):
        self.search_container.should(be.visible)
        return self

    @allure.step('Open search')
    def open_search(self):
        self.search_container.click()
        from wiki_mobile.screens.search_screen import SearchScreen

        return SearchScreen()
