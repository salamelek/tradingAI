import pandas as pd
import os


folder_path = './2023-data'  # Change this to your folder path
all_files = os.listdir(folder_path)
csv_files = [f for f in all_files if f.endswith('.csv')]

# Sort the list of CSV files
csv_files = sorted(csv_files)

# Create a list to hold the dataframes
df_list = []

for csv in csv_files:
    if csv.startswith("MERGED"):
        continue

    file_path = os.path.join(folder_path, csv)
    try:
        # Try reading the file using default UTF-8 encoding
        df = pd.read_csv(file_path, usecols=[1, 2, 3, 4], header=None, names=["open", "high", "low", "close"])

        if df["open"][0] == "open":
            df = df.drop(df.index[0])
            df = df.reset_index(drop=True)

        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)

        df_list.append(df)
    except Exception as e:
        print(f"Could not read file {csv} because of error: {e}")

# Concatenate all data into one DataFrame
big_df = pd.concat(df_list, ignore_index=True)

# Save the final result to a new CSV file
big_df.to_csv(os.path.join(folder_path, 'MERGED-ETHUSDT-15m-23.csv'), index=False)
