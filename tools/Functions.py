# functions for expr
from utils import *

def delta(data, n):
    dir_df = data.diff().apply(np.sign)
    window = dir_df.rolling(n)
    result = window.sum()
    return result
