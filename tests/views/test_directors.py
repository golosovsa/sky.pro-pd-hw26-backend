import pytest

from app.dao.models import Director


class TestDirectorsView:
    @pytest.fixture
    def director(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, director):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    def test_director_pages(self, client, director):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/directors/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_director(self, client, director):
        response = client.get(f"/directors/1/")
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    def test_director_not_found(self, client, director):
        response = client.get("/directors/999/")
        assert response.status_code == 404
