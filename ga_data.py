import yfinance as yf
import pandas as pd

# Fetch historical stock price data for Microsoft (MSFT)
msft_data = yf.download('MSFT', start='2014-03-10', end='2024-03-10')

# Calculate moving averages
msft_data['MA10'] = msft_data['Close'].rolling(window=10).mean()
msft_data['MA20'] = msft_data['Close'].rolling(window=20).mean()
msft_data['MA50'] = msft_data['Close'].rolling(window=50).mean()

# Calculate percentage moves
msft_data['Percent_Move'] = msft_data['Close'].pct_change() * 100

# Shift the percentage moves to align with the next day's move
msft_data['Next_Day_Move'] = msft_data['Percent_Move'].shift(-1)

# Drop rows with NaN values (first row and last row)
msft_data.dropna(inplace=True)

# Select the columns for input features and target
features = ['Percent_Move(t-5)', 'Percent_Move(t-4)', 'Percent_Move(t-3)', 'Percent_Move(t-2)', 'Percent_Move(t-1)']
target = 'Next_Day_Move'

# Create lagged features for past five days' percentage moves
for i in range(5):
    msft_data[f'Percent_Move(t-{i+1})'] = msft_data['Percent_Move'].shift(i+1)

# Drop rows with NaN values (due to lagging)
msft_data.dropna(inplace=True)

# Select features and target
X = msft_data[features]
y = msft_data[target]

# Print the first few rows of the data
pd.set_option('display.max_columns', None)
#print(msft_data.head(10))
msft_data.to_csv('msft_data2.txt', index=True, sep='\t')
