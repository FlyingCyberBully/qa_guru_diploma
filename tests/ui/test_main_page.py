import allure
import pytest

from pages.main_page import MainPage

pytestmark = [
    pytest.mark.ui,
    allure.epic('UI'),
    allure.feature('Main Page'),
]


@allure.story('Page Elements')
class TestMainPageElements:

    @allure.title('Main page has a search bar')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_main_page_has_search_bar(self):
        MainPage().open().should_have_search_bar()

    @allure.title('Main page has a trending section')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_main_page_has_trending_section(self):
        MainPage().open().should_have_trending_section()

    @allure.title('Main page has navigation menu')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_main_page_has_navigation(self):
        MainPage().open().should_have_navigation()

    @allure.title('Main page shows popular movies')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_main_page_has_popular_section(self):
        MainPage().open().should_have_popular_section()
