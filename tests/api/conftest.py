import pytest

from tmdb_api.client import TMDBClient


@pytest.fixture(scope='session')
def tmdb_client():
    """Provide a TMDB API client for the entire test session."""
    return TMDBClient()


@pytest.fixture(scope='session')
def guest_session_id(tmdb_client):
    """Create a guest session and return its ID."""
    response = tmdb_client.create_guest_session()
    assert response.status_code == 200, 'Failed to create guest session'
    return response.json()['guest_session_id']
