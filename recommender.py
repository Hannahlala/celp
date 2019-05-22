from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import pandas as pd
import itembased
import random
import check
from operator import itemgetter


def recommend(user_id=None, business_id=None, city=None, n=10):
    """
    Returns n recommendations as a list of dicts.
    Optionally takes in a user_id, business_id and/or city.
    A recommendation is a dictionary in the form of:
        {
            business_id:str
            stars:str
            name:str
            city:str
            adress:str
        }
    """

    # user_id isn't given
    if not user_id:
        # business_id isn't given
        if not business_id:
            return logout_without_business(city, n)
        # business_id is given
        else:
            return logout_with_business(business_id, city, n)

    # user_id is given
    # runs tests
    else:
        # business_id isn't given
        if not business_id:
            return login_without_business(user_id, n)
        # business_id is given
        else:
            return login_with_business(user_id, business_id, city, n)
        
        return login_with_business(user_id, business_id, city, n)

def logout_without_business(city, n):
    """filter all data and sort by highest stars"""
    if not city:
        filtered_data = filtering_not_city()    
    
    else:
        filtered_data = filtering_city()

    sorted_data = sorted(filtered_data, key=itemgetter('stars'), reverse=True)

    return sorted_data[:n]

def logout_with_business(business_id, city, n):
    """filter all data on categories and sort by highest stars"""

    # get categories from specific business
    for business1 in BUSINESSES[city]:
        if business1["business_id"] == business_id:
            if business1['categories'] != None:
                business_cat = business1["categories"].split(', ')

    # check if categories match with other businesses
    filtered_data = []
    for business2 in BUSINESSES[city]:
        if business2['business_id'] != business_id:
            if business2['categories'] != None:
                if any(x in business2["categories"].split(', ') for x in business_cat):
                    filtered_data.append(business2)

    sorted_data = sorted(filtered_data, key=itemgetter('stars'), reverse=True)

    return sorted_data[:n]


def login_without_business(user_id, n):
    x, y = itembased.itembase(user_id=user_id)
    return x[:n]
    

def login_with_business(user_id, business_id, city, n):
    x, y = itembased.incl_city_business(user_id=user_id, business_id=business_id, city=city)
    return x[:n]

def filtering_not_city():
    " Filtering data if there's no city"
    filtered_data = []

    for place in CITIES:
            for business in BUSINESSES[place]:
                if business['is_open'] == 1 and business['review_count'] > 9:
                    filtered_data.append(business)
    return filtered_data

def filtering_city():
    " Filtering data if there's a city"
    filtered_data = []

    for business in BUSINESSES[place]:
        if business['is_open'] == 1 and business['review_count'] > 9:
            filtered_data.append(business)
    return filtered_data
    