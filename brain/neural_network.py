import numpy as np
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

INPUTS = 38
HIDDEN_LAYER_1 = 32
HIDDEN_LAYER_2 = 16
OUPUTS = 20

MUTATION_STD = 0.5      # magnitude of noise added when cloning

def init_model():
    model = models.Sequential([
        layers.Flatten(input_shape=(INPUTS,)), # (*,) converts to a tuple
        layers.Dense(HIDDEN_LAYER_1, activation='relu'),
        layers.Dense(HIDDEN_LAYER_2, activation='relu'),
        layers.Dense(OUPUTS, activation='softmax')])
    return model

def mutate_weights(model, std=MUTATION_STD):
    child = models.clone_model(model)
    child.build(model.input_shape)
    new_weights = []
    for w in model.get_weights():
        noise = np.random.normal(0, std, size=w.shape)
        new_weights.append(w + noise)
    child.set_weights(new_weights)
    return child
    
def think(model, state_dict):
    nn_input = np.array([tuple(state_dict.values())]) # 2D array for tensorflow predict() method
    raw_ouput = np.array(model(nn_input, training=False))
    prediction = raw_ouput[0]
    dices = prediction[:5] >= 0.5
    output = {'rerolls': dices[:5],
        'scores':
        {'1s': prediction[5],
        '2s': prediction[6],
        '3s': prediction[7],
        '4s': prediction[8],
        '5s': prediction[9],
        '6s': prediction[10],
        'pair': prediction[11],
        'double_pair': prediction[12],
        'brelans': prediction[13],
        'squares': prediction[14],
        'full_houses': prediction[15],
        'small_straights': prediction[16],
        'large_straights': prediction[17],
        'luck': prediction[18],
        'yatzis': prediction[19],}
        }
    return output