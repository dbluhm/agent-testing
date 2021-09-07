"""Bob client to return route capable agent.

Bob is intended to be run with he corresponding Alice server to
demonstrate return routing.
"""

import hashlib
import os
from aries_staticagent import StaticConnection, Target, crypto, utils

"""
from pydantic import (
    BaseModel,
)

class Item(BaseModel):
    name: str
    item_characteristics: str
"""


def main():
    """Send a message and await the reply."""
    their_vk, _ = crypto.create_keypair(seed=hashlib.sha256(b"server").digest())
    conn = StaticConnection.from_seed(
        hashlib.sha256(b"client").digest(),
        Target(
            their_vk=their_vk,
            endpoint="http://localhost:{}".format(os.environ.get("PORT", 3000)),
        ),
    )

    def list_addition():
        """Creates an item to be added to the list."""

        name = input("What do you want to name the" " item? : ")
        features = input("What features are in this" " item? : ")

        return {"Name": name, "Features": features}

    def delete_item():
        """Deletes an item from the given list"""

        item_del = input("What is the Item Number of item you" "want to delete? : ")
        return item_del

    """Here we ask the client what they want to do."""
    request = input("Hello! What do you need me to do? : ")

    # The qualifier will determine the message type.
    qualifier = ""

    if "add" in request:
        qualifier = "add"
        request = list_addition()
    elif "return" in request:
        qualifier = "get"
        request = "get_item"
    elif "delete" in request:
        qualifier = "delete"
        request = delete_item()

    reply = conn.send_and_await_returned(
        {
            "@type": "https://didcomm.org/basicmessage/1.0/" + qualifier,
            "~l10n": {"locale": "en"},
            "sent_time": utils.timestamp(),
            "content": request,
        },
        return_route="all",
    )
    print("Msg from conn:", reply and reply.pretty_print())


if __name__ == "__main__":
    main()
