from app.config import config
from app.dao.models import Genre, Director, Movie, FavouriteMovies, User
from app.server import create_app, db


app = create_app(config)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "FavoriteMovies": FavouriteMovies,
        "User": User,
    }
