import pandas as pd
import numpy as np
import re

def get_finds(comment: str):
    finds = re.findall(pattern="(?:\$?[A-Z]{4},?\s?){1,}(?:(?:dan)?(?:hingga)?\s?[A-Z]{4})?", string=comment)

    finds = [re.sub("[\$\n,]|dan|hingga", "", item).split() for item in finds]
    
    return finds
  
def is_subject_equal_to_symbol(finds: list[list[str]], symbol: str):
  
  for index, items in enumerate(finds):
    # check 1st finds
    if index == 0:

      # no subject
      # e.g "sahamnya bagus"
      if len(items) == 0: return 1
      
      # 1st finds length is 1
      # e.g "GOTO bagus"
      if len(items) == 1:

        # e.g "IHSG naik 0.3% Rekomendasi Saham GOTO, ICBP"
        if items[0] == "IHSG": continue
        elif items[0] == symbol: return 1
        else: return 0
    
    # check 1st and 2nd finds
    # 2nd finds length is 1
    # e.g "IHSG naik 0.3% GOTO bagus"
    if len(items) == 1:
      if finds[0] == symbol: return 1

    else:
      # finds length are more than 1.
      # e.g "GOTO, ICBP bagus"
      # e.g "IHSG naik 0.3% GOTO, ICBP bagus"
      for item in items:
        if item == symbol: return 1

  # unknown pattern.
  # verdict: Reject
  return 0

def predict_subject(comments: pd.DataFrame, symbol: str):
    
    finds = comments['comment'].apply(lambda comment: get_finds(comment))
    subject = finds.apply(lambda row: is_subject_equal_to_symbol(row, symbol))
    
    return subject.tolist()