import recommender
import pandas as pd
from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import numpy as np

import math


def incl_city_business(user_id, business_id, city):
    """creates combination of item based and content based recommender system"""
    frame1 = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS if x == city])

    businesses = pd.DataFrame()

    for business1 in BUSINESSES[city]:
        if business1["business_id"] == business_id and business1['categories'] is not None:
            business_cat = business1["categories"].split(', ')

    for business2 in BUSINESSES[city]:
        if business2['business_id'] != business_id:
            if business2['is_open'] == 1 and business2['review_count'] > 9 and business2['categories'] is not None:
                if any(x in business2["categories"].split(', ') for x in business_cat):
                    businesses = businesses.append(business2, ignore_index=True)

    # drop first reviews when user reviewed company more then once
    frame2 = frame1.drop_duplicates(subset=["user_id","business_id"], keep='last', inplace=False)
    utility_matrix = pivot_reviews(frame2)
    similarity = create_similarity_matrix_euclid(utility_matrix)

    for business in businesses.index:
        neighborhood = select_neighborhood(similarity, utility_matrix, user_id, businesses.loc[business]["business_id"])
        prediction = weighted_mean(neighborhood, utility_matrix, user_id)
        businesses.ix[business, 'predicted rating'] = prediction

    sorted_prediction = businesses.sort_values(by=['predicted rating'], ascending=False)
    sorted_prediction2 = sorted_prediction.drop(columns=['predicted rating'])
    sorted_prediction2 = sorted_prediction2.reset_index()
    sorted_prediction3 =sorted_prediction.reset_index()
    return sorted_prediction2.to_dict(orient='records'), sorted_prediction3.to_dict(orient='records')


def itembase(user_id):
    """creates item based recommender system"""
    frame1 = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])
    filtered_data = recommender.filtering_not_city()
    businesses = pd.DataFrame(filtered_data).set_index('business_id')
    frame2 = frame1.drop_duplicates(subset=["user_id","business_id"], keep='last', inplace=False)
    
    utility_matrix = pivot_reviews(frame2)

    similarity = create_similarity_matrix_euclid(utility_matrix)

    for business in businesses.index:
        neighborhood = select_neighborhood(similarity, utility_matrix, user_id, business)
        prediction = weighted_mean(neighborhood, utility_matrix, user_id)
        businesses.ix[business, 'predicted rating'] = prediction

    sorted_prediction = businesses.sort_values(by=['predicted rating'], ascending=False)
    sorted_prediction2 = sorted_prediction.drop(columns=['predicted rating'])
    sorted_prediction2 = sorted_prediction2.reset_index()
    sorted_prediction3 =sorted_prediction.reset_index()
    return sorted_prediction2.to_dict(orient='records'), sorted_prediction3.to_dict(orient='records')

def get_review(reviews, userId, BusinessId):
    """given a userId and BusinessId, this function returns the corresponding review"""
    reviews = reviews[(reviews['business_id'] == BusinessId) & (reviews['user_id'] == userId)]
    
    if reviews.empty:
        return np.nan
    elif len(reviews) > 1:
        return float(reviews['stars'].max())
    else:
        return float(reviews['stars'])

def pivot_reviews(reviews):
    """takes a review table as input and computes the utility matrix"""

    businessIds = reviews['business_id'].unique()
    userIds = reviews['user_id'].unique()

    pivot_data = pd.DataFrame(np.nan, columns=userIds, index=businessIds, dtype=float)

    for user in userIds:
        for business in businessIds:
            pivot_data.loc[business][user] = get_review(reviews, user, business)
    
    return pivot_data

def similarity_euclid(matrix, business1, business2):
    """computes the euclidean similarity"""
    selected_features = matrix.loc[business1].notna() & matrix.loc[business2].notna()

    if not selected_features.any():
        return 0

    features1 = matrix.loc[business1][selected_features]
    features2 = matrix.loc[business2][selected_features]
    distance = math.sqrt(((features1 - features2) ** 2).sum())

    if distance is np.nan:
        return 0

    return 1 / (1 + distance)

def create_similarity_matrix_euclid(matrix):
    """creates the similarity matrix based on euclidean distance"""
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

    return pd.Series(items_dict)

def weighted_mean(neighborhood, utility_matrix, user_id):
    """computes the weighted mean"""
    if neighborhood.sum() != 0:
        return ((utility_matrix[user_id] * neighborhood).sum()) / neighborhood.sum()
    else:
        return 0