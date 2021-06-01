"""Fixtures and other common code."""

import pytest


# This will require a session scoped event loop
@pytest.fixture(scope="session")
async def connection():
    """Start up agent and yield a connection to it."""
