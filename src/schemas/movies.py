from pydantic import BaseModel
from datetime import date


class MovieDetailSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    overview: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
