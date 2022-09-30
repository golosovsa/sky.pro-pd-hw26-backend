import json

import pytest

from app.dao import UserDAO
from app.services import UserService


class TestAuthView:

    @pytest.fixture
    def user_service(self, db):
        return UserService(UserDAO(db.session))

    def test_auth_registration_post(self, client, user_service):
        response = client.post(
            "/auth/register/",
            data=json.dumps(dict(
                email="register_test_email",
                password="register_TEST_password_123_!@#"
            )),
            content_type='application/json'
        )

        assert response.status_code == 201
        assert "location" in response.headers

    def test_auth_login_post(self, client, user_service):
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

        assert response.status_code == 201
        tokens = response.json
        assert "access_token" in tokens
        assert "refresh_token" in tokens

    def test_auth_login_put(self, client, user_service):
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

        refresh_token = response.json["refresh_token"]
        response = client.put(
            "/auth/login/",
            data={"refresh_token": refresh_token},
            content_type='multipart/form-data'
        )

        assert response.status_code == 201
        tokens = response.json
        assert "access_token" in tokens
        assert "refresh_token" in tokens
