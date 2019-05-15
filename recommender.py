from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random
import itembased
import numpy as np
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
    # ideeën
    # op plek x een random suggestie (weinig rating of buiten range)
    
    print(user_id, business_id, city, n)
    if not user_id:
        if not business_id:
            return logout_without_business(city, n)

        return logout_with_business(business_id, city, n)
    # city = random.choice(CITIES)
    
    if not business_id:
        return login_without_business(user_id, city, n)
    
    return login_with_business(user_id, business_id, city, n)

def logout_without_business(city, n):
    # filter all data (nu elke keer als pagina wordt geopend, moet ooit per sessie)
    filtered_data = []
    if not city:
        for place in CITIES:
            for business in BUSINESSES[place]:
                if business['is_open'] == 1 and business['review_count'] > 9:
                    filtered_data.append(business)
    
    else:
        for business in BUSINESSES[city]:
            if business['is_open'] == 1 and business['review_count'] > 9:
                filtered_data.append(business)

    sorted_data = sorted(filtered_data, key=itemgetter('stars'), reverse=True)[:n]
        
    # let op, als er geen overlap was, geeft hij nu 11 terug ipv 10
    return sorted_data[:n]

def logout_with_business(business_id, city, n):
    if not city:
        city = random.choice(CITIES)
    
    # get categories from specific business
    for business1 in BUSINESSES[city]:
        if business1["business_id"] == business_id:
            business_cat = business1["categories"].split(', ')

    # check if categories match with other businesses
    filtered_data = []
    for business2 in BUSINESSES[city]:
        if any(x in business2["categories"].split(', ') for x in business_cat):
            filtered_data.append(business2)

    sorted_data = sorted(filtered_data, key=itemgetter('stars'), reverse=True)[:n + 1]

    # prevents the specific business from displaying twice
    for x in sorted_data:
        if x['business_id'] == business_id:
            sorted_data.remove(x)

    return  sorted_data[:n]


def login_without_business(user_id, n):
    return itembased.itembase(user_id=user_id, n=n)
    

def login_with_business(user_id, business_id, city, n):
    if not city:
        city = random.choice(CITIES)
    return itembased.incl_city_business(user_id=user_id, business_id=business_id, city=city, n=n)
