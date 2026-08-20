import numpy as np

from brain.neural_network import init_model, mutate_weights
from game.game import play_game
from tracking.ledger import TrainingLogger
from tracking.checkpoints import maybe_save_checkpoint

GAMES_PER_EVAL = 5
POPULATION_SIZE = 50
KEEP_TOP = 10

def evaluate_brain(model, generation, logger, games=GAMES_PER_EVAL):
    scores = []
    for game_i in range(games):
        game_score = play_game(model)
        scores.append(game_score)
        logger.log_game(generation, game_i, game_score)
    return np.mean(scores)

def init_population(size):
    return [init_model() for _ in range(size)]

def evolve_generation(generation, population=init_population(POPULATION_SIZE), keep_top=KEEP_TOP, logger=None):
    if logger is None:
        logger = TrainingLogger()
    scored = [(evaluate_brain(m, generation, logger), m) for m in population]
    scored.sort(key=lambda x: x[0], reverse=True)

    # Checkpoint the best model if it meets the threshold
    best_score = scored[0][0]
    checkpoint_file = maybe_save_checkpoint(scored[0][1], generation, best_score)

    # Log a summary row for this generation (population-wide mean)
    pop_mean = np.mean([s for s, _ in scored])
    logger.log_generation(generation, pop_mean, best_score, checkpoint_file)

    survivors = [m for _, m in scored[:keep_top]]

    next_gen = list(survivors)  # keep the best unmutated (elitism)
    while len(next_gen) < len(population): # fill the remaining population with mutations
        parent = survivors[np.random.randint(len(survivors))]
        next_gen.append(mutate_weights(parent))

    return next_gen, scored  # new population, scores this gen