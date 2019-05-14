import pandas as pd
from sklearn.model_selection import train_test_split
from data import CITIES, BUSINESSES, USERS, REVIEWS, TIPS, CHECKINS


frame = pd.concat([pd.DataFrame(BUSINESSES[x]) for x in BUSINESSES])

trainset, testset = train_test_split(frame, test_size=0.2)