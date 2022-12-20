import pandas as pd
import numpy as np

# TODO: Neutral/Negative/Positive Model
def predict_sentiment(comments: pd.DataFrame):
    return np.random.randint(0,3,comments.shape[0])