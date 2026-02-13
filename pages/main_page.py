import allure
from selene import browser, be


class MainPage:
    def __init__(self):
        self.search_input = browser.element('#search_v4')
        self.trending_section = browser.element('section.inner_content.trending')
        self.popular_section = browser.element('div.column_wrapper')
        self.nav_movies = browser.element('a[href="/movie"]')
        self.nav_tv = browser.element('a[href="/tv"]')
        self.nav_people = browser.element('a[href="/person"]')

    @allure.step('Open TMDB main page')
    def open(self):
        browser.open('/')
        return self

    @allure.step('Enter search query: "{query}"')
    def search(self, query: str):
        self.search_input.should(be.visible).type(query).press_enter()
        from pages.search_page import SearchResultsPage

        return SearchResultsPage()

    @allure.step('Verify search bar is displayed')
    def should_have_search_bar(self):
        self.search_input.should(be.visible)
        return self

    @allure.step('Verify trending section is displayed')
    def should_have_trending_section(self):
        self.trending_section.should(be.visible)
        return self

    @allure.step('Verify popular movies section is displayed')
    def should_have_popular_section(self):
        self.popular_section.should(be.visible)
        return self

    @allure.step('Verify navigation menu is present')
    def should_have_navigation(self):
        self.nav_movies.should(be.visible)
        self.nav_tv.should(be.visible)
        self.nav_people.should(be.visible)
        return self

    @allure.step('Navigate to Movies section')
    def go_to_movies(self):
        self.nav_movies.click()
        return self

    @allure.step('Navigate to People section')
    def go_to_people(self):
        self.nav_people.click()
        return self
