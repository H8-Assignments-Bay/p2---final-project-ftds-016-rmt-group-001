import pandas as pd
import numpy as np
import re
import joblib
from nltk.tokenize import word_tokenize

def __load_slangwords_stopwords():
    global __slangwords, __stopwords, __vectorizer, __model
    
    with open('./util/model/slangwords_sentiment.txt', 'rt') as file_1:
        __slangwords = {}
        for line in file_1:
            (key, val) = line.rstrip().split(":")
            __slangwords[key] = val

    with open('./util/model/stopwords_sentiment.txt') as file_2:
        __stopwords = [item.rstrip() for item in list(file_2)]
        
    with open('./util/model/vectorizer_sentiment.pkl', 'rb') as file_3:
        __vectorizer = joblib.load(file_3)
        
    with open('./util/model/model_sentiment.pkl', 'rb') as file_4:
        __model = joblib.load(file_4)

__load_slangwords_stopwords()

def __preprocess(comment: str):

  # Menghilangkan nama saham
  comment = re.sub("$[A-Z]{4}| [A-Z]{4} ", " ", comment)

  # Mengubah text ke Lowercase agar semua data seragam
  comment = comment.lower()

  # Menghilangkan @/Mention karena pada berita palsu ada mention akun twitter
  comment = re.sub("@[A-Za-z0-9]+", " ", comment)

  # Menghilangkan #/Hashtag untuk mengantisipasi karena berita palsu mengambil dari twitter
  comment = re.sub("#[A-Za-z0-9_]+", " ", comment)

  # Menghilangkan \n untuk antisipasi
  comment = re.sub(r"\n", " ", comment)

  # Menghilangkan Whitespace untuk antisipasi
  comment = comment.strip()

  # Menghilangkan Link dikarenakan berita palsu terdapat link ke artikel lain
  comment = re.sub(r"http\S+", " ", comment)
  comment = re.sub(r"www.\S+", " ", comment)

  # Menghilangkan yang Bukan Huruf seperti Emoji, Simbol Matematika (seperti μ), dst untuk antisipasi
  comment = re.sub("[^A-Za-z\s']", " ", comment)

  # Melakukan Tokenisasi
  tokens = word_tokenize(comment)

  # Menghilangkan Stopwords
  comment = ' '.join([word for word in tokens if word not in __stopwords])

  # Melakukan lemmatizing
  comment = " ".join(__slangwords.get(word, word) for word in comment.split())

  return comment

def __transform(comments_preprocessed: pd.Series):
    return __vectorizer.transform(comments_preprocessed)

def predict_sentiment(comments: pd.DataFrame):
    comments_preprocessed = comments['comment'].apply(lambda comment: __preprocess(comment))
    comments_vectorized = __transform(comments_preprocessed)
    
    y_pred = __model.predict(comments_vectorized)
    
    return [int(item) for item in y_pred]