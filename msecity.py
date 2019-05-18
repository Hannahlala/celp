from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from check import mse

mse_getal = 0
users_getal = 0

for city in CITIES:
    for user in USERS[city]:
        users_getal += mse(user["user_id"])[1]
        mse_getal += mse(user["user_id"])[0] * mse(user["user_id"])[1]
        print(mse_getal/users_getal)

print(mse_getal/users_getal)