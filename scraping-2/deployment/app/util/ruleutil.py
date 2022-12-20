import pandas as pd
import numpy as np

# TODO: Rule-based Filter
def predict_subject(comments: pd.DataFrame):
    return np.random.randint(0,2,comments.shape[0])