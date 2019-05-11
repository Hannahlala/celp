from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

import random

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
    if not city:
        city = random.choice(CITIES)
    
    if not user_id:
        # filter all data (nu elke keer als pagina wordt geopend, moet per sessie)
        filtered_data =[]
        for place in CITIES:
            for business in BUSINESSES[place]:
                if business['is_open'] == 1 and business['review_count'] > 9:
                    filtered_data.append(business)
        
        
        sorted_data = sorted(filtered_data, key=lambda k: k['stars'], reverse=True)[:n+1]
        
        # Check if searched business is not also recommended, remove if yes
        for x in sorted_data:
            if x['business_id'] == business_id:
                sorted_data.remove(x)
    
        # let op, als er geen overlap was, geeft hij nu 11 terug ipv 10
        return sorted_data[:n]
    return random.sample(BUSINESSES[city], n)
