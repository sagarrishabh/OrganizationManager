import pytest

from organization_manager.db.models import Organization
from tests.organization_manager.api.v1.endpoints.base import TestEndToEnd


class TestOrganization(TestEndToEnd):
    @pytest.fixture(autouse=True)
    def setup_organization(self, request):
        """Create a test organization and make it available to all tests"""
        db = next(self.get_test_db())
        organization_name = "Nava"
        organization = Organization(
            name=organization_name
        )
        db.add(organization)
        db.commit()
        db.refresh(organization)

        # Attach user data to the test instance
        self.test_organization = {
            "name": organization_name,
        }

        yield

        # Cleanup after test
        db.query(Organization).delete()
        db.commit()

    def test_create_organization(self):
        """Test successful login with correct credentials"""

        data = {
            "organization_name": "Test Organization",
            "email": "test_org@example.com",
            "password": "testpassword123"
        }

        response = self.client.post(
            "/org/create",
            json=data
        )
        assert response.status_code == 200

        expected_response = {'id': 2, 'name': 'Test Organization'}
        assert response.json() == expected_response

    def test_get_organization(self):
        """Test successful login with correct credentials"""
        response = self.client.get(
            "/org/get",
            params={
                "organization_name": self.test_organization["name"],
            }
        )
        assert response.status_code == 200
        expected_response = {'organizations': [{'id': 1, 'name': 'Nava'}]}
        assert response.json() == expected_response

    def test_get_organization_with_invalid_name(self):
        """Test successful login with correct credentials"""
        response = self.client.get(
            "/org/get",
            params={
                "organization_name": "Invalid Organization Name",
            }
        )
        assert response.status_code == 200
        expected_response = {'organizations': []}
        assert response.json() == expected_response
