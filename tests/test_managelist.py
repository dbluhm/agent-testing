"""Test the ManageListProtocol Handler in agent."""
from aries_staticagent import StaticConnection
import pytest


@pytest.mark.asyncio
async def test_retrievelist(connection: StaticConnection):
    items = ["first", "second", "third"]
    for item in items:
        await connection.send_async(
            {"@type": "https://example.com/manage-list/0.1/add", "item": item}
        )
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://example.com/" "manage-list/0.1/get-list",
        },
        return_route="all",
    )
    assert reply["item"] == items


@pytest.mark.asyncio
async def test_deleteitem(connection: StaticConnection):
    reply = await connection.send_and_await_reply_async(
        {"@type": "https://example.com/" "manage-list/0.1/delete", "item": 1},
        return_route="all",
    )
    assert reply["content"] == ["first", "third"]
