"""
Test configuration and fixtures for AI2CUP backend tests.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def app():
    """Create a test application instance."""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client for HTTP requests."""
    with TestClient(app) as c:
        yield c
