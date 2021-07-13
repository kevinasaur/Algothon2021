#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np

nInst=100

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    currentPos_first = np.zeros(50)
    currentPos_second = volatilePos(prcSoFar[50:,])
    
    currentPos = np.concatenate((currentPos_first, currentPos_second))
    return currentPos

def volatilePos(second_half):
      
    window = 10

    # For volatile testing, position of 0s for first 50 stocks
    pos = np.zeros(50)
    
    for stock_num, stock in enumerate(second_half):

        # Get latest day prices
        t = len(stock) - 1
        if t > 0:

            curr_price = stock[t]
            mean = np.mean(stock[np.max([0, t-window]):t-1])
            global_mean = np.mean(stock[:t-1])
            global_diff = curr_price - global_mean
            diff_mean = curr_price - mean 
            last_move = curr_price - stock[t-1]
            recent_trend = stock[t-1] - stock[np.max([0, t-window])]

            # Thresholds determined through parameter search
            if (last_move - recent_trend > 0.1) and (diff_mean > 3):
                pos[stock_num] = np.ceil((-10000*diff_mean)/curr_price)

            elif (last_move - recent_trend < -0.1) and (diff_mean < -3):
                pos[stock_num] = np.floor((-10000*diff_mean)/curr_price)

            stock_num += 1        
    return pos
    
