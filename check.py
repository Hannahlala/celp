from data import REVIEWS
import itembased
import pandas as pd




def start(user_id, business_id=None, city=None):
    "Initiates the functions and calculates mse"
    if not business_id:
        return mse(user_id)
    else:
        return mse(user_id, business_id, city)


def test1(user_id):
    "Refers to itembased predictions"
    x, y = itembased.itembase(user_id=user_id)
    return pd.DataFrame(y)


def test2(user_id, business_id, city):
    "Refers to item and content based predictions"
    x, y = itembased.incl_city_business(user_id=user_id, business_id=business_id, city=city)
    return pd.DataFrame(y)


def all_ratings_user(user_id):
    " Shows all the rows when users reviews business(es)"
    frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    condition = frame["user_id"] == user_id
    correct_user = frame.loc[condition]
    return correct_user


def ratings_together(user_id, business_id=None, city=None):
    """creates dataframe with actual and predicted review"""
    if not business_id:
        allpredicted = test1(user_id)
        realreview = all_ratings_user(user_id)
        return pd.merge(allpredicted, realreview, on='business_id')
    else:
        allpredicted = test2(user_id, business_id, city)
        realreview = all_ratings_user(user_id)
        return pd.merge(allpredicted, realreview, on='business_id')


def mse(user_id, business_id=None, city=None):
    """computes the mean square error between actual ratings and predicted ratings"""
    if not business_id:
        allpredicted = ratings_together(user_id)
        diff = allpredicted['stars_y'] - allpredicted['predicted rating']
        length_reviews_user = len(diff)
        return [(diff ** 2).mean(), length_reviews_user]
    else:
        allpredicted = ratings_together(user_id, business_id, city)
        diff = allpredicted['stars_y'] - allpredicted['predicted rating']
        length_reviews_user = len(diff)
        return [(diff ** 2).mean(), length_reviews_user]
