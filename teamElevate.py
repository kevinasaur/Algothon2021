#!/usr/bin/env python

# RENAME THIS FILE WITH YOUR TEAM NAME.

import numpy as np

nInst=100

# Dummy algorithm to demonstrate function format.
def getMyPosition (prcSoFar):
    currentPos_first = shapePos(prcSoFar[:50,])
    currentPos_second = volatilePos(prcSoFar[50:,])
    
    currentPos = np.concatenate((currentPos_first, currentPos_second))
    return currentPos

def shapePos(prcSoFar):
    
    # Window threshold subject to optimisation
    window = 5
    
    for i in range(len(prcSoFar)):
        shape = prcSoFar[i,:]
        shape_reshaped = shape[-window:].reshape(1,window)
    
        # Create empty position vector
        pos = np.zeros(100)

        # Define exponential patterns to look for matches against
        up_flat = -np.exp(-5*np.linspace(0,1,window))
        down_flat = np.exp(-5*np.linspace(0,1,window))
        flat_up = np.exp(5*np.linspace(0,1,window))
        flat_down = -np.exp(5*np.linspace(0,1,window))

        # Stack matrixes for cross-correlation calculations
        shape_data = np.concatenate((shape_reshaped,(up_flat,down_flat,flat_up,flat_down)), axis=0)

        # Calculate correlation
        shape_corr = np.corrcoef(shape_data,rowvar=True)
        
        # Categorise current window
        if shape_corr[-4,0] > shape_corr[-2,0]:
            # Sell if in decreasing upwards trend (proportional to confidence in shape)
            if (shape_corr[-4,0] > 0.75): pos[i] = -100*shape_corr[-4,0]
        else:
            # Buy if in increasing upwards trend (proportional to confidence in shape)
            if (shape_corr[-2,0] > 0.75): pos[i] = 100*shape_corr[-2,0]

        if shape_corr[-3,0] > shape_corr[-1,0]:
            # Buy if in decreasing downwards trend (proportional to confidence in shape)
            if (shape_corr[-3,0] > 0.75): pos[i] = 100*shape_corr[-3,0]
        else:
            # Sell if in increasing downwards trend (proportional to confidence in shape)
            if (shape_corr[-1,0] > 0.75): pos[i] = -100*shape_corr[-1,0]

    return pos

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
    
