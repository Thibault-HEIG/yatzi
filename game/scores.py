CATEGORIES = ['1s', '2s', '3s', '4s', '5s', '6s', 'pair', 'double_pair', 'brelan', 'square', 'full_house', 'small_straight', 'large_straight', 'luck', 'yatzi']

def score(game_state, category, possibilities):
    if category not in CATEGORIES:
        return False
    
    completed_key = f'completed_{category}'
    if getattr(game_state, completed_key) == 1:
        return False
    
    value = possibilities.get(category, -1)
    if value == -1:
        return False
    
    game_state.current_score += value
    setattr(game_state, completed_key, 1)
    print(f"Scored {value} in {category}")
    return True    