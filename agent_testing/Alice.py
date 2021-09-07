"""Alice return route capable agent.

This server is meant to interpret the messages of the
corresponding Bob client and carry out their requests.
"""

import hashlib
import re
import os
from aiohttp import web
from aries_staticagent import StaticConnection, Target, crypto, utils, route


def main():

    """Start a server with a static connection."""
    their_vk, _ = crypto.create_keypair(seed=hashlib.sha256(b"client").digest())
    conn = StaticConnection.from_seed(
        hashlib.sha256(b"server").digest(), Target(their_vk=their_vk)
    )

    my_list = [{"name": "item1", "features": "feature1"}]

    def delete_item(item):
        # Deletes an item from the given list

        del my_list[int(item) - 1]

        response = {"Success!": "Item number " + str(item) + " deleted!"}
        return response

    """Make handlers for our three message types."""

    @conn.route("https://didcomm.org/basicmessage/1.0/add")
    # This handler will deal with the "add" message type.

    async def add_message_responder(msg, conn):

        new_item = {
            "Name": msg["content"]["Name"],
            "Features": msg["content"]["Features"],
        }

        my_list.append(new_item)
        response = {
            "Success!": "Item successfully added to list. "
            "Item number = " + str(my_list.index(new_item) + 1) + "."
        }

        await conn.send_async(
            {
                "@type": "https://didcomm.org/basicmessage/1.0/add",
                "~l10n": {"locale": "en"},
                "sent_time": utils.timestamp(),
                "content": "{}".format(response),
            }
        )

    @conn.route("https://didcomm.org/basicmessage/1.0/get")
    # This handler will deal with the "get" message type.

    async def get_message_responder(msg, conn):

        await conn.send_async(
            {
                "@type": "https://didcomm.org/basicmessage/1.0/get",
                "~l10n": {"locale": "en"},
                "sent_time": utils.timestamp(),
                "content": "{}".format(my_list),
            }
        )

    @conn.route("https://didcomm.org/basicmessage/1.0/delete")
    # This handler will deal with the "delete" message type.

    async def delete_message_responder(msg, conn):

        response = delete_item(msg["content"])

        await conn.send_async(
            {
                "@type": "https://didcomm.org/basicmessage/1.0/get",
                "~l10n": {"locale": "en"},
                "sent_time": utils.timestamp(),
                "content": "{}".format(response),
            }
        )

    async def handle(request):
        """aiohttp handle POST."""
        response = []

        with conn.session(response.append) as session:
            await conn.handle(await request.read(), session)

        if response:
            return web.Response(body=response.pop())

        raise web.HTTPAccepted()

    app = web.Application()
    app.add_routes([web.post("/", handle)])

    web.run_app(app, port=os.environ.get("PORT", 3000))


if __name__ == "__main__":
    main()
