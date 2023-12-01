"""
BASIC GOAL
    The goal of this program is to say what action should have been taken given the price action and specific time
    So basically I want the program to say "long" when the price is about to go up
    and I want it to say "short" when the price is about to go down

    Since this program should be quite picky, I hope I won't have to rely on another program that refines the choices of this one.

DETECT A SLOPE:
    THINKING
    to detect a nice slope and thus the beginning of it, I need some key parameters:
        1) xMin: the min time that has to pass from the beginning of the slope to the end of it
        2) xMax: the max time that can pass from the beginning of the slope to the end of it
        3) yMin: the min change in price that has to happen for a slope to be considered
        4) mMax: the max inclination that the slope can have (we don't want to consider those instant cliffs)
        5) chopMax: the max amount of chope that we allow a slope to have
            But how do I detect chop?
                1) average distance from line
                2) area between price and line

    THE MATH MUST GET MATHING
        x: time
        y: price
        A: open position
        N1, N2, ..., NK: all the values between A and B
        B: close position

        1) Bx - Ax >= xMin
        2) Bx - Ax <= xMax
        3) By - Ay >= yMin
        4) (By - Ay) / (Bx - Ax) <= mMax
        5.1) sum(dist(line, N1), dist(line, N2), ..., dist(line, NK)) / K
        5.2) ??? idk I don't want to implement that

OPTIMISATION
    I could check for each kline all the following xMax - xMin klines, but this would be slow
    Instead, I think it would be quicker to first eliminate all the values that do not meet certain conditions
    and then refine the search. E.g.: first eliminate the values that can't reach yMin within xMax, then calculate the chop
"""

import json
import pandas as pd


# let's load the data that we stole
with open("GC15min-01-01-23 00:00:00.json", "r") as jsonFile:
    data = json.load(jsonFile)

# convert the data into a pandas df
df = pd.DataFrame.from_dict(data, orient='index')
df.columns = ['close', 'coords']
df.insert(0, "timestamp", df.index)
df.reset_index(drop=True, inplace=True)


# TODO
"""
next thing to do is to find a nice and fast way to detect slopes using the said
"""
# TODO
