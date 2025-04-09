import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# -------------------------------------------
# 📥 Load the Excel file
# -------------------------------------------
df = pd.read_excel("S&P 500 Stock Prices 2014-2017.xlsx")

# -------------------------------------------
# 🧼 Initial Data Inspection and Cleaning
# -------------------------------------------
df.columns = df.columns.str.strip().str.lower()     # Clean column names
data_info = df.info()                               # Summary info
columns = df.columns.tolist()                       # List of columns
head = df.head()                                    # First 5 rows
tail = df.tail()                                    # Last 5 rows
duplicates = df.duplicated().sum()                  # Count duplicates
description = df.describe()                         # Summary stats
null_values = df.isnull().sum()                     # Count null values

# Drop rows with missing values
df.dropna(inplace=True)

# -------------------------------------------
# 🎯 Objective 1: Identify Major Trading Events
# -------------------------------------------
df['percent_change'] = ((df['close'] - df['open']) / df['open']) * 100
major_events = df.loc[df.groupby('symbol')['percent_change'].apply(lambda x: x.abs().idxmax())]
major_events = major_events.sort_values(by='percent_change', key=abs, ascending=False)

print("🔍 Top 10 Major Trading Events (By % Change):")
print(major_events[['symbol', 'date', 'open', 'close', 'percent_change']].head(10))

# -------------------------------------------
# 🎯 Objective 2: Trading Behavior by Weekday
# -------------------------------------------

df['weekday'] = df['date'].dt.day_name()
weekday_volume = df.groupby('weekday')['volume'].sum()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
weekday_volume = weekday_volume.reindex(weekday_order)

highest_day = weekday_volume.idxmax()
lowest_day = weekday_volume.idxmin()

print("\n📊 Trading Volume by Weekday:")
print(weekday_volume)
print(f"\n📈 Highest average volume day: {highest_day}")
print(f"📉 Lowest average volume day: {lowest_day}")

# 📊 Horizontal bar plot to visualize weekday volume
plt.figure(figsize=(8, 5))
sns.barplot(x=weekday_volume.values, y=weekday_volume.index, palette="crest", orient='h')
plt.title("Total Trading Volume by Weekday (2014–2017)")
plt.xlabel("Total Volume")
plt.ylabel("Weekday")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 🎯 Objective 3: Measuring Stock Volatility
# -------------------------------------------

df['volatility'] = df['high'] - df['low']
max_volatility_per_stock = df.loc[df.groupby('symbol')['volatility'].idxmax()]
top_volatile_days = max_volatility_per_stock.sort_values(by='volatility', ascending=False)

print("\n⚠️ Top 10 Highest Volatility Days (By Stock):")
print(top_volatile_days[['symbol', 'date', 'high', 'low', 'volatility']].head(10))

# 📊 Strip plot to show spread of volatility for top 10 volatile stocks
plt.figure(figsize=(10, 6))
top_symbols = top_volatile_days['symbol'].head(10).tolist()
subset_df = df[df['symbol'].isin(top_symbols)]
sns.stripplot(data=subset_df, x='symbol', y='volatility', jitter=True, palette='coolwarm')
plt.title("Volatility Distribution of Top 10 Volatile Stocks")
plt.xlabel("Stock Symbol")
plt.ylabel("Price Volatility (High - Low)")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 🎯 Objective 4: Evaluate ROI from Jan 2014 to Dec 2017
# -------------------------------------------

start_date = '2014-01-02'
end_date = '2017-12-29'

start_prices = df[df['date'] == pd.to_datetime(start_date)].set_index('symbol')['open']
end_prices = df[df['date'] == pd.to_datetime(end_date)].set_index('symbol')['close']

common_symbols = start_prices.index.intersection(end_prices.index)
start_prices = start_prices.loc[common_symbols]
end_prices = end_prices.loc[common_symbols]

roi = ((end_prices - start_prices) / start_prices) * 100
roi = roi.sort_values(ascending=False)

print("\n💹 Top 10 Stocks by ROI (2014–2017):")
print(roi.head(10))

# 📊 Line chart with markers for ROI
top10 = roi.head(10)
plt.figure(figsize=(10, 6))
plt.plot(top10.index, top10.values, marker='o', linestyle='-', color='green')
plt.title("Top 10 ROI Stocks (2014–2017) - Line Chart")
plt.xlabel("Stock Symbol")
plt.ylabel("ROI (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()


# -------------------------------------------
# 🎯 Objective 5: Calculate Value at Risk (VaR)
# -------------------------------------------

selected_stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN']
var_results = {}

for stock in selected_stocks:
    stock_data = df[df['symbol'] == stock].copy()
    stock_data['daily_return'] = stock_data['close'].pct_change()
    var_95 = np.percentile(stock_data['daily_return'].dropna(), 5)
    var_results[stock] = var_95

print("\n📉 Value at Risk (VaR) at 95% Confidence Level:")
for stock, var in var_results.items():
    print(f"{stock}: {var:.4%} potential loss in a day")

# 📊 Pie chart for proportional VaR
plt.figure(figsize=(6, 6))
plt.pie(
    [-val for val in var_results.values()],
    labels=var_results.keys(),
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette("mako", len(var_results))
)
plt.title("Proportional VaR Contribution (95% Level)")
plt.tight_layout()
plt.show()

# -------------------------------------------
# 🎯 Objective 6: t-test between Apple and Microsoft
# -------------------------------------------

aapl_data = df[df['symbol'] == 'AAPL'].copy()
msft_data = df[df['symbol'] == 'MSFT'].copy()

aapl_data['daily_return'] = aapl_data['close'].pct_change()
msft_data['daily_return'] = msft_data['close'].pct_change()

aapl_returns = aapl_data['daily_return'].dropna()
msft_returns = msft_data['daily_return'].dropna()

t_stat, p_value = ttest_ind(aapl_returns, msft_returns, equal_var=False)

print("\n🧪 T-Test Results (AAPL vs MSFT):")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("✅ Result: There is a statistically significant difference in their daily returns.")
else:
    print("❌ Result: No statistically significant difference in their daily returns.")

# 📊 KDE plot to visualize distribution of returns
plt.figure(figsize=(10, 6))
sns.kdeplot(aapl_returns, label='AAPL', fill=True, color='blue')
sns.kdeplot(msft_returns, label='MSFT', fill=True, color='orange')
plt.title("Daily Return Distribution: AAPL vs MSFT")
plt.xlabel("Daily Return")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.show()
