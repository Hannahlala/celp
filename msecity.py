from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from check import mse
import numpy as np

mse_getal = 0
users_getal = 1

for city in CITIES:
    for user in USERS[city]:
        a, b = mse(user["user_id"])
        users_getal += b
        if not np.isnan(a):
                mse_getal += a * b
                print(user["user_id"], mse_getal/users_getal)

print(mse_getal/(users_getal-1))