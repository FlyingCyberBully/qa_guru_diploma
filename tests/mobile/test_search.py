import allure
import pytest

from wiki_mobile.screens.main_screen import MainScreen
from wiki_mobile.screens.onboarding_screen import OnboardingScreen

pytestmark = [
    pytest.mark.mobile,
    allure.epic('Mobile'),
    allure.feature('Search'),
]


@allure.story('Article Search')
class TestMobileSearch:

    @allure.title('Search for an article on Wikipedia')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_article(self):
        OnboardingScreen().pass_if_present()
        search_screen = MainScreen().open_search()
        search_screen.type_query('Python')
        search_screen.should_have_results()

    @allure.title('Search results contain expected text')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_results_content(self):
        OnboardingScreen().pass_if_present()
        search_screen = MainScreen().open_search()
        search_screen.type_query('Appium')
        search_screen.should_have_result_with_text('Appium')
