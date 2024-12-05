import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from organization_manager.db.database import get_db
from organization_manager.db.models.base import MasterBase
from organization_manager.main import app


class TestEndToEnd:
    @pytest.fixture(autouse=True)
    def init_test(self):
        """Setup test database and client"""
        # Create test database
        SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
        engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Create tables
        MasterBase.metadata.create_all(bind=engine)

        # Override the dependency
        def override_get_db():
            try:
                db = TestingSessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        # Create test client
        self.client = TestClient(app)

        # Store the session maker for test usage
        self.TestingSessionLocal = TestingSessionLocal

        yield

        # Cleanup
        MasterBase.metadata.drop_all(bind=engine)
        app.dependency_overrides.clear()

    def get_test_db(self):
        """Helper method to get db session for test setup"""
        db = self.TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
