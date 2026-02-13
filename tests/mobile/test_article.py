import allure
import pytest

from wiki_mobile.screens.main_screen import MainScreen
from wiki_mobile.screens.onboarding_screen import OnboardingScreen

pytestmark = [
    pytest.mark.mobile,
    allure.epic('Mobile'),
    allure.feature('Article'),
]


@allure.story('View Article')
class TestArticle:

    @allure.title('Open article from search results')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_open_article_from_search(self):
        OnboardingScreen().pass_if_present()
        search_screen = MainScreen().open_search()
        search_screen.type_query('Python')
        search_screen.should_have_results()

        article = search_screen.open_first_result()
        article.should_be_visible()
