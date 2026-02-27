# Trader Performance vs Market Sentiment

This project analyzes how Bitcoin market sentiment (Fear vs Greed) relates to trader behavior and performance on Hyperliquid.

## Objective

To uncover patterns between market sentiment and trading outcomes that could inform smarter trading strategies.

---

## Dataset

Two datasets are used:

1. **Bitcoin Market Sentiment (Fear/Greed)**
   - Columns: Date, Classification (Fear/Greed)
   - Frequency: Daily

2. **Hyperliquid Historical Trader Data**
   - Trade-level data including account, price, size, side, time, closedPnL, leverage, etc.

Place both CSV files in the project directory before running the analysis:

- `fear_greed.csv`
- `hyperliquid_trades.csv`

---

## Methodology

1. Data Cleaning
   - Converted timestamps to datetime format
   - Removed duplicates
   - Aggregated trade data to daily level per trader

2. Feature Engineering
   Created daily metrics per trader:
   - Daily PnL
   - Win rate
   - Number of trades
   - Average trade size
   - Average leverage
   - Long/Short ratio

3. Data Integration
   - Merged trader metrics with daily market sentiment

4. Analysis
   - Compared performance across Fear vs Greed periods
   - Examined behavioral changes
   - Segmented traders by leverage and activity

---

## Key Outputs

The analysis generates:

- Performance comparison by sentiment
- Behavioral insights (trade frequency, leverage, bias)
- Trader segmentation
- Visualization charts

---

## Setup

Install required libraries:

pip install -r requirements.txt

---

## How to Run

Run the analysis script:

python analysis.py

or open and run all cells if using Jupyter Notebook.

---

## Files in This Repository

- `analysis.py` or `analysis.ipynb` — Main analysis code
- `requirements.txt` — Dependencies
- `report.md` — Summary of findings
- Dataset files (not included)

---

## Conclusion

Market sentiment significantly influences trader behavior and performance.  
Incorporating sentiment-aware risk management strategies can improve trading consistency and reduce downside risk.
