import allure
import pytest

from tmdb_api.models import MovieDetails, CreditsResponse

pytestmark = [
    pytest.mark.api,
    allure.epic('API'),
    allure.feature('Movie Details'),
]

FIGHT_CLUB_ID = 550


@allure.story('GET /movie/{id}')
class TestMovieDetails:

    @allure.title('Get movie details by ID')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movie_details(self, tmdb_client):
        response = tmdb_client.get_movie_details(FIGHT_CLUB_ID)

        assert response.status_code == 200
        data = MovieDetails.model_validate(response.json())
        assert data.title == 'Fight Club'
        assert data.id == FIGHT_CLUB_ID

    @allure.title('Movie details contain overview')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_movie_details_have_overview(self, tmdb_client):
        response = tmdb_client.get_movie_details(FIGHT_CLUB_ID)

        data = MovieDetails.model_validate(response.json())
        assert len(data.overview) > 0

    @allure.title('Non-existent movie returns 404')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_movie_not_found(self, tmdb_client):
        response = tmdb_client.get_movie_details(999999999)

        assert response.status_code == 404


@allure.story('GET /movie/{id}/credits')
class TestMovieCredits:

    @allure.title('Get movie credits')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_credits(self, tmdb_client):
        response = tmdb_client.get_movie_credits(FIGHT_CLUB_ID)

        assert response.status_code == 200
        data = CreditsResponse.model_validate(response.json())
        assert len(data.cast) > 0

    @allure.title('Fight Club credits include Brad Pitt')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.MINOR)
    def test_fight_club_cast_contains_brad_pitt(self, tmdb_client):
        response = tmdb_client.get_movie_credits(FIGHT_CLUB_ID)

        data = CreditsResponse.model_validate(response.json())
        actor_names = [member.name for member in data.cast]
        assert 'Brad Pitt' in actor_names
