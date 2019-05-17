import pandas as pd
from sklearn.model_selection import train_test_split

import itembased_test2
from data import REVIEWS


# splits data in training and test
def splitter(frame):
    trainset, testset = train_test_split(frame, test_size=0.2)

    # returns list test and traingsset
    return [testset, trainset]


# demounts ratings and testframe
def shower():
    frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    # picks the testset
    testset = splitter(frame)[0]
    copy_test = testset

    # gives the right dataframes
    user_rating_frame = pd.DataFrame([testset['user_id'], testset['business_id'], testset['stars']]).T
    frame_no_ratings = copy_test.drop('stars', axis=1)

    return [frame_no_ratings, user_rating_frame]


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
    allpredicted = test1(user_id)
    realreview = all_ratings_user(user_id)
    allpredicted.append(realreview['stars'])

    return allpredicted


def mse(user_id):
    # add rows to test data
    together_frame = ratings_together(user_id)
    together_frame['difference'] = together_frame['stars'] - together_frame['predicted rating']
    together_frame["squared difference"] = together_frame['difference'] ** 2

    # cumpute mean square error
    sum_of_squared = together_frame["squared difference"].sum()
    length_reviews_user = len(together_frame['difference'])
    mse = sum_of_squared / length_reviews_user

    return [mse, length_reviews_user]