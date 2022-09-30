import json
import pytest


class TestUserView:

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

    def test_user_get(self, client, tokens):
        responce = client.get(
            "/user/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        assert responce.status_code == 200
        data = responce.json
        assert data
        assert "email" in data
        assert data["email"] == "register_test_email"
        assert "password" not in data

    def test_user_patch(self, client, tokens):
        response = client.patch(
            "/user/",
            data=json.dumps({
                "name": "test_name",
            }),
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            },
            content_type='application/json',
        )

        assert response.status_code == 201

        response = client.get(
            "/user/",
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            }
        )

        data = response.json

        assert data
        assert "name" in data
        assert data["name"] == "test_name"

    def test_user_change_password(self, client, tokens):
        response = client.put(
            "/user/password/",
            data=json.dumps({
                "old_password": "register_TEST_password_123_!@#",
                "new_password": "register_TEST_password_123_!@#_new",
            }),
            headers={
                "Authorization": f"Bearer {tokens['access_token']}"
            },
            content_type='application/json',
        )

        assert response.status_code == 201

