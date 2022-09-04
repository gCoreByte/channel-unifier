from typing import List
import aiohttp
from discord import Webhook


class DiscordWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def send_as_user(self, data: str, integration_name: str = "", username: str = "", avatar_url: str = None,
                           files: List = None):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(url=self.webhook_url, session=session)

            # default files
            if files is None:
                files = []

            # name is either INTEGRATIONNAME-USERNAME or the default webhook name
            name = '-'.join([integration_name, username])
            if len(name) == 1:
                name = webhook.name
            # default url
            avatar_url = avatar_url if avatar_url else webhook.display_avatar.url

            await webhook.send(data, username=name, avatar_url=avatar_url, files=files)
            await session.close()
