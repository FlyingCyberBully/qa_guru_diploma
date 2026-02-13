from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    overview: str = ''
    vote_average: float = 0.0
    release_date: str = ''
    poster_path: str | None = None


class MovieDetails(BaseModel):
    id: int
    title: str
    overview: str
    vote_average: float
    release_date: str
    runtime: int | None = None
    status: str = ''
    tagline: str = ''


class CastMember(BaseModel):
    id: int
    name: str
    character: str = ''


class CreditsResponse(BaseModel):
    id: int
    cast: list[CastMember] = []
