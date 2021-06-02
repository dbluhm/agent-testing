"""Example return route capable agent.

This example is intended to be run with the return_route_client to demonstrate
return routing.
"""

import hashlib
import os
from aiohttp import web
from aries_staticagent import StaticConnection, Target, crypto


def main():
    """Start a server with a static connection."""
    their_vk, _ = crypto.create_keypair(seed=hashlib.sha256(b"client").digest())
    conn = StaticConnection.from_seed(
        hashlib.sha256(b"server").digest(), Target(their_vk=their_vk)
    )

    # @conn.route('https://didcomm.org/basicmessage/1.0/message')
    # async def basic_message_auto_responder(msg, conn):
    #     await conn.send_async({
    #         "@type": "https://didcomm.org/"
    #                  "basicmessage/1.0/message",
    #         "~l10n": {"locale": "en"},
    #         "sent_time": utils.timestamp(),
    #         "content": "You said: {}".format(msg['content'])
    #     })

    async def handle(request):
        """aiohttp handle POST."""
        response = []
        with conn.session(response.append) as session:
            await conn.handle(await request.read(), session)

        if response:
            return web.Response(body=response.pop())

        raise web.HTTPAccepted()

    # @conn.route("https://example.com/test_protocol/0.1/test")
    # async def test_message(msg, conn):
    #     print("Received test message from client", msg)

    strings_list = []  # create empty list to store arbitrary strings
    # Add arbitrary strings from client to list

    @conn.route("https://example.com/manage-list/0.1/add")
    async def add_string(items, conn):
        item = items.get("item", "no item found")
        strings_list.append(item)

    # Respond to client's request to send the list of strings
    @conn.route("https://example.com/manage-list/0.1/get-list")
    async def return_list(message, conn):
        await conn.send_async(
            {"@type": "https://example.com/manage-list/0.1/list", "item": strings_list}
        )

    # Delete string from the list
    @conn.route("https://example.com/manage-list/0.1/delete")
    async def delete_item(message, conn):
        print("Deleting string of index", message["item"], "from the list.")
        strings_list.remove(strings_list[message["item"]])
        print("Updated list: ", strings_list)

    app = web.Application()
    app.add_routes([web.post("/", handle)])

    web.run_app(app, port=os.environ.get("PORT", 3000))


if __name__ == "__main__":
    main()
