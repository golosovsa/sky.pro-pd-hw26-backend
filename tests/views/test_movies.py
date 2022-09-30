import pytest

from app.dao.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie(self, db):
        obj = Movie(
            id=1,
            title='test_movie_1_title',
            description='test_movie_1_description',
            trailer='test_movie_1_trailer',
            year=2000,
            rating=8.0,
            genre_id=1,
            director_id=1,
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [{
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "trailer": movie.trailer,
            "year": movie.year,
            "rating": movie.rating,
            "genre_id": movie.genre_id,
            "director_id": movie.director_id,
            "director": {
                "id": None,
                "name": None
            },
            "genre": {
                "id": None,
                "name": None
            },
        }]

    def test_movie_pages(self, client, movie):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movie(self, client, movie):
        response = client.get(f"/movies/1/")
        assert response.status_code == 200
        assert response.json == {
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "trailer": movie.trailer,
            "year": movie.year,
            "rating": movie.rating,
            "genre_id": movie.genre_id,
            "director_id": movie.director_id,
            "director": {
                "id": None,
                "name": None
            },
            "genre": {
                "id": None,
                "name": None
            },
        }

    def test_movie_not_found(self, client, movie):
        response = client.get("/movies/999/")
        assert response.status_code == 404
