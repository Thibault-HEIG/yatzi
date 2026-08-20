DICES_TO_ROLL = 5
NB_OF_ROUNDS = 15

class GameState:
    def __init__(self):
        self.current_score = 0
        self.dices = [0, 0, 0, 0, 0]
        self.round = 0
        self.rolls_left = 2
        self.points_to_bonus = 63
        
        self.completed_1s = 0
        self.completed_2s = 0
        self.completed_3s = 0
        self.completed_4s = 0
        self.completed_5s = 0
        self.completed_6s = 0
        self.completed_pair = 0
        self.completed_double_pair = 0
        self.completed_brelan = 0
        self.completed_square = 0
        self.completed_full_house = 0
        self.completed_small_straight = 0
        self.completed_large_straight = 0
        self.completed_luck = 0
        self.completed_yatzi = 0