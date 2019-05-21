import pandas as pd
from sklearn.model_selection import train_test_split
import itembased_test2
from data import REVIEWS

def start(user_id, business_id=None, city=None):
    if not business_id:
        return mse(user_id)
    else:
        return mse(user_id, business_id, city)


def test1(user_id):
    return pd.DataFrame(itembased_test2.itembase(user_id=user_id))

def test2(user_id, business_id, city):
    return pd.DataFrame(incl_city_business(user_id=user_id, business_id=business_id, city=city))


def all_ratings_user(user_id):
    frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    condition = frame["user_id"] == user_id
    correct_user = frame.loc[condition]
    return correct_user


def ratings_together(user_id, business_id=None, city=None):
    """creates dataframe with actual and predicted review"""

    if not business_id:
        allpredicted = test1(user_id)
        realreview = all_ratings_user(user_id)
        allpredicted.append(realreview['stars'])
        return allpredicted
    else:
        allpredicted = test2(user_id, business_id, city)
        realreview = all_ratings_user(user_id)
        allpredicted.append(realreview['stars'])
        return allpredicted



def mse(user_id, business_id=None, city=None):
    """computes the mean square error between actual ratings and predicted ratings"""

    allpredicted = ratings_together(user_id, business_id=None, city=None)
    diff = allpredicted['stars'] - allpredicted['predicted rating']
    length_reviews_user = len(diff)
    return [(diff ** 2).mean(), length_reviews_user]