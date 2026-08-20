"""
CSV logging utility for training progress.

Writes one row per event (individual game or generation summary) to a CSV file.
File is opened in append mode per write — safe to crash mid-run without losing data.
"""

import csv
import os
from datetime import datetime

# Where the CSV lives, relative to the project root
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_PATH = os.path.join(LOG_DIR, "training_log.csv")

# Column order — keep in sync with log_game / log_generation
COLUMNS = [
    "timestamp",
    "generation",
    "game_index",      # null for generation_summary rows
    "score",
    "row_type",        # "game" or "generation_summary"
    "model_filename",  # null unless a checkpoint was saved this row
]


class TrainingLogger:
    """Append-only CSV logger for training runs.

    Usage:
        logger = TrainingLogger()
        logger.log_game(generation=0, game_index=2, score=87)
        logger.log_generation(generation=0, mean_score=74.6, best_score=112)
    """

    def __init__(self, path=LOG_PATH):
        self.path = path
        # Make sure the directory exists (first run or clean checkout)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        # Write header only if the file doesn't exist yet
        if not os.path.exists(self.path):
            self._write_row(COLUMNS)

    # -- public API -----------------------------------------------------------

    def log_game(self, generation, game_index, score):
        """Record a single game result."""
        self._write_row([
            _now(),
            generation,
            game_index,
            score,
            "game",
            "",  # no checkpoint for individual games
        ])

    def log_generation(self, generation, mean_score, best_score, model_filename=None):
        """Record a generation summary.

        `score` is the generation's best individual mean (top of the leaderboard).
        `mean_score` is stored as the score column for the summary row so the
        dashboard can plot the population-average trend.
        """
        self._write_row([
            _now(),
            generation,
            "",  # no game_index for summary rows
            mean_score,
            "generation_summary",
            model_filename or "",
        ])

    # -- internals ------------------------------------------------------------

    def _write_row(self, row):
        """Append a single row and close the file immediately."""
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)


def _now():
    """ISO-8601 timestamp, no microseconds (keeps the CSV readable)."""
    return datetime.now().isoformat(timespec="seconds")
