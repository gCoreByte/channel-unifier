from urllib.parse import urlparse, urlunparse


def replace_for_current(endpoint: str, domain: str):
    """Replaces the example URL with a valid one"""
    parsed = urlparse(endpoint)
    return urlunparse(parsed._replace(netloc=domain))
