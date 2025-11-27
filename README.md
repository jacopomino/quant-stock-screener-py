# 📈 Quantitative Stock & ETF Screener

A high-performance Python tool designed to automate technical analysis for financial assets. It processes lists of tickers asynchronously using **Yahoo Finance** data and filters for specific "Buy" signals based on a custom statistical strategy.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [The Strategy](#-the-strategy)
- [Installation](#-installation)
- [Usage](#-usage)
- [Disclaimer](#-disclaimer)

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
