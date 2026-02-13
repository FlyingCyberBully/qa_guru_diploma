import allure
import pytest

from tmdb_api.models import GuestSessionResponse

pytestmark = [
    pytest.mark.api,
    allure.epic('API'),
    allure.feature('Authentication'),
]


@allure.story('Guest Session')
class TestAuthentication:

    @allure.title('Create a new guest session')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_guest_session(self, tmdb_client):
        response = tmdb_client.create_guest_session()

        assert response.status_code == 200
        data = GuestSessionResponse.model_validate(response.json())
        assert data.success is True
        assert len(data.guest_session_id) > 0

    @allure.title('Guest session has expiration date')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.NORMAL)
    def test_guest_session_has_expiration(self, tmdb_client):
        response = tmdb_client.create_guest_session()

        data = GuestSessionResponse.model_validate(response.json())
        assert len(data.expires_at) > 0
