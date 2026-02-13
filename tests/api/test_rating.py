import allure
import pytest

from tmdb_api.models import RateMovieRequest, RateMovieResponse

pytestmark = [
    pytest.mark.api,
    allure.epic('API'),
    allure.feature('Movie Rating'),
]

FIGHT_CLUB_ID = 550


@allure.story('POST /movie/{id}/rating')
class TestRateMovie:

    @allure.title('Rate a movie as a guest user')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rate_movie(self, tmdb_client, guest_session_id):
        request_body = RateMovieRequest(value=8.5)
        response = tmdb_client.rate_movie(
            FIGHT_CLUB_ID,
            request_body.model_dump(),
            guest_session_id,
        )

        assert response.status_code == 201
        data = RateMovieResponse.model_validate(response.json())
        assert data.success is True

    @allure.title('Rate movie with different values')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('rating', [0.5, 5.0, 10.0])
    def test_rate_movie_various_values(self, tmdb_client, guest_session_id, rating):
        allure.dynamic.parameter('rating', rating)
        request_body = RateMovieRequest(value=rating)
        response = tmdb_client.rate_movie(
            FIGHT_CLUB_ID,
            request_body.model_dump(),
            guest_session_id,
        )

        assert response.status_code in (200, 201)
        data = RateMovieResponse.model_validate(response.json())
        assert data.success is True


@allure.story('DELETE /movie/{id}/rating')
class TestDeleteRating:

    @allure.title('Delete a movie rating')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movie_rating(self, tmdb_client, guest_session_id):
        # Arrange — rate the movie first
        request_body = RateMovieRequest(value=7.0)
        tmdb_client.rate_movie(
            FIGHT_CLUB_ID,
            request_body.model_dump(),
            guest_session_id,
        )

        # Act — delete the rating
        response = tmdb_client.delete_movie_rating(
            FIGHT_CLUB_ID,
            guest_session_id,
        )

        # Assert
        assert response.status_code == 200
        data = RateMovieResponse.model_validate(response.json())
        assert data.success is True
