import pandas as pd
from sklearn.model_selection import train_test_split
import itembased_test2
from data import REVIEWS

def start(user_id):
    predicted = test1(user_id)
    all_rating = all_ratings_user(user_id)
    mse_for_realzies = mse(user_id)
    return mse_for_realzies


def test1(user_id):
    framed = pd.DataFrame(itembased_test2.itembase(user_id=user_id))
    return framed


def all_ratings_user(user_id):
    frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    condition = frame["user_id"] == user_id
    correct_user = frame.loc[condition]
    return correct_user


def ratings_together(user_id):
    """creates dataframe with actual and predicted review"""

    allpredicted = test1(user_id)
    realreview = all_ratings_user(user_id)
    allpredicted.append(realreview['stars'])
    return allpredicted


def mse(user_id):
    """computes the mean square error between actual ratings and predicted ratings"""

    allpredicted = ratings_together(user_id)
    diff = allpredicted['stars'] - allpredicted['predicted rating']
    length_reviews_user = len(diff)
    return [(diff ** 2).mean(), length_reviews_user]