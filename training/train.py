import numpy as np

from brain.neural_network import init_model, mutate_weights
from game.game import play_game

GAMES_PER_EVAL = 5
POPULATION_SIZE = 50
KEEP_TOP = 10

def evaluate_brain(model, games=GAMES_PER_EVAL):
    scores = []
    for _ in range(games):
        scores.append(play_game(model))  # your existing game loop, returns final_score
    return np.mean(scores)

def init_population(size):
    return [init_model() for _ in range(size)]

def evolve_generation(population=init_population(POPULATION_SIZE), keep_top=KEEP_TOP):
    scored = [(evaluate_brain(m), m) for m in population]
    scored.sort(key=lambda x: x[0], reverse=True)
    survivors = [m for _, m in scored[:keep_top]]

    next_gen = list(survivors)  # keep the best unmutated (elitism)
    while len(next_gen) < len(population): # fill the remaining population with mutations
        parent = survivors[np.random.randint(len(survivors))]
        next_gen.append(mutate_weights(parent))

    return next_gen, scored  # new population, scores this gen