# analysis on alpha returns and PNL 
from utils import *
import matplotlib.pyplot as plt


# weights_df and alpha_returns_df includes "year" column here, bcos python edits the inputs
def pnl(weights, returns_df):
    
    weights_df = weights.copy() # already shifted in run function
    weights_df = weights_df[weights_df.index.isin(returns_df.index)]
    
    alpha_returns_df = pd.DataFrame(
        (weights_df * returns_df).sum(axis = 1), 
        columns = ['returns']
    )
    
    pnl = (alpha_returns_df['returns'] + 1).cumprod() - 1
    
    return pnl

