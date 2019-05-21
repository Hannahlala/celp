from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
import pandas as pd
import numpy as np
import random

def mse(frame):
    difference = frame['stars'] - frame['random_ratings']
    return (difference**2).mean()

frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])

# creates list of random ratings
frame['random_ratings'] = np.random.randint(1, 5, frame.shape[0])

# calculates the mse
mse_random = mse(frame)
print("Random mse:", mse_random)