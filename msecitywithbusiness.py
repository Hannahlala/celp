from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from check import mse
import pandas as pd
import itembased
import random
import numpy as np

"""computes the content + item based mse of the complete city"""

mse_getal = 0
users_getal = 1

for city in CITIES:
    for user in USERS[city]:
        x, y = itembased.itembase(user['user_id'])
        yes = pd.DataFrame(y)[:10]
        
        random_business = random.sample(list(yes['business_id']), 1)[0]
        a, b = mse(user["user_id"], random_business, city)
        users_getal += b
        if not np.isnan(a):
            mse_getal += a * b
            print(user["user_id"], mse_getal/users_getal)
            

print(mse_getal/(users_getal-1))