import pytest


@pytest.fixture(scope="session")
def store_url():
    return "https://store.steampowered.com"


@pytest.fixture(scope="session")
def api_url():
    return "https://api.steampowered.com"
