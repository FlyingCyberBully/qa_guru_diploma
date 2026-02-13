import allure
import pytest

from pages.movie_page import MoviePage

pytestmark = [
    pytest.mark.ui,
    allure.epic('UI'),
    allure.feature('Movie Page'),
]

FIGHT_CLUB_ID = 550


@allure.story('Movie Details Display')
class TestMoviePage:

    @allure.title('Movie page displays correct title')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_movie_page_displays_title(self):
        MoviePage().open(FIGHT_CLUB_ID).should_have_title('Fight Club')

    @allure.title('Movie page displays overview')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_movie_page_displays_overview(self):
        movie_page = MoviePage().open(FIGHT_CLUB_ID)
        movie_page.should_have_overview_containing('soap')

    @allure.title('Movie page shows user score')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_movie_page_shows_user_score(self):
        MoviePage().open(FIGHT_CLUB_ID).should_have_user_score()
