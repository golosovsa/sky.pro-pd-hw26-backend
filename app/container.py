from app.dao import GenreDAO, DirectorDAO, MovieDAO, UserDAO, FavouriteMovieDAO

from app.services import GenreService, DirectorService, MovieService, UserService, FavouriteMovieService
from app.setup.db import db

# DAO
genre_dao = GenreDAO(db.session)
director_dao = DirectorDAO(db.session)
movie_dao = MovieDAO(db.session)
user_dao = UserDAO(db.session)
favourite_movie_dao = FavouriteMovieDAO(db.session)

# Services
genre_service = GenreService(dao=genre_dao)
director_service = DirectorService(dao=director_dao)
movie_service = MovieService(dao=movie_dao)
user_service = UserService(dao=user_dao)
favourite_movie_service = FavouriteMovieService(dao=favourite_movie_dao)
