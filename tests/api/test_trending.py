import allure
import pytest

from tmdb_api.models import SearchResponse

pytestmark = [
    pytest.mark.api,
    allure.epic('API'),
    allure.feature('Trending Movies'),
]


@allure.story('GET /trending/movie/week')
class TestTrending:

    @allure.title('Trending movies endpoint returns status 200')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_trending_movies_status(self, tmdb_client):
        response = tmdb_client.get_trending_movies()

        assert response.status_code == 200

    @allure.title('Trending movies response matches schema')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_trending_movies_schema(self, tmdb_client):
        response = tmdb_client.get_trending_movies()

        data = SearchResponse.model_validate(response.json())
        assert data.page >= 1
        assert data.total_results > 0

    @allure.title('Trending movies list is not empty')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_trending_movies_not_empty(self, tmdb_client):
        response = tmdb_client.get_trending_movies()

        data = SearchResponse.model_validate(response.json())
        assert len(data.results) > 0

    @allure.title('Each trending movie has required fields')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_trending_movies_have_required_fields(self, tmdb_client):
        response = tmdb_client.get_trending_movies()

        data = SearchResponse.model_validate(response.json())
        for movie in data.results[:5]:
            assert movie.id > 0
            assert len(movie.title) > 0
