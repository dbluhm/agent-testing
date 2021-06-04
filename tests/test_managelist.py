"""Test the ManageListProtocol Handler in agent."""
from aries_staticagent import StaticConnection
import pytest


@pytest.mark.asyncio
async def test_retrievelist(connection: StaticConnection):
    await connection.send_async(
        {
            "@type": "https://example.com/" "manage-list/0.1/add",
            "item": "First test string.",
        }
    )
    await connection.send_async(
        {
            "@type": "https://example.com/" "manage-list/0.1/add",
            "item": "Second test string.",
        }
    )
    await connection.send_async(
        {
            "@type": "https://example.com/" "manage-list/0.1/add",
            "item": "Third test string.",
        }
    )
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://example.com/" "manage-list/0.1/get-list",
        },
        return_route="all",
    )
    assert reply["item"] == [
        "First test string.",
        "Second test string.",
        "Third test string.",
    ]


@pytest.mark.asyncio
async def test_deleteitem(connection: StaticConnection):
    reply = await connection.send_and_await_reply_async(
        {"@type": "https://example.com/" "manage-list/0.1/delete", "item": 1},
        return_route="all",
    )
    assert reply["content"] == ["First test string.", "Third test string."]
