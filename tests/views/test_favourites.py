import json
import pytest

from app.dao.models import FavouriteMovies

class TestFavoritesView:

    @pytest.fixture
    def tokens(self, client):
        data = json.dumps(dict(
            email="register_test_email",
            password="register_TEST_password_123_!@#"
        ))

        response = client.post(
            "/auth/register/",
            data=data,
            content_type='application/json'
        )

        response = client.post(
            "/auth/login/",
            data=data,
            content_type='application/json'
        )

        return response.json

    @pytest.fixture
    def user_1(self, client, tokens):
        response = client.get(
            "/user/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        return response.json

    @pytest.fixture
    def favorite_1(self, app, user_1, db):
        with app.app_context():
            favourite = FavouriteMovies(user_id=user_1["id"], movie_id=1)
            db.session.add(favourite)
            db.session.commit()
        return favourite

    @pytest.fixture
    def favorite_2(self, app, user_1, db):
        with app.app_context():
            favourite = FavouriteMovies(user_id=user_1["id"], movie_id=2)
            db.session.add(favourite)
            db.session.commit()
        return favourite

    def test_get(self, client, tokens, user_1, favorite_1, favorite_2):
        response = client.get(
            "/favorites/movies/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert response.status_code == 200
        data = response.json
        assert data
        assert isinstance(data, list)
        assert len(data) == 2
        assert data == [
            {"user_id": user_1["id"], "movie_id": 1},
            {"user_id": user_1["id"], "movie_id": 2},
        ]

    def test_get_one(self, client, tokens, user_1, favorite_1):
        response = client.get(
            "/favorites/movies/1/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert response.status_code == 200
        data = response.json
        assert data
        assert isinstance(data, dict)
        assert "user_id" in data
        assert data["user_id"] == user_1["id"]
        assert "movie_id" in data
        assert data["movie_id"] == 1

    def test_post(self, client, tokens, user_1, favorite_1, favorite_2):
        response = client.post(
            "/favorites/movies/3/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert response.status_code == 201

        response = client.post(
            "/favorites/movies/4/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert response.status_code == 201

        response = client.get(
            "/favorites/movies/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        data = response.json
        assert len(data) == 4

    def test_delete(self, client, tokens, user_1, favorite_1, favorite_2):
        response = client.delete(
            f"/favorites/movies/{user_1['id']}/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert response.status_code == 204

        response = client.get(
            "/favorites/movies/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        data = response.json
        assert len(data) == 1
