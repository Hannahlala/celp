import recommender
import pandas as pd
from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random
import numpy as np
from operator import itemgetter

import math
from scipy.spatial import distance

def itembase (user_id, city, n):
    print("lets go!")
    
    frame = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])

    predictions = []

    utility_matrix = pivot_ratings(frame)

    print("je bent ong halverwege...")

    similarity = create_similarity_matrix_euclid(utility_matrix)

    print("we zijn er bijna")

    for business in BUSINESSES[city]:
        neighborhood = select_neighborhood(similarity, utility_matrix, user_id, business["business_id"])
        prediction = weighted_mean(neighborhood, utility_matrix, user_id)
        print("normaal: ", prediction)
        # wanneer hij hier voor de tweede keer komt, krijg ik de vollgende melding: 
        # C:\Users\Gebruiker\Documents\GitHub\celp\itembased.py:111: RuntimeWarning: invalid value encountered in double_scalarsmean = ((utility_matrix[user_id] * neighborhood).sum())/neighborhood.sum()
        # vervolgens lijkt hij wel gewoon door te gaan
        # verwijder alle city's die je nu hebt staan en voeg dan Ambridge toe, dit is nl veel minder data en anders duurt het echt te lang
        # daarbij als je meerdere citys hebt gaat het wss mis
        # dit is omdat hij random een city pakt en dan kan het zijn dat alles nan wordt als de city niet 1 is waar de gebruiker in zit
        # als je hem dan runt en inlogd met Jarrod zie je in de terminal dit probleem
        predictions.append([prediction, business])

    # vervolgens wordt predictions wel een list met daar in lists en in elke van deze lists staat op de eerste plek de voorspelde rating
    # en op de tweede plek een dict met alle info van het bedrijf
    # dus dit is de vorm: [[rating, {business info}], [rating, {business info}], ect.]
    # wanneer ik die vervolgens probeer te sorteren gebeurt er precies niks.
    # in de terminal print hij eerst op volgorde van predictions en daarna op de volgorde van sorted_prediction
    # en dan kun je zien dat ze hetzelfde zijn :)
    sorted_prediction = sorted(predictions, key=lambda x: x[0])

    for x in sorted_prediction:
        print("gesorteerd: ", x[0])

    return random.sample(BUSINESSES[city], n)

def get_rating(ratings, userId, BusinessId):
    """Given a userId and BusinessId, this- function returns the corresponding rating.
      Should return NaN if no rating exists."""
    rating = ratings[(ratings['business_id'] == BusinessId) & (ratings['user_id'] == userId)]
    
    if rating.empty:
        return np.nan
    elif len(rating) > 1:
        return float(rating['stars'].max())
    else:
        return float(rating['stars'])

def pivot_ratings(ratings):
    """ takes a rating table as input and computes the utility matrix """
    # get business and user id's
    businessIds = ratings['business_id'].unique()
    userIds = ratings['user_id'].unique()
    
    # create empty data frame
    pivot_data = pd.DataFrame(np.nan, columns=userIds, index=businessIds, dtype=float)
    
    # use the function get_rating to fill the matrix
    for user in userIds:
        for business in businessIds:
            pivot_data.loc[business][user] = get_rating(ratings, user, business)
    
    return pivot_data

def similarity_euclid(matrix, business1, business2):
    # only take the features that have values for both id1 and id2
    selected_features = matrix.loc[business1].notna() & matrix.loc[business2].notna()
    
    # if no matching features, return NaN
    if not selected_features.any():
        return 0

    # get the features from the matrix
    features1 = matrix.loc[business1][selected_features]
    features2 = matrix.loc[business2][selected_features]

    # compute the distances for the features
    distance = math.sqrt(((features1 - features2) ** 2 ).sum())
    
    # if no distance could be computed (no shared features) return a similarity of 0
    if distance is np.nan:
        return 0
    
    # else return similarity
    return 1 / (1 + distance)

def create_similarity_matrix_euclid(matrix):
    """creates the similarity matrix based on eucledian distance"""
    similarity_matrix_euclid = pd.DataFrame(0, index=matrix.index, columns=matrix.index, dtype=float)
    
    for business1 in matrix.index:
        for business2 in matrix.index:
            similarity_matrix_euclid[business1][business2] = similarity_euclid(matrix, business1, business2)
            
    return similarity_matrix_euclid

def select_neighborhood(similarity_matrix, utility_matrix, target_user, target_business):
    """selects all items with similarity > 0"""
    items_dict ={}
    new_matrix = utility_matrix[target_user].dropna()
    for business in new_matrix.index:
        if new_matrix[business] and similarity_matrix[business][target_business] > 0:
            items_dict[business] = similarity_matrix[business][target_business]
    items = pd.Series(items_dict) 
    return items

def weighted_mean(neighborhood, utility_matrix, user_id):
    mean = ((utility_matrix[user_id] * neighborhood).sum())/neighborhood.sum()
    return mean