import pandas as pd
import recommender
import same
import random
import math

import itembased
import numpy as np
from operator import itemgetter
from sklearn.model_selection import train_test_split
from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS
from scipy.spatial import distance

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
    frame_no_ratings = copy_test.drop('stars',axis=1)

    return [frame_no_ratings, user_rating_frame]

def actual_rating(user_id):
    review_frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    return review_frame.loc[user_id]