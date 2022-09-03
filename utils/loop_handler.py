import asyncio


class LoopHandler:
    """Contains helper methods for the asyncio main event loop"""

    def __init__(self, discord_webhooks):
        """Initializes all of the Discord webhooks and the event loop"""
        self.discord_webhooks = discord_webhooks
        self.loop = asyncio.get_event_loop()

    def run_forever(self):
        """Begins the loop"""
        self.loop.run_forever()

    async def create_task(self, task):
        """Add additional tasks (eg integrations) to the loop"""
        self.loop.create_task(task)

    async def create_callback(self, callback):
        """Adds a callback, eg send_to_all"""
        self.loop.call_soon(callback)

    async def send_to_all(self, data: str, integration_name: str = "", username: str = "", avatar_url: str = None,
                          files: [] = None):
        """Sends the specified message to all added Discord webhooks"""
        for webhook in self.discord_webhooks:
            self.loop.create_task(webhook.send_to_user(data, integration_name, username, avatar_url, files))
