import allure
import pytest

from pages.main_page import MainPage

pytestmark = [
    pytest.mark.ui,
    allure.epic('UI'),
    allure.feature('Search'),
]


@allure.story('Movie Search')
class TestSearch:

    @allure.title('Search for a trending movie from API')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_trending_movie(self, trending_movie_title):
        """Uses TMDB API to get a trending movie, then searches for it in UI."""
        allure.dynamic.description(
            f'Searching for trending movie: {trending_movie_title}'
        )
        search_results = MainPage().open().search(trending_movie_title)
        search_results.should_have_results()

    @allure.title('Search for "{query}" returns results')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        'query',
        ['Fight Club', 'The Matrix', 'Inception'],
        ids=['fight_club', 'matrix', 'inception'],
    )
    def test_search_movie_parametrized(self, query):
        search_results = MainPage().open().search(query)
        search_results.should_have_results()
        search_results.should_have_movie(query)

    @allure.title('Search results page is loaded after search')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_results_page_loaded(self):
        search_results = MainPage().open().search('Interstellar')
        search_results.should_be_loaded()
