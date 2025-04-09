# 📈 S&P 500 Stock Market Analysis (2014–2017)

This project is a comprehensive analysis of historical stock prices of companies listed in the S&P 500 index, using data from **2014 to 2017**. It leverages Python and popular data science libraries to uncover insights about trading patterns, stock performance, risk, and statistical significance.

---

## 📦 Dataset

- Source: `S&P 500 Stock Prices 2014–2017.csv`
- Columns include:
  - Date
  - Open, High, Low, Close prices
  - Volume
  - Stock symbol

---

## 🎯 Objectives

1. 📌 "Identify major trading events" during the period based on daily percentage change.
2. 📊 "Analyze weekday trading volume trends" to find the most and least active trading days.
3. ⚠️ "Measure stock volatility" and highlight days with the highest price fluctuations.
4. 💹 "Evaluate ROI to determine the best-performing stock over the 4-year period.
5. 📉 "Calculate Value at Risk (VaR)" for selected stocks under normal market conditions.
6. 🧪 "Conduct a t-test" between Apple and Microsoft to check if their returns differ significantly.

---

## 🧰 Tools & Technologies

- Language: Python 3
- Libraries Used:
  - `pandas` – for data manipulation
  - `numpy` – for numerical operations
  - `matplotlib`, `seaborn` – for data visualization
  - `scipy.stats` – for statistical testing

---

## 📌 Key Features

- Automatic date parsing and cleaning
- Group-wise analysis per stock symbol
- Custom visualizations: ROI bar charts, weekday volume plots
- Risk estimation using historical VaR
- Hypothesis testing (t-test) for comparing stock returns

---

## 📊 Sample Outputs

- 📈 Top ROI Stock (2014–2017): XYZ (e.g., +200%)
- 📉 Most Volatile Stock: ABC Corp on `YYYY-MM-DD`
- 🧪 T-test p-value (AAPL vs MSFT): 0.03 → Statistically Significant

---

## 🔍 Instructions to Run

1. Clone the repo or download the files.
2. Ensure you have Python 3.x installed.
3. Install required libraries (if not already installed):

```bash
pip install pandas numpy matplotlib seaborn scipy

```
Run the script:
```
python Project.py

```
🎓 Academic Relevance
This project is part of INT375 – Data Science Toolbox: Python Programming:

Python basics

Data manipulation (NumPy, Pandas)

Visualization (Matplotlib, Seaborn)

Exploratory Data Analysis

Statistical Testing & Distributions

👨‍💻 Author:
Name: Utkarsh Pandey
Course: INT375

📄 License:
This project is for educational use only.
```

