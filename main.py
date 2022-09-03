from utils.loop_handler import LoopHandler
import yaml
from integrations.discord_hook import DiscordWebhook


def init_discord_webhooks(config_file_path):
    webhooks = []
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for url in config['discord']['webhook_urls']:
            webhooks.append(DiscordWebhook(url))
    return webhooks


if __name__ == '__main__':
    # Initialise classes
    discord_webhooks = init_discord_webhooks("config/discord_config.yml")

    loop = LoopHandler(discord_webhooks=discord_webhooks)
    # Add to integrations to loop

    # Event loop start
    loop.run_forever()