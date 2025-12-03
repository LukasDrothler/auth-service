import os
import pytest
from dotenv import load_dotenv
from src.database_service import DatabaseService
from src.auth_service import AuthService

# Load environment variables from .env file
load_dotenv()

# Set the RSA_KEYS_DIR to a local directory for tests
# This must be done before importing main, as main loads .env
os.environ["RSA_KEYS_DIR"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "keys")


@pytest.fixture(scope="function")
def db_service():
    """
    Fixture to provide a DatabaseService instance connected to a test database.
    This fixture ensures the test database is initialized and clean before each test.
    """
    # Set the database name to a test database
    original_db_name = os.environ.get("DB_NAME")
    os.environ["DB_NAME"] = "auth_test"

    service = DatabaseService()

    # Re-initialize the database schema to ensure a clean state for each test
    service.execute_init_db_sql()

    yield service

    # Restore original environment variable
    if original_db_name:
        os.environ["DB_NAME"] = original_db_name
    else:
        del os.environ["DB_NAME"]


@pytest.fixture(scope="session")
def auth_service():
    """
    Fixture to provide an AuthService instance.
    This service is stateless and can be shared across tests.
    """
    return AuthService()
