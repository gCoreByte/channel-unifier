import asyncio
import yaml
from integrations.discord_hook import DiscordWebhook

def init_discord_webhooks(config_file_path):
    discord_webhooks = []
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for url in config.webhook_urls:
            discord_webhooks.append(DiscordWebhook(url))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_forever()