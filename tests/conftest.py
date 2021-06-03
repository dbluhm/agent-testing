"""Fixtures and other common code."""

import asyncio
from contextlib import suppress
import hashlib

from aries_staticagent import StaticConnection, crypto, Target
import pytest

from agent_testing.agent import Agent


@pytest.fixture(scope="session")
def event_loop():
    """Create a session scoped event loop.

    pytest.asyncio plugin provides a default function scoped event loop
    which cannot be used as a dependency to session scoped fixtures.
    """
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def agent():
    """Yield connection to the agent under test."""
    agent = Agent()
    yield agent


@pytest.fixture(scope="session", autouse=True)
async def http_endpoint(agent: Agent):
    """Start up agent and yield a connection to it."""
    server_task = asyncio.ensure_future(agent.start_async())

    yield

    server_task.cancel()
    with suppress(asyncio.CancelledError):
        await server_task
    await agent.cleanup()


@pytest.fixture(scope="session")
async def connection(agent):
    their_vk, _ = crypto.create_keypair(seed=hashlib.sha256(b"server").digest())
    yield StaticConnection.from_seed(
        hashlib.sha256(b"client").digest(),
        Target(
            their_vk=their_vk, endpoint="http://{}:{}".format(agent.host, agent.port)
        ),
    )
