"""Example return route capable agent.

This example is intended to be run with the return_route_client to demonstrate
return routing.
"""

from datetime import datetime
import hashlib
from aiohttp import web
from aries_staticagent import StaticConnection, Target, crypto
from aries_staticagent.module import Module, route


class BaseAgent:
    """Simple Agent class.

    Used to start up an agent with statically configured handlers.
    """

    def __init__(self, host: str, port: int, connection: StaticConnection):
        """Initialize BaseAgent."""
        self.host = host
        self.port = port
        self.connection = connection
        self._runner = None

    async def handle_web_request(self, request: web.Request):
        """Handle HTTP POST."""
        response = []
        with self.connection.session(response.append) as session:
            await self.connection.handle(await request.read(), session)

        if response:
            return web.Response(body=response.pop())

        raise web.HTTPAccepted()

    async def start_async(self):
        """Start the agent listening for HTTP POSTs."""
        app = web.Application()
        app.add_routes([web.post("/", self.handle_web_request)])
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def cleanup(self):
        """Clean up async start."""
        await self.runner.cleanup()

    def start(self):
        """Start sychronously."""
        app = web.Application()
        app.add_routes([web.post("/", self.handle_web_request)])

        web.run_app(app, port=self.port)

    def register_modules(self, *modules: Module):
        """Register modules on connection."""
        for module in modules:
            self.connection.route_module(module)


class BasicMessageCounter(Module):
    """A simple BasicMessage module.
    Responds with the number of messages received.
    """

    DOC_URI = "https://didcomm.org/"
    PROTOCOL = "basicmessage"
    VERSION = "1.0"

    def __init__(self):
        super().__init__()
        self.count = 0

    @route
    async def message(self, _msg, conn):
        """Respond to basic messages with a count of messages received."""
        self.count += 1
        await conn.send_async(
            {
                "@type": self.type("message"),
                "~l10n": {"locale": "en"},
                "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": "{} message(s) received.".format(self.count),
            }
        )


class ManageListProtocol(Module):
    """List management protocol handlers."""

    DOC_URI = "https://example.com/"
    PROTOCOL = "manage-list"
    VERSION = "0.1"

    def __init__(self):
        """Initialize ManageListProtocol and state."""
        super().__init__()
        self.strings_list = []  # create empty list to store arbitrary strings

    @route("https://example.com/manage-list/0.1/add")
    async def add_string(self, items, conn):
        item = items.get("item", "no item found")
        self.strings_list.append(item)

    # Respond to client's request to send the list of strings
    @route("https://example.com/manage-list/0.1/get-list")
    async def return_list(self, message, conn):
        await conn.send_async(
            {
                "@type": "https://example.com/manage-list/0.1/list",
                "item": self.strings_list,
            }
        )

    # Delete string from the list
    @route("https://example.com/manage-list/0.1/delete")
    async def delete_item(self, message, conn):
        self.strings_list.remove(self.strings_list[message["item"]])
        await conn.send_async(
            {
                "@type": "https://example.com/manage-list/0.1/delete",
                "content": self.strings_list,
            }
        )


class Agent(BaseAgent):
    """Our cool agent that does list management protocol."""

    HOST = "localhost"
    PORT = 3000

    def __init__(self):
        their_vk, _ = crypto.create_keypair(seed=hashlib.sha256(b"client").digest())
        conn = StaticConnection.from_seed(
            hashlib.sha256(b"server").digest(), Target(their_vk=their_vk)
        )
        super().__init__(self.HOST, self.PORT, conn)
        manage_list = ManageListProtocol()
        basic_message = BasicMessageCounter()
        self.register_modules(manage_list, basic_message)


def main():
    """Start our cool agent."""
    agent = Agent()
    agent.start()


if __name__ == "__main__":
    main()
