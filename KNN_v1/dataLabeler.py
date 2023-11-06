"""
This will (should) label each kline automatically

1) connect to a chart or get data from a dict
    1.1) Data needed is at least close prices and timestamps of klines
2) check at which point it was optimal to buy/sell/hold
    2.1) since this will be algorithmic, I need a concrete way of telling if a trade is good or bad. I will measure it in profit %.
    2.2) Parameters required to define a "good" slope:
        xMin: min num of Klines
        xMax: max num of klines
        yMin: min difference in price
        chop: max tolerated "choppiness" (~~> standard deviation)
            standardDeviation = sqrt(((data[0] - avg(data))² + (data[1] - avg(data))² + ... + (data[len(data) - 1] - avg(data))²) / len(data)
            standardDeviation = dataFrame.std()
    2.3)
        - fill the necessary buffer
        - from kline a, check points in the range [a + xMin, a + xMax]
        - for each kline check, check also y
        - if y > yMin, then check also the std from a to the current kline
        - if std([a, cKline]) < chop, then store a as a good slope point
        - continue to do this until end dof check klines, then procede to the next kline, b
3) label that point
    Since I don't know the timestamps, I'll have to derive them myself.
    Since I know the start kline, current kline and kline time, i can calculate the current kline's timestamp
    Data example:
        timestamp of start of slope: [x, y, std, label]

        GC15min = {
            1672531200: {
                "label": "s",
                "duration": 7,
                "priceChange": -3.6,
                "std": 1.2,
                "coords": [adx0, adx1, ..., rsi4]
            },
            1672531300: {
                "label": "h",
                "duration": None,
                "priceChange": None,
                "std": None,
                "coords": [adx0, adx1, ..., rsi4]
            },
        }
"""

if __name__ == '__main__':
    pass
