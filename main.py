from integrations.campuswire.campuswire_wrapper import Campuswire
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
    zulip_integrations = []
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for zulip_config in config['zulip']:
            api_key = zulip_config['api_key']
            domain = zulip_config['domain']
            email = zulip_config['email']
            zulip = Zulip(loop=loop_handler, email=email, api_key=api_key, domain=domain)
            zulip_integrations.append(zulip)
    return zulip_integrations
def init_campuswire_hooks(config_file_path: str, loop_handler: LoopHandler):
    campuswire_integrations = []
    with open(config_file_path, mode="r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
        for campuswire_config in config['campuswire']:
            email = campuswire_config['email']
            password = campuswire_config['password']
            campuswire = Campuswire(loop=loop_handler, email=email, password=password)
            campuswire_integrations.append(campuswire)
    return campuswire_integrations


if __name__ == '__main__':
    # Initialise classes
    discord_webhooks = init_discord_webhooks("config/discord_config.yml")

    loop = LoopHandler(discord_webhooks=discord_webhooks)
    # Add to integrations to loop
    zulip_integrations = init_zulip_hooks("config/zulip_config.yml", loop)
    campuswire_integrations = init_campuswire_hooks("config/campuswire_config.yml", loop)
    for zulip in zulip_integrations:
        loop.create_task(zulip.run())
    for campuswire in campuswire_integrations:
        loop.create_task(campuswire.run())
    # Event loop start
    loop.run_forever()
