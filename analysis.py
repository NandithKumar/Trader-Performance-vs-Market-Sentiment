# Trader Performance vs Market Sentiment Analysis
# Primetrade.ai — Data Science Intern Assignment

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# =========================
# 1. LOAD DATA
# =========================

# Place both CSV files in the same folder as this script
sentiment = pd.read_csv("fear_greed.csv")
trades = pd.read_csv("hyperliquid_trades.csv")

print("Sentiment shape:", sentiment.shape)
print("Trades shape:", trades.shape)

# =========================
# 2. DATA CLEANING
# =========================

# Convert dates
sentiment['Date'] = pd.to_datetime(sentiment['Date'])

trades['time'] = pd.to_datetime(trades['time'])
trades['Date'] = trades['time'].dt.date
trades['Date'] = pd.to_datetime(trades['Date'])

# Remove duplicates if any
sentiment = sentiment.drop_duplicates()
trades = trades.drop_duplicates()

# =========================
# 3. FEATURE ENGINEERING
# =========================

# Daily PnL per trader
daily_pnl = trades.groupby(['account', 'Date'])['closedPnL'].sum().reset_index()
daily_pnl.rename(columns={'closedPnL': 'daily_pnl'}, inplace=True)

# Number of trades per day
trade_count = trades.groupby(['account', 'Date']).size().reset_index(name='num_trades')

# Average trade size
avg_size = trades.groupby(['account', 'Date'])['size'].mean().reset_index(name='avg_size')

# Win rate
trades['win'] = trades['closedPnL'] > 0
win_rate = trades.groupby(['account', 'Date'])['win'].mean().reset_index(name='win_rate')

# Average leverage
leverage = trades.groupby(['account', 'Date'])['leverage'].mean().reset_index(name='avg_leverage')

# Long/Short ratio
long_short = trades.pivot_table(
    index=['account', 'Date'],
    columns='side',
    values='size',
    aggfunc='count',
    fill_value=0
).reset_index()

long_short['long_short_ratio'] = long_short.get('BUY', 0) / (long_short.get('SELL', 1))

# =========================
# 4. MERGE ALL METRICS
# =========================

metrics = daily_pnl.merge(trade_count, on=['account', 'Date'])
metrics = metrics.merge(avg_size, on=['account', 'Date'])
metrics = metrics.merge(win_rate, on=['account', 'Date'])
metrics = metrics.merge(leverage, on=['account', 'Date'])
metrics = metrics.merge(
    long_short[['account', 'Date', 'long_short_ratio']],
    on=['account', 'Date']
)

# Merge with sentiment
final_df = metrics.merge(sentiment, on='Date', how='left')

print("\nMerged dataset shape:", final_df.shape)

# =========================
# 5. PERFORMANCE ANALYSIS
# =========================

performance = final_df.groupby('Classification')[['daily_pnl', 'win_rate']].mean()
print("\nPerformance by Sentiment:\n", performance)

# =========================
# 6. VISUALIZATIONS
# =========================

plt.figure(figsize=(8,5))
sns.boxplot(data=final_df, x='Classification', y='daily_pnl')
plt.title("PnL Distribution by Market Sentiment")
plt.show()

plt.figure(figsize=(8,5))
sns.barplot(data=final_df, x='Classification', y='num_trades')
plt.title("Trade Frequency by Sentiment")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(data=final_df, x='Classification', y='avg_leverage')
plt.title("Leverage vs Sentiment")
plt.show()

plt.figure(figsize=(8,5))
sns.boxplot(data=final_df, x='Classification', y='long_short_ratio')
plt.title("Long/Short Ratio by Sentiment")
plt.show()

# =========================
# 7. TRADER SEGMENTATION
# =========================

final_df['leverage_group'] = np.where(
    final_df['avg_leverage'] > final_df['avg_leverage'].median(),
    'High',
    'Low'
)

final_df['frequency_group'] = np.where(
    final_df['num_trades'] > final_df['num_trades'].median(),
    'Frequent',
    'Infrequent'
)

final_df['winner_group'] = np.where(
    final_df['daily_pnl'] > 0,
    'Winner',
    'Loser'
)

print("\nSegmentation counts:")
print(final_df[['leverage_group','frequency_group','winner_group']].apply(pd.Series.value_counts))

# =========================
# 8. SAVE OUTPUT (OPTIONAL)
# =========================

final_df.to_csv("processed_trader_data.csv", index=False)

print("\nAnalysis completed successfully.")