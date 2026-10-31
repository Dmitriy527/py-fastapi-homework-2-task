from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import get_db, MovieModel
from database.models import CountryModel, GenreModel, ActorModel, LanguageModel
from schemas import MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_list_movies(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    movies = await db.scalars(
        select(MovieModel).order_by(MovieModel.id.desc()).offset(offset).limit(per_page)
    )
    page_movies = movies.all()
    total_items = await db.scalar(
        select(func.count(MovieModel.id)).select_from(MovieModel)
    )
    prev_page = None
    next_page = None

    if not page_movies:
        raise HTTPException(404, "No movies found.")

    if total_items % per_page == 0:
        total_pages = total_items // per_page + 1
    else:
        total_pages = total_items // per_page

    if page > 1:
        prev_page = f"/api/v1/theater/movies/?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"/api/v1/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=page_movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )
