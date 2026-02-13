import allure
import pytest

from tmdb_api.models import SearchResponse

pytestmark = [
    pytest.mark.api,
    allure.epic('API'),
    allure.feature('Search Movies'),
]


@allure.story('GET /search/movie')
class TestSearchAPI:

    @allure.title('Search for "{query}" returns results')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize('query', ['Matrix', 'Inception', 'Interstellar'])
    def test_search_movie_returns_results(self, tmdb_client, query):
        allure.dynamic.parameter('query', query)
        response = tmdb_client.search_movie(query)

        assert response.status_code == 200
        data = SearchResponse.model_validate(response.json())
        assert data.total_results > 0
        assert len(data.results) > 0

    @allure.title('Search results contain the queried movie title')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_results_contain_title(self, tmdb_client):
        query = 'Fight Club'
        response = tmdb_client.search_movie(query)

        data = SearchResponse.model_validate(response.json())
        titles = [movie.title for movie in data.results]
        assert any('Fight Club' in title for title in titles)

    @allure.title('Search with empty query returns empty results')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.MINOR)
    def test_search_empty_query(self, tmdb_client):
        response = tmdb_client.search_movie('')

        assert response.status_code == 200
        data = SearchResponse.model_validate(response.json())
        assert data.total_results == 0
