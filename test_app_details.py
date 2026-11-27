import pytest
import requests


@pytest.fixture(scope="module")
def witcher_details(store_url):
    response = requests.get(
        f"{store_url}/api/appdetails",
        params={"appids": 292030, "cc": "us", "l": "english"},
        timeout=10,
    )
    assert response.status_code == 200
    return response.json()["292030"]


def test_app_details_paid_game(witcher_details):
    assert witcher_details["success"] is True
    assert witcher_details["data"]["type"] == "game"
    assert "Witcher" in witcher_details["data"]["name"]
    assert witcher_details["data"]["is_free"] is False


def test_app_details_price_consistency(witcher_details):
    price = witcher_details["data"]["price_overview"]
    assert price["currency"] == "USD"
    assert isinstance(price["initial"], int)
    assert isinstance(price["final"], int)
    assert price["final"] <= price["initial"]


def test_app_details_free_game(store_url):
    response = requests.get(
        f"{store_url}/api/appdetails",
        params={"appids": 730, "cc": "us", "l": "english"},
        timeout=10,
    )
    assert response.status_code == 200
    app = response.json()["730"]
    assert app["success"] is True
    assert app["data"]["is_free"] is True
    assert "price_overview" not in app["data"]


def test_app_details_unknown_id(store_url):
    response = requests.get(
        f"{store_url}/api/appdetails",
        params={"appids": 1},
        timeout=10,
    )
    assert response.status_code == 200
    app = response.json()["1"]
    assert app["success"] is False
    assert "data" not in app
