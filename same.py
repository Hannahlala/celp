import pandas as pd
from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS

framey = pd.concat([pd.DataFrame(REVIEWS[x]) for x in REVIEWS])

def same(dataframe):
    #dataframe[~dataframe[dataframe.user_id].apply(tuple).duplicated()]
    dataframe.drop_duplicates(subset=["user_id","business_id"], keep='last', inplace=False)

same(framey)