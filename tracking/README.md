# Training Tracking

Tools for monitoring your Yatzy AI training runs: CSV logging, model checkpointing, and a live dashboard.

## Quick Start

```bash
# 1. Install dependencies (if you haven't already)
pip install -r requirements.txt

# 2. Start training (in one terminal)
python main.py

# 3. Watch progress (in another terminal)
streamlit run tracking/dashboard.py
```

## CSV Schema — `tracking/logs/training_log.csv`

Each row is one of two types, indicated by `row_type`:

| Column           | Type   | Description                                                                 |
|------------------|--------|-----------------------------------------------------------------------------|
| `timestamp`      | string | ISO-8601 timestamp (seconds precision)                                       |
| `generation`     | int    | Zero-indexed generation number                                               |
| `game_index`     | int?   | Index of the game within the evaluation (0–4). **Empty** on summary rows.    |
| `score`          | float  | For `game` rows: single game score. For `generation_summary`: population mean.|
| `row_type`       | string | `"game"` or `"generation_summary"`                                           |
| `model_filename` | string?| Filename of the saved checkpoint, if any. **Empty** unless a checkpoint was saved. |

### Row types

- **`game`** — One row per individual game played during evaluation. Every model in the population plays `GAMES_PER_EVAL` (default 5) games, each producing a row.
- **`generation_summary`** — One row per generation. Records the population-wide mean score. If the best model's mean score met the save threshold, `model_filename` links to the checkpoint.

## Checkpoints — `tracking/checkpoints/`

Model checkpoints are saved in Keras native format (`.keras`). Filename pattern:

```
gen_{generation}_{YYYYMMDD_HHMMSS}.keras
```

A checkpoint is only saved when the generation's best model has a mean evaluation score ≥ `SAVE_THRESHOLD` (default: 100, set in `tracking/checkpoints.py`).

### Tracing a checkpoint back to its stats

1. Open `training_log.csv`
2. Find the `generation_summary` row where `model_filename` matches your checkpoint filename
3. The `score` column shows the population mean for that generation
4. Filter `game` rows by the same `generation` to see individual game scores

## Dashboard

The Streamlit dashboard (`tracking/dashboard.py`) shows:

1. **Overview stats** — generation count, mean of generation averages, best/worst generation
2. **Line chart** — generation average score over time (trend line)
3. **Recent games** — last 50 individual game scores
4. **Checkpoints** — table of all saved model checkpoints with their scores

The dashboard auto-refreshes every 5 seconds. For the smoothest experience, install `streamlit-autorefresh`:

```bash
pip install streamlit-autorefresh
```

Without it, the dashboard falls back to `st.rerun()` with a sleep loop (works fine, just slightly less smooth).
