import numpy as np

def volatilePos(prcSoFar):

    # Note: prcSoFar is a transposed version of prices250.txt so stocks are the rows
    volatile = prcSoFar[50:,]

    # For volatile testing, position of 0's for first 50 stocks
    pos = np.zeros(100)

    # Count of 
    stock_num = 50

    for stock in volatile:

        # Window size subject to optimisation
        window = 3

        # Get latest day prices
        t = len(stock) - 1

        curr_price = stock[t]
        mean = np.mean(stock[t-window:t-1])
        global_mean = np.mean(stock[:t-1])
        global_diff = curr_price - global_mean
        diff_mean = curr_price - mean 
        last_move = curr_price - stock[t-1]
        recent_trend = stock[t-1] - stock[t-window]
        
        # Thresholds subject to optimisation
        if (last_move - recent_trend > 0.05) and (diff_mean > 0.2):
            # placeholder for amount of stocks to sell, probably determined by global mean
            pos[stock_num] = -10
        elif (last_move - recent_trend < -0.2) and (diff_mean < -0.2):
            # placeholder for amount of stocks to buy, probably determined by global mean
            pos[stock_num] = 10

        #print("Stock: ", stock_num, "\n Spikes: ", spikes, "\n Drops: ", drops)
        stock_num += 1

    return pos

# Test data
data = np.loadtxt('prices250.txt')
prices = data[:201,:].T

# Test model             
pos = volatilePos(prices)
print(pos)

        