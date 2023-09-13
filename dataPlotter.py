# =================== PLT STUFF ===================

import matplotlib.pyplot as plt


def plot(df):
    print("Plotting data...")

    # Create a figure and multiple subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(16, 10), sharex="all")

    # Plot the original 'close' price, EMAs, and RSI in the top subplot
    ax1.plot(df['date'], df['close'], label='Close Price', color='blue')
    ax1.plot(df['date'], df['EMA_5'], label='EMA 5', color='orange')
    ax1.plot(df['date'], df['EMA_50'], label='EMA 50', color='red')
    ax1.plot(df['date'], df['EMA_100'], label='EMA 100', color='green')
    ax1.plot(df['date'], df['EMA_200'], label='EMA 200', color='yellow')
    ax1.set_ylabel('Price')
    ax1.legend()

    # plot ema5 growth
    ax2.plot(df['date'], df['EMA_5_SLOPE'], label="ema 5 slope", color="black")
    ax2.axhline(y=0, color='red', linestyle='--')

    # Plot the MACD and signal line in the middle subplot
    ax3.plot(df['date'], df['macd'], label='MACD', color='red')
    ax3.plot(df['date'], df['macd_signal'], label='Signal Line', color='purple')
    ax3.set_ylabel('MACD')
    ax3.legend()

    # Plot the RSI in a different color
    ax4.plot(df['date'], df['rsi'], label='RSI', color='green')
    # Add horizontal lines at RSI levels of 70 and 30
    ax4.axhline(y=70, color='red', linestyle='--', label='Overbought (70)')
    ax4.axhline(y=30, color='blue', linestyle='--', label='Oversold (30)')
    ax4.legend()


    # Reduce the number of x-axis ticks and labels as shown in previous responses
    num_ticks = 3  # Adjust this number to your preference
    step = len(df) // num_ticks
    xticks = df['date'][::step]

    # Set the x-axis ticks and labels for all subplots
    ax1.set_xticks(xticks)

    # Customize the layout and title
    # ax1.set_xlabel('Date')
    # ax1.set_title(f"{symbol} Stock")

    # Ensure tight layout
    plt.tight_layout()

    # Display the plot
    plt.show()

    print("Done!\n")
