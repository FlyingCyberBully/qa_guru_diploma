from pydantic import BaseModel, Field


class RateMovieRequest(BaseModel):
    value: float = Field(..., ge=0.5, le=10.0)


class RateMovieResponse(BaseModel):
    success: bool
    status_code: int
    status_message: str
