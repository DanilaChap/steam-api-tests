# Steam Web & Storefront API Tests

Automated API tests for public Steam endpoints (`store.steampowered.com` and `api.steampowered.com`), written in Python with `pytest` and `requests`.

## What is covered

- **App Details (`/api/appdetails`)** — [test_app_details.py](./test_app_details.py)
  - Paid game metadata (`292030` — *The Witcher 3: Wild Hunt*): `success`, `type == "game"`, title, `is_free is False` (shared module-scoped fixture to avoid redundant calls and rate limits).
  - Price overview consistency: `currency == "USD"`, `initial` and `final` prices are integers (cents), `final <= initial`.
  - Free-to-play contract (`730` — *Counter-Strike 2*): `is_free is True`, `price_overview` key is absent.
  - Negative test (`appids=1`): HTTP `200` with `success: false` and no `data` key.
- **Store Search (`/api/storesearch/`)** — [test_store_search.py](./test_store_search.py)
  - Positive search (`term=witcher`): non-empty `items` list, `total >= 1`, each item contains `id` and `name`.
  - Empty search result (`term=zzzzqqqq12345`): `total == 0` and `items == []`.
- **Live Player Count (`/ISteamUserStats/GetNumberOfCurrentPlayers/v1/`)** — [test_player_count.py](./test_player_count.py)
  - Parametrized live player count check across 3 titles (`730` *Counter-Strike 2*, `292030` *The Witcher 3*, `1091500` *Cyberpunk 2077*): `result == 1` and `player_count > 0`.
  - Negative test (`appid=999999999`): HTTP `404` with `result == 42` and no `player_count` field.

## Tech stack

- Python 3.14
- pytest
- requests
- ruff
- GitHub Actions (CI)

## Project structure

- `conftest.py` — session-scoped fixtures for `store_url` and `api_url`
- `test_app_details.py` — storefront app details tests
- `test_store_search.py` — storefront search tests
- `test_player_count.py` — Steam Web API player stats tests
- `.github/workflows/tests.yml` — CI pipeline (linter + tests on push and PR)

## How to run

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the linter and tests:

   ```bash
   ruff check .
   python -m pytest -v
   ```
