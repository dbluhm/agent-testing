"""Test the BasicMessage Handler in agent."""
from datetime import datetime
from aries_staticagent import StaticConnection
import pytest


@pytest.mark.asyncio
async def test_basicmessage(connection: StaticConnection):
    """Test basicmessage handler responds."""
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://didcomm.org/" "basicmessage/1.0/message",
            "~l10n": {"locale": "en"},
            "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": "The Cron script has been executed.",
        },
        return_route="all",
    )
    assert reply["content"] == "1 message(s) received."
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://didcomm.org/" "basicmessage/1.0/message",
            "~l10n": {"locale": "en"},
            "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": "Some other message.",
        },
        return_route="all",
    )
    assert reply["content"] == "2 message(s) received."
