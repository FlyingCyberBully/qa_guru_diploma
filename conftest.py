import pytest

from tmdb_api.client import TMDBClient
from tmdb_api.models import SearchResponse


@pytest.fixture(scope='session')
def trending_movie_title():
    """Fetch a trending movie title via TMDB API — used in UI tests."""
    client = TMDBClient()
    try:
        response = client.get_trending_movies()
        if response.status_code == 200:
            data = SearchResponse.model_validate(response.json())
            if data.results:
                return data.results[0].title
    except Exception:
        pass
    return 'Fight Club'
