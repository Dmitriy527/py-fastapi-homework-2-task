from decimal import Decimal
from importlib.metadata import requires

from pydantic import BaseModel, Field, condecimal, field_validator
from datetime import date

from sqlalchemy import Float

from database.models import (
    MovieStatusEnum,
    CountryModel,
    GenreModel,
    ActorModel,
    LanguageModel,
)


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


class MovieRequestSchema(BaseModel):
    name: str
    date: date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float = Field(ge=0)
    revenue: float = Field(ge=0)

    @field_validator("budget", "revenue", mode="before")
    @classmethod
    def convert_to_float(cls, v):
        if isinstance(v, (Decimal, str)):
            return float(v)
        return v

    country: str = Field(description="ISO 3166-1 alpha-3 code", examples=["UKR"])
    genres: list[str]
    actors: list[str]
    languages: list[str]


class CountrySchema(BaseModel):
    id: int
    code: str
    name: str | None = Field(default=None, description="Country name")

    class Config:
        from_attributes = True


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActorSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LanguageSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieReturnSchema(MovieRequestSchema):
    id: int
    country: CountrySchema
    genres: list[GenreSchema]
    actors: list[ActorSchema]
    languages: list[LanguageSchema]

    class Config:
        from_attributes = True


class MovieRequestDetailSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float = Field(ge=0)
    revenue: float = Field(ge=0)
    country: str = Field(description="ISO 3166-1 alpha-3 code", examples=["UKR"])
    genres: list[str]
    actors: list[str]
    languages: list[str]
    country: CountrySchema
    genres: list[GenreSchema]
    actors: list[ActorSchema]
    languages: list[LanguageSchema]

    class Config:
        from_attributes = True
