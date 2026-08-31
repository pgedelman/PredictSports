# PredictSports

Scrapes 30+ years of historical NFL game data, stores it in MySQL, and trains an LSTM (PyTorch) to predict game outcomes from team performance trends.

**Status:** work in progress / learning project. Data collection, cleaning, and model training are functional; there's no served API or UI yet — everything runs through the notebooks below.

## How it works

1. **Collect** — Playwright/Selenium + BeautifulSoup scrape box scores and per-game team stats (passing, rushing, third-down conversions, time of possession, etc.) from [pro-football-reference.com](https://www.pro-football-reference.com/) back to 1966, and load them into MySQL (`backend/collect_data.ipynb`).
2. **Clean** — `backend/data_cleanup.ipynb` and `backend/backfill_game_location.py` find and patch missing/inconsistent rows (nulls, home/away flags, etc.) left by scraping edge cases.
3. **Train** — `backend/training/training.ipynb` builds rolling team-performance features from the stored games and trains an LSTM to predict outcomes.

## Project structure

```
PredictSports/
├── backend/
│   ├── input_data.py              # scraping/parsing helpers shared by the notebooks
│   ├── collect_data.ipynb         # scrapes games + team stats into MySQL
│   ├── data_cleanup.ipynb         # finds/fixes bad or missing rows
│   ├── backfill_game_location.py  # one-off script to patch a missing column
│   ├── training/
│   │   └── training.ipynb         # feature engineering + LSTM training
│   └── requirements.txt
├── database/
│   └── schema.sql                 # MySQL schema
└── LICENSE
```

## Tech stack

- **Data collection:** Playwright, Selenium, BeautifulSoup, Requests
- **Database:** MySQL
- **Modeling:** PyTorch, scikit-learn, pandas

## Setup

### Database

```sql
mysql -u root -p < database/schema.sql
```

Create a `.env` in `backend/`:

```
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=predict_sports
BASE_URL=https://www.pro-football-reference.com/
```

### Scraping / cleaning / training

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # or `source venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
playwright install          # first time only, downloads browser binaries
```

Then run, in order: `collect_data.ipynb` → `data_cleanup.ipynb` → `training/training.ipynb`.

## License

MIT — see [LICENSE](LICENSE).
