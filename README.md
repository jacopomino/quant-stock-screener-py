# 📈 Quantitative Stock & ETF Screener

A high-performance Python tool designed to automate technical analysis for financial assets. It processes lists of tickers asynchronously using **Yahoo Finance** data and filters for specific "Buy" signals based on a custom statistical strategy.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Table of Contents

* [Features](#-features)
* [Project Structure](#-project-structure)
* [The Strategy](#-the-strategy)
* [Installation](#-installation)
* [Usage](#-usage)
* [Disclaimer](#-disclaimer)

## ✨ Features

* **⚡ Asynchronous Processing:** Powered by `yahooquery` to fetch data for hundreds of tickers in parallel, drastically reducing wait times compared to standard loops.
* **📊 Technical Indicators:** Automatically calculates RSI, MACD, Bollinger Bands, SMA (14/40), EMA, and Volume Moving Averages.
* **🧠 Smart Filtering:** Applies strict logic to identify potential mean-reversion or momentum opportunities.
* **📂 Automated Workflow:** Reads from a CSV input, processes data, and saves a clean, sorted CSV output.
* **🛡️ Robust Logging:** Keeps a detailed log file (`_log.txt`) to track errors or missing data during execution.

## 📂 Project Structure

Ensure your folders are organized as follows before running the script:

```text
.
├── azioniDaComprare.py       # Main Application Script
├── azioni/
│   ├── CSVInput/
│   │   └── etf.csv           # Input file (Ticker, Name)
│   └── CSVOutput/
│       ├── etfDaComprare.csv # Generated Results
│       └── etf_log.txt       # Execution Log
```

## 💡 The Strategy

The screener analyzes weekly data (3 years history). A stock is flagged as a potential **BUY** only if it meets **ALL** the following conditions in the most recent period:

* **RSI (14):** Must be < 45 (Indicates the asset is not overbought).
* **Trend Context:** SMA 14 < SMA 40 (Looking for potential reversals in downtrends or deep pullbacks).
* **Bollinger Bands:** Price is closer to the Lower Band than the Upper Band.
* **Momentum Shift:** The RSI is currently rising (diff > 0).
* **MACD:** Signal Line > MACD.
* **Volume Spike:** Current volume > 14-period average volume.

## 🛠️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/jacopomino/quant-stock-screener-py.git
cd quant-stock-screener-py
```

2. **Install Dependencies**

This project relies on `yahooquery` for data and `pandas` for analysis.

```bash
pip install pandas yahooquery tqdm
```

## 💻 Usage

1. **Prepare your Input File**

Create a file named `etf.csv` inside `azioni/CSVInput/`.

Format: CSV with at least two columns: **Ticker** and **Name**.

Example:

```csv
AAPL,Apple Inc.
MSFT,Microsoft Corp.
TSLA,Tesla Inc.
```

2. **Run the Script**

```bash
python azioniDaComprare.py
```

**View Results:** Open `azioni/CSVOutput/etfDaComprare.csv`. The list will be sorted by **Average Volume** (highest liquidity first).

## ⚠️ Disclaimer

This software is for educational and research purposes only. Do not trade based solely on these signals. The strategy implemented is algorithmic and does not account for fundamental news, economic events, or market sentiment.

