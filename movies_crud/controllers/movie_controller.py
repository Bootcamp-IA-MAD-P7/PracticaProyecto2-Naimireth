from sqlalchemy.orm import Session
from movies_crud.schemas import movie_schema
from movies_crud.models.movie_model import Movie

class MovieController:

    @staticmethod
    def get_movies(db: Session):
        return db.query(Movie).all()

    @staticmethod 
    def get_movie_by_id(db: Session, movie_id: int):
        return db.query(Movie).filter(Movie.id == movie_id).first()

    @staticmethod
    def create_movie(db: Session, movie: movie_schema.MovieCreate):
        db_movie = Movie(title=movie.title, description=movie.description)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    @staticmethod
    def update_movie(db: Session, movie_id: int, movie: movie_schema.MovieCreate):
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if db_movie:
            db_movie.title = movie.title 
            db_movie.description = movie.description
            db.commit()
            db.refresh(db_movie)
        return db_movie
   
    @staticmethod
    def delete_movie(db: Session, movie_id: int):
        db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if db_movie:
            db.delete(db_movie)
            db.commit()
            return True
        return False