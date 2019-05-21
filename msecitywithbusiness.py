from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from check import mse
import pandas as pd
import itembased_test2
import itembased
import random

mse_getal = 0
users_getal = 0

for city in CITIES:
    for user in USERS[city]:
            yes = pd.DataFrame(itembased.itembase(user['user_id']))[:10]
            listi = list(yes['business_id'])
            random_business = random.choice(listi)

            users_getal += mse(user["user_id"], random_business, city)[1]
            mse_getal += mse(user["user_id"], random_business, city)[0] * mse(user["user_id"], random_business, city)[1]
            print(mse_getal/users_getal)

print(mse_getal/users_getal)