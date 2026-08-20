"""
Model checkpointing — save the best network when it clears a score threshold.

Checkpoint filenames encode the generation number and timestamp so they can be
traced back to the corresponding CSV row in the training ledger.
"""

import os
from datetime import datetime

# Directory where .keras checkpoints are saved
CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "checkpoints")

# Only save a checkpoint when the generation's best mean score >= this value.
# Tune this based on your game — a random agent typically scores ~50-80,
# so 100 is a reasonable "the network is learning something" bar.
SAVE_THRESHOLD = 75


def maybe_save_checkpoint(model, generation, mean_score):
    """Save the model if mean_score meets the threshold.

    Returns the filename (relative to tracking/) if saved, or None.
    """
    if mean_score < SAVE_THRESHOLD:
        return None

    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gen_{generation}_{timestamp}.keras"
    filepath = os.path.join(CHECKPOINT_DIR, filename)
    model.save(filepath)
    print(f"[checkpoint] saved {filename}  (score={mean_score:.1f})")
    return filename
