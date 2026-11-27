import pytest
import requests


@pytest.mark.parametrize("appid", [730, 292030, 1091500])
def test_player_count_popular_game(api_url, appid):
    response = requests.get(
        f"{api_url}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
        params={"appid": appid},
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()["response"]
    assert data["result"] == 1
    assert isinstance(data["player_count"], int)
    assert data["player_count"] > 0


def test_player_count_unknown_app(api_url):
    response = requests.get(
        f"{api_url}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
        params={"appid": 999999999},
        timeout=10,
    )
    assert response.status_code == 404
    data = response.json()["response"]
    assert data["result"] == 42
    assert "player_count" not in data
