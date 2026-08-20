"""
Streamlit dashboard for monitoring training progress.

Run with:
    streamlit run tracking/dashboard.py

Reads tracking/logs/training_log.csv and auto-refreshes every few seconds
so you can watch training in real time.
"""

import os
import time

import pandas as pd
import streamlit as st

# -- Config -------------------------------------------------------------------

CSV_PATH = os.path.join(os.path.dirname(__file__), "logs", "training_log.csv")
REFRESH_INTERVAL_SECONDS = 5

# -- Page setup ---------------------------------------------------------------

st.set_page_config(page_title="Yatzy AI Training", layout="wide")
st.title("🎲 Yatzy AI — Training Dashboard")

# -- Auto-refresh -------------------------------------------------------------
# Try streamlit-autorefresh first (cleaner), fall back to manual rerun.

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=REFRESH_INTERVAL_SECONDS * 1000, key="auto_refresh")
except ImportError:
    # No autorefresh package — use a manual sleep + rerun loop.
    # This blocks the script for REFRESH_INTERVAL_SECONDS then reruns.
    placeholder = st.empty()
    placeholder.info(
        f"Auto-refreshing every {REFRESH_INTERVAL_SECONDS}s "
        "(install `streamlit-autorefresh` for a smoother experience)"
    )

# -- Load data ----------------------------------------------------------------

if not os.path.exists(CSV_PATH):
    st.warning("No training log found yet. Start training first (`python main.py`).")
    # Still trigger a rerun so it picks up the file once training starts
    time.sleep(REFRESH_INTERVAL_SECONDS)
    st.rerun()

df = pd.read_csv(CSV_PATH)

# Split into game rows and generation summaries
games = df[df["row_type"] == "game"].copy()
summaries = df[df["row_type"] == "generation_summary"].copy()

# Make sure numeric columns are actually numeric (CSV reads as strings sometimes)
games["score"] = pd.to_numeric(games["score"], errors="coerce")
games["generation"] = pd.to_numeric(games["generation"], errors="coerce")
summaries["score"] = pd.to_numeric(summaries["score"], errors="coerce")
summaries["generation"] = pd.to_numeric(summaries["generation"], errors="coerce")

# -- Stats summary -----------------------------------------------------------

st.subheader("Overview")

if not summaries.empty:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Generations", int(summaries["generation"].max()) + 1)
    col2.metric("Avg (gen means)", f"{summaries['score'].mean():.1f}")
    col3.metric("Best gen avg", f"{summaries['score'].max():.1f}")
    col4.metric("Worst gen avg", f"{summaries['score'].min():.1f}")
else:
    st.info("No generation summaries recorded yet.")

# -- Line chart: generation average over time ---------------------------------

st.subheader("Generation Average Score")

if not summaries.empty:
    chart_data = summaries[["generation", "score"]].set_index("generation").sort_index()
    chart_data.columns = ["avg_score"]
    st.line_chart(chart_data)
else:
    st.info("Waiting for data…")

# -- Recent game scores (optional detail table) -------------------------------

st.subheader("Recent Game Scores")

if not games.empty:
    # Show the last 50 games so the table doesn't get huge
    st.dataframe(
        games[["timestamp", "generation", "game_index", "score"]]
        .tail(50)
        .sort_values("timestamp", ascending=False),
        use_container_width=True,
    )
else:
    st.info("No individual game scores recorded yet.")

# -- Checkpoints table --------------------------------------------------------

st.subheader("Saved Checkpoints")

checkpoints = summaries[summaries["model_filename"].notna() & (summaries["model_filename"] != "")]
if not checkpoints.empty:
    st.dataframe(
        checkpoints[["timestamp", "generation", "score", "model_filename"]],
        use_container_width=True,
    )
else:
    st.info("No checkpoints saved yet (threshold not reached).")

# -- Manual rerun fallback (placed at the end so the page renders first) ------

try:
    from streamlit_autorefresh import st_autorefresh  # noqa: F811
except ImportError:
    time.sleep(REFRESH_INTERVAL_SECONDS)
    st.rerun()
