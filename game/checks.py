def dices_to_values(dices):
    values = [0] * 7
    values[0] = 0
    for i in range(1, 7):
        values[i] = dices.count(i)
    return values

# Check combinations
def _pair(values):
    for i in range(6, 0, -1):
        if values[i] >= 2:
            return i * 2
    return 0

def _double_pair(values):
    for i in range(6, 0, -1):
        if values[i] >= 2:
            for j in range(i, 0, -1):
                if values[j] >= 2:
                    return (i * 2) + (j * 2)
    return 0

def _brelan(values):
    for i in range(6, 0, -1):
        if values[i] >= 3:
            return i * 3
    return 0

def _square(values):
    for i in range(6, 0, -1):
        if values[i] >= 4:
            return i * 4
    return 0

def _full_house(values):
    for i in range(6, 0, -1):
        if values[i] >= 3:
            for j in range(6, 0, -1):
                if values[j] >= 2 and j != i:
                    return (i * 3) + (j * 2)
    return 0

def _small_straight(values):
    for start in (1, 2, 3):  # windows [1-4], [2-5], [3-6]
        if all(values[start + k] >= 1 for k in range(4)):
            return 15
    return 0

def _large_straight(values):
    # Check [1,2,3,4,5] or [2,3,4,5,6]
    if all(values[i] >= 1 for i in range(1, 6)) or all(values[i] >= 1 for i in range(2, 7)):
        return 20
    return 0
        
def _yatzi(values):
    for i in range(6, 0, -1):
        if values[i] == 5:
            return 50
    return 0
    
def possibilities(dices):
    values = dices_to_values(dices)
    # Differed for optimal perfomance
    pair = _pair(values)
    double_pair = 0
    brelan = 0
    square = 0
    full_house = 0
    small_straight = _small_straight(values)
    large_straight = 0
    yatzi = 0
    
    if small_straight > 0:
        large_straight = _large_straight(values)
        
    if pair > 0:
        double_pair = _double_pair(values)
        brelan = _brelan(values)
        
        if brelan > 0:
            square = _square(values)
            full_house = _full_house(values)
            
            if square > 0:
                yatzi = _yatzi(values)
        
    return {
        "1s": values[1] * 1,
        "2s": values[2] * 2,
        "3s": values[3] * 3,
        "4s": values[4] * 4,
        "5s": values[5] * 5,
        "6s": values[6] * 6,
        "pair": pair,
        "double_pair": double_pair,
        "brelan": brelan,
        "square": square,
        "full_house": full_house,
        "small_straight": small_straight,
        "large_straight": large_straight,
        "luck": sum(dices),
        "yatzi": yatzi
    }