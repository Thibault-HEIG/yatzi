import random
from game.checks import possibilities
from game.scores import score
from game.state import GameState, DICES_TO_ROLL, NB_OF_ROUNDS
from brain.neural_network import think

def roll_dices(game_state, dices_to_roll = None):
    if dices_to_roll is None:
        dices_to_roll = [True] * DICES_TO_ROLL
    dices = game_state.dices
    for i in range(len(dices)):
        if dices_to_roll[i]:
            dices[i] = random.randint(1, 6)
    return dices

def print_dices(dices):
    print("Dices: ", end="")
    for dice in dices:
        print(dice, end=" ")
    print()
    
def max_scaling(value, max_value):
    return value / max_value

def inverted_max_scaling(value, max_value):
    return 1 - (value / max_value)
    
def create_input(game_state, possibilities_dict, dices):
    # Possibilities features
    scaled_1s = max_scaling(possibilities_dict.get('1s'), 1 * DICES_TO_ROLL)
    scaled_2s = max_scaling(possibilities_dict.get('2s'), 2 * DICES_TO_ROLL)
    scaled_3s = max_scaling(possibilities_dict.get('3s'), 3 * DICES_TO_ROLL)
    scaled_4s = max_scaling(possibilities_dict.get('4s'), 4 * DICES_TO_ROLL)
    scaled_5s = max_scaling(possibilities_dict.get('5s'), 5 * DICES_TO_ROLL)
    scaled_6s = max_scaling(possibilities_dict.get('6s'), 6 * DICES_TO_ROLL)
    scaled_pair = max_scaling(possibilities_dict.get('pair'), 2 * 6)
    scaled_double_pair = max_scaling(possibilities_dict.get('double_pair'), 2 * 6 + 2 * 6)
    scaled_brelans = max_scaling(possibilities_dict.get('brelan'), 3 * 6)
    scaled_squares = max_scaling(possibilities_dict.get('square'), 4 * 6)
    scaled_full_houses = max_scaling(possibilities_dict.get('full_house'), 3 * 6 + 2 * 6)
    scaled_small_straights = max_scaling(possibilities_dict.get('small_straight'), 15)
    scaled_large_straights = max_scaling(possibilities_dict.get('large_straight'), 20)
    scaled_luck = max_scaling(possibilities_dict.get('luck'), 6 * DICES_TO_ROLL) # The dices sum
    scaled_yatzis = max_scaling(possibilities_dict.get('yatzi'), 50)
    
    # Game state features
    scaled_rolls_left = max_scaling(game_state.rolls_left, 2)
    scaled_round = max_scaling(game_state.round, 14) # round 0 to 14
    scaled_points_to_bonus = inverted_max_scaling(game_state.points_to_bonus, 63)
    completed_1s = game_state.completed_1s
    completed_2s = game_state.completed_2s
    completed_3s = game_state.completed_3s
    completed_4s = game_state.completed_4s
    completed_5s = game_state.completed_5s
    completed_6s = game_state.completed_6s
    completed_pair = game_state.completed_pair
    completed_double_pair = game_state.completed_double_pair
    completed_brelan = game_state.completed_brelan
    completed_square = game_state.completed_square
    completed_full_house = game_state.completed_full_house
    completed_small_straight = game_state.completed_small_straight
    completed_large_straight = game_state.completed_large_straight
    completed_luck = game_state.completed_luck
    completed_yatzi = game_state.completed_yatzi
    
    # Dices results features
    scaled_dice_0 = max_scaling(dices[0], 6)
    scaled_dice_1 = max_scaling(dices[1], 6)
    scaled_dice_2 = max_scaling(dices[2], 6)
    scaled_dice_3 = max_scaling(dices[3], 6)
    scaled_dice_4 = max_scaling(dices[4], 6)
    
    return {
        '1s': scaled_1s,
        '2s': scaled_2s,
        '3s': scaled_3s,
        '4s': scaled_4s,
        '5s': scaled_5s,
        '6s': scaled_6s,
        'pair': scaled_pair,
        'double_pair': scaled_double_pair,
        'brelans': scaled_brelans,
        'squares': scaled_squares,
        'full_houses': scaled_full_houses,
        'small_straights': scaled_small_straights,
        'large_straights': scaled_large_straights,
        'luck': scaled_luck,
        'yatzis': scaled_yatzis,
        'rolls_left': scaled_rolls_left,
        'round': scaled_round,
        'points_to_bonus': scaled_points_to_bonus,
        'completed_1s': completed_1s,
        'completed_2s': completed_2s,
        'completed_3s': completed_3s,
        'completed_4s': completed_4s,
        'completed_5s': completed_5s,
        'completed_6s': completed_6s,
        'completed_pair': completed_pair,
        'completed_double_pair': completed_double_pair,
        'completed_brelan': completed_brelan,
        'completed_square': completed_square,
        'completed_full_house': completed_full_house,
        'completed_small_straight': completed_small_straight,
        'completed_large_straight': completed_large_straight,
        'completed_luck': completed_luck,
        'completed_yatzi': completed_yatzi,
        'dice_0': scaled_dice_0,
        'dice_1': scaled_dice_1,
        'dice_2': scaled_dice_2,
        'dice_3': scaled_dice_3,
        'dice_4': scaled_dice_4
    }
    
def play_game(model):
    game_state = GameState()
    
    while game_state.round < NB_OF_ROUNDS:
        print(f"Round {game_state.round}")
        game_state.round += 1
        game_state.rolls_left = 2
        print(f"Current score : {game_state.current_score}")
    
        # Rolling dices
        game_state.dices = roll_dices(game_state)
        dices = game_state.dices
        want_to_reroll = True

        while game_state.rolls_left > 0 and want_to_reroll == True:
            # For the network
            possibilities_dict = possibilities(dices)
            nn_input = create_input(game_state, possibilities_dict, dices)
            nn_output = think(model, nn_input)
            dices_to_reroll = nn_output['rerolls'] # [0,1,0,0,1] → [False, True, False, False, True]
            if dices_to_reroll.any():
                dices = roll_dices(game_state, dices_to_reroll)
                game_state.rolls_left -= 1
            else:
                want_to_reroll = False
        
        # Choosing where to score
        possibilities_dict = possibilities(dices) # Refresh the last available
        
        dict_scores = nn_output['scores']
        sorted_scores = dict(sorted(dict_scores.items(), key=lambda x: x[1], reverse=True))
        
        # Dict des proba de chaque catégorie trié
        for category in sorted_scores:
                try:
                    if score(game_state, category, possibilities_dict):
                        break
                except:
                    print(category + " is not a category.")
    
    return game_state.current_score