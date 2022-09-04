from utils.loop_handler import LoopHandler
import yaml
from integrations.discord_hook import DiscordWebhook
from integrations.zulip.zulip_wrapper import Zulip


def init_discord_webhooks(config_file_path: str):
    webhooks = []
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for url in config['discord']['webhook_urls']:
            webhooks.append(DiscordWebhook(url))
    return webhooks

def init_zulip_hooks(config_file_path: str, loop_handler: LoopHandler):
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for zulip_config in config['zulip']:
            api_key = zulip_config['api_key']
            domain = zulip_config['domain']
            email = zulip_config['email']
            zulip = Zulip(loop=loop_handler, email=email, api_key=api_key, domain=domain)
            loop_handler.create_task(zulip.run())


if __name__ == '__main__':
    # Initialise classes
    discord_webhooks = init_discord_webhooks("config/discord_config.yml")

    loop = LoopHandler(discord_webhooks=discord_webhooks)
    # Add to integrations to loop
    zulip_integrations = init_zulip_hooks("config/zulip_config.yml", loop)

    # Event loop start
    loop.run_forever()
