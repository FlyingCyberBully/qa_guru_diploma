import allure
import requests

from config import settings
from utils.api_logging import allure_request_logger


class TMDBClient:
    def __init__(self):
        self.base_url = settings.api_base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                'Authorization': f'Bearer {settings.api_token}',
                'Content-Type': 'application/json;charset=utf-8',
            }
        )
        self.session.hooks['response'].append(allure_request_logger)

    @allure.step('GET /trending/movie/week')
    def get_trending_movies(self):
        return self.session.get(f'{self.base_url}/trending/movie/week')

    @allure.step('GET /search/movie — query="{query}"')
    def search_movie(self, query: str, page: int = 1):
        return self.session.get(
            f'{self.base_url}/search/movie',
            params={'query': query, 'page': page},
        )

    @allure.step('GET /movie/{movie_id}')
    def get_movie_details(self, movie_id: int):
        return self.session.get(f'{self.base_url}/movie/{movie_id}')

    @allure.step('GET /movie/{movie_id}/credits')
    def get_movie_credits(self, movie_id: int):
        return self.session.get(f'{self.base_url}/movie/{movie_id}/credits')

    @allure.step('GET /authentication/guest_session/new')
    def create_guest_session(self):
        return self.session.get(
            f'{self.base_url}/authentication/guest_session/new'
        )

    @allure.step('POST /movie/{movie_id}/rating')
    def rate_movie(self, movie_id: int, payload: dict, guest_session_id: str):
        return self.session.post(
            f'{self.base_url}/movie/{movie_id}/rating',
            params={'guest_session_id': guest_session_id},
            json=payload,
        )

    @allure.step('DELETE /movie/{movie_id}/rating')
    def delete_movie_rating(self, movie_id: int, guest_session_id: str):
        return self.session.delete(
            f'{self.base_url}/movie/{movie_id}/rating',
            params={'guest_session_id': guest_session_id},
        )
