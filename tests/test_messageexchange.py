"""Test the MessageExchangeProtocol Handler in agent."""
from aries_staticagent import StaticConnection
import pytest


@pytest.mark.asyncio
async def test_first_message(connection: StaticConnection):
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://example.com/message-exchange/0.1/message1",
            "item": "Hi! I'd like to learn more about blockchain.",
        },
        return_route="all",
    )
    assert (
        reply["content"] == "Blockchain is a type of database that stores information "
        "in a decentralized, distributed digital ledger."
    )


@pytest.mark.asyncio
async def test_second_message(connection: StaticConnection):
    reply = await connection.send_and_await_reply_async(
        {
            "@type": "https://example.com/message-exchange/0.1/message2",
            "item": "Why is this a good way of transferring information?",
        },
        return_route="all",
    )
    assert (
        reply["content"] == "Data is recorded in a way that is transparent, time "
        "stamped, and immutable. (Type one of the previous words to learn more.)"
    )


@pytest.mark.asyncio
async def test_third_message(connection: StaticConnection):
    # Response_options: 'transparent', 'time stamped', 'immutable'
    choice = "immutable"
    if choice.lower() == "transparent":
        reply = await connection.send_and_await_reply_async(
            {
                "@type": "https://example.com/message-exchange/0.1/message3",
                "item": choice,
            },
            return_route="all",
        )
        assert (
            reply["content"]
            == "This means that everyone can see that there was a transaction."
        )
    elif choice.lower() == "time stamped":
        reply = await connection.send_and_await_reply_async(
            {
                "@type": "https://example.com/message-exchange/0.1/message3",
                "item": choice,
            },
            return_route="all",
        )
        assert (
            reply["content"]
            == "This means that everyone can see when the transaction was made."
        )
    elif choice.lower() == "immutable":
        reply = await connection.send_and_await_reply_async(
            {
                "@type": "https://example.com/message-exchange/0.1/message3",
                "item": choice,
            },
            return_route="all",
        )
        assert (
            reply["content"]
            == "This means that no one can alter previous transactions "
            "or information on the ledger."
        )
    else:
        reply = await connection.send_and_await_reply_async(
            {
                "@type": "https://example.com/message-exchange/0.1/message3",
                "item": choice,
            },
            return_route="all",
        )
        assert (
            reply["content"] == "Sorry, we didn't understand your request! Please type "
            "'transparent', 'time stamped', 'immutable' (not case sensitive)."
        )
