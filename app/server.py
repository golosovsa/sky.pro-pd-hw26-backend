from flask import Flask, jsonify, render_template
from flask_cors import CORS

from app.exceptions import BaseServiceError
from app.setup.api import api
from app.setup.db import db, migrate
from app.views import auth_ns, user_ns, genres_ns, directors_ns, movies_ns, favourites_ns


# from app.dao.models import Genre, Director, User, Movie, FavouriteMovies


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    print(app.config["SQLALCHEMY_DATABASE_URI"])

    @app.route("/")
    def index():
        return "OK", 200

    CORS(app=app)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # with app.app_context():
    #     Genre.prepare(db.engine)
    #     Director.prepare(db.engine)
    #     User.prepare(db.engine)
    #     Movie.prepare(db.engine)
    #     FavoriteMovies.prepare(db.engine)

    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(favourites_ns)

    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app
