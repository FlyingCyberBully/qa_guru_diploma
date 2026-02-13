from pydantic import BaseModel

from tmdb_api.models.movie import Movie


class SearchResponse(BaseModel):
    page: int
    results: list[Movie]
    total_pages: int
    total_results: int
