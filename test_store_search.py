import requests


def test_search_returns_items(store_url):
    response = requests.get(
        f"{store_url}/api/storesearch/",
        params={"term": "witcher", "cc": "us", "l": "english"},
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1
    for item in data["items"]:
        assert "id" in item
        assert "name" in item


def test_search_unknown_term(store_url):
    response = requests.get(
        f"{store_url}/api/storesearch/",
        params={"term": "zzzzqqqq12345", "cc": "us", "l": "english"},
        timeout=10,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []
