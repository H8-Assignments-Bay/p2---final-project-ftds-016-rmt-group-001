from typing import Dict
import pandas as pd

cache: Dict[str, pd.DataFrame] = {}

def get_cache(symbol: str):
    return cache.get(symbol)

def set_cache(symbol: str, df: pd.DataFrame):
    cache[symbol] = df