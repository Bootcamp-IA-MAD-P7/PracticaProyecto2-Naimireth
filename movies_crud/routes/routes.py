from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from movies_crud.controllers.movie_controller import MovieController
from movies_crud.schemas import movie_schema
from movies_crud.database.database import get_db

router = APIRouter()

@router.post("/movies/", response_model=movie_schema.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_new_movie(movie: movie_schema.MovieCreate, db: Session = Depends(get_db)):
    return MovieController.create_movie(db, movie)

@router.get("/movies/", response_model=List[movie_schema.MovieResponse])
def read_all_movies(db: Session = Depends(get_db)):
    return MovieController.get_movies(db)

@router.get("/movies/{movie_id}", response_model=movie_schema.MovieResponse)
def read_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieController.get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/movies/{movie_id}", response_model=movie_schema.MovieResponse)
def update_existing_movie(movie_id: int, movie: movie_schema.MovieCreate, db: Session = Depends(get_db)):
    updated_movie = MovieController.update_movie(db, movie_id, movie)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_movie(movie_id: int, db: Session = Depends(get_db)):
    deleted = MovieController.delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None