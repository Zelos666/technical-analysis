import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file containing the stock symbols
file_path = '/Users/javvad/stocks/EQUITY_L.csv'
stock_data = pd.read_csv(file_path)

# Extract the stock symbols from the CSV file, remove extra quotes, and trim whitespace
stock_symbols = stock_data['SYMBOL'].str.replace('"', '').str.strip().tolist()


# Test with a known valid symbol
test_symbol = "RELIANCE.NS"
df = yf.download(test_symbol, start="2023-08-01", end="2023-08-03")


# Define the time period for the previous two days
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Initialize a list to store the shortlisted stocks
shortlisted_stocks = []

# Loop through each stock symbol
for symbol in stock_symbols:
    try:
        # Test without adding ".NS" if needed
        df = yf.download(symbol + ".NS", start=start_date, end=end_date)
        print(f"Data for {symbol}:")
        

        if len(df) < 2:
            print(f"Not enough data for {symbol}. Skipping...")
            continue  # Skip the stock if there's not enough data

        # Check if the stock closed in green on the previous day
        previous_day = df.iloc[-2]
        current_day = df.iloc[-1]

        if previous_day['Close'] > previous_day['Open']:
            # Check if today's open is equal to today's high
            if current_day['Open'] == current_day['High']:
                shortlisted_stocks.append(symbol)

    except Exception as e:
        print(f"Failed to download data for {symbol}. Error: {e}")

# Display the shortlisted stocks
if shortlisted_stocks:
    print("Shortlisted Stocks:")
    for stock in shortlisted_stocks:
        print(stock)
else:
    print("No stocks found with the given criteria.")
