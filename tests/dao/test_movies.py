import datetime
from typing import List

import pytest

from app.dao import MovieDAO
from app.dao.models import Movie


class TestMoviesDAO:

    @pytest.fixture()
    def movies_dao(self, db):
        return MovieDAO(db.session)

    @pytest.fixture()
    def movie_1(self, db):
        model = Movie(
            title="Утомленные солнцем",
            description="Российско-французская картина 1994 года - лауреат премии 'Оскар' за "
                        "'Лучший фильм на иностранном языке', также она получила Гран-при 47-го "
                        "Каннского фестиваля. По российскому телевидению фильм был впервые показан "
                        "21 октября 1995 года - в 50-летний юбилей Никиты Михалкова. Действие фильма "
                        "разворачивается в 1936 году, незадолго до начала сталинских репрессий. "
                        "В картине снимались сам Михалков, Игнеборга Дапкунайте, Олег Меньшиков, "
                        "Надя Михалкова.",
            trailer="https://www.youtube.com/watch?v=6JsFEMUtNM4",
            year=1994,
            rating=7.7,
            genre_id=1,
            director_id=1
        )
        db.session.add(model)
        db.session.commit()
        return model

    @pytest.fixture()
    def movie_2(self, db):
        model = Movie(
            title="Профиль",
            description="Британская журналистка, работающая под прикрытием, внедряется в систему пропаганды "
                        "«Исламского государства», которое привлекает в свои ряды все больше молодых европейских "
                        "женщин. Ежедневные контакты с вербовщиками террористов затягивают ее.",
            trailer="https://www.youtube.com/watch?v=DKgW8UcGMNk",
            year=2018,
            rating=7.1,
            genre_id=2,
            director_id=2
        )
        db.session.add(model)
        db.session.commit()
        return model

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []

    def test_movies_updatable_fields(self, movies_dao):
        assert "title" in movies_dao.__updatable_fields__
        assert "description" in movies_dao.__updatable_fields__
        assert "trailer" in movies_dao.__updatable_fields__
        assert "year" in movies_dao.__updatable_fields__
        assert "rating" in movies_dao.__updatable_fields__
        assert "genre_id" in movies_dao.__updatable_fields__
        assert "director_id" in movies_dao.__updatable_fields__

    def test_movies_create(self, movies_dao):
        movie = Movie(
            title="test_create_genre",
            description="test_create_genre",
            trailer="test_create_genre",
            year=202020,
            rating=100.100,
            genre_id=999,
            director_id=999,
        )
        movies_dao.create(movie)
        assert movies_dao.get_by_id(movie.id) == movie

    def test_movies_delete(self, movies_dao, movie_1):
        pk = movie_1.id
        movies_dao.delete(movie_1)
        assert movies_dao.get_by_id(pk) is None

    def test_movies_update(self, movies_dao, movie_1):
        movie_1.title = "test_update_movie"
        movie_1.description = "test_update_movie"
        movie_1.trailer = "test_update_movie"
        movie_1.year = 202020
        movie_1.rating = 100.100
        movie_1.genre_id = 999
        movie_1.director_id = 999

        movies_dao.update(movie_1)

        movie = movies_dao.get_by_id(movie_1.id)

        assert movie.title == "test_update_movie"
        assert movie.description == "test_update_movie"
        assert movie.trailer == "test_update_movie"
        assert movie.year == 202020
        assert movie.rating == 100.100
        assert movie.genre_id == 999
        assert movie.director_id == 999

    def test_get_all_movies_and_order_by_newest(self, movies_dao):
        movie_2022 = Movie(
            title="2022",
            description="2022",
            trailer="2022",
            year=2022,
            rating=100.100,
            genre_id=999,
            director_id=999,
        )
        movie_2023 = Movie(
            title="2023",
            description="2023",
            trailer="2023",
            year=2023,
            rating=100.100,
            genre_id=999,
            director_id=999,
        )
        movie_2024 = Movie(
            title="2024",
            description="2024",
            trailer="2024",
            year=2024,
            rating=100.100,
            genre_id=999,
            director_id=999,
        )
        movies_dao.create(movie_2022)
        movies_dao.create(movie_2023)
        movies_dao.create(movie_2024)

        movie_2022.created = datetime.datetime(year=2022, month=1, day=1)
        movie_2023.created = datetime.datetime(year=2023, month=1, day=1)
        movie_2024.created = datetime.datetime(year=2024, month=1, day=1)

        movies_dao.update(movie_2022)
        movies_dao.update(movie_2023)
        movies_dao.update(movie_2024)

        models: List[Movie] = movies_dao.get_all_and_order_by_newest()

        assert models[0] == movie_2024
        assert models[1] == movie_2023
        assert models[2] == movie_2022
