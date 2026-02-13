import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


class SearchScreen:
    def __init__(self):
        self.search_input = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/search_src_text')
        )
        self.results = browser.all(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')
        )
        self.search_container = browser.element(
            (AppiumBy.ID, 'org.wikipedia.alpha:id/search_container')
        )

    @allure.step('Type search query: "{query}"')
    def type_query(self, query: str):
        self.search_input.should(be.visible).type(query)
        return self

    @allure.step('Verify search results are not empty')
    def should_have_results(self):
        self.results.should(have.size_greater_than(0))
        return self

    @allure.step('Verify results contain text: "{text}"')
    def should_have_result_with_text(self, text: str):
        self.results.first.should(have.text(text))
        return self

    @allure.step('Open first result')
    def open_first_result(self):
        self.results.first.click()
        from wiki_mobile.screens.article_screen import ArticleScreen

        return ArticleScreen()
