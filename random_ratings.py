from data import REVIEWS
import pandas as pd
import numpy as np


def mse(frame):
    """computes the mse when predictions are made randomly"""
    difference = frame['stars'] - frame['random_ratings']
    return (difference ** 2).mean()


frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
frame['random_ratings'] = np.random.randint(1, 5, frame.shape[0])
mse_random = mse(frame)

print("Random mse:", mse_random)
