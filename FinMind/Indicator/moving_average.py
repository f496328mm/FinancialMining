
import pandas as pd
import numpy as np
import math

def simple_moving_average(pd_src, period):
    """
    Args:
        pd_src (pandas.Series) : 
        period (int) : 
    """
    return pd_src.rolling(period).mean()

def exponential_moving_average(pd_src, period):
    """
    Args:
        pd_src (pandas.Series) : 
        period (int) : 
    """
    ema_list    = []
    init_index  = pd_src.first_valid_index()
    ema         = pd_src.at[init_index]
    k           = 2/(period+1)

    for index, row in pd_src.iteritems():
        if index >= init_index:
            ema = k * row + (1-k) * ema
        if index >= period-1:
            ema_list.append(ema)
        else:
            ema_list.append(np.NaN)
            
    return pd.DataFrame(ema_list)

# Nickname
ma  = simple_moving_average
sma = simple_moving_average
ema = exponential_moving_average
