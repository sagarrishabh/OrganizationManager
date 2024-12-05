import pytest

from organization_manager.db.models import User
from organization_manager.utils.hash_password import hash_password
from tests.organization_manager.api.v1.endpoints.base import TestEndToEnd


class TestLogin(TestEndToEnd):
    @pytest.fixture(autouse=True)
    def setup_user(self, request):
        """Create a test user and make it available to all tests"""
        db = next(self.get_test_db())
        password = "testpassword123"
        hashed_password = hash_password(password)

        user = User(
            email="test@example.com",
            hashed_password=str(hashed_password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Attach user data to the test instance
        self.test_user = {
            "email": "test@example.com",
            "password": password,
            "user_id": user.id
        }

        yield

        # Cleanup after test
        db.query(User).delete()
        db.commit()

    def test_login_successful(self):
        """Test successful login with correct credentials"""
        response = self.client.post(
            "/admin/login",
            json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["access_token"] is not None

    def test_login_invalid_password(self):
        """Test login with invalid password"""
        response = self.client.post(
            "/admin/login",
            json={
                "email": self.test_user["email"],
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 400
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_email(self):
        """Test login with non-existent email"""
        response = self.client.post(
            "/admin/login",
            json={
                "email": "nonexistent@example.com",
                "password": self.test_user["password"]
            }
        )

        assert response.status_code == 400
        assert "User not found" in response.json()["detail"]

    def test_login_empty_credentials(self):
        """Test login with empty credentials"""
        response = self.client.post(
            "/admin/login",
            json={
                "email": "",
                "password": ""
            }
        )

        assert response.status_code == 422

    def test_login_invalid_email_format(self):
        """Test login with invalid email format"""
        response = self.client.post(
            "/admin/login",
            json={
                "email": "invalid-email",
                "password": self.test_user["password"]
            }
        )

        assert response.status_code == 422
