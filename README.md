# Normal Distribution for Finance

A simple Streamlit-based MVP project for visualizing the normal distribution and understanding its relevance to finance.

## Overview

This project provides an interactive visualization of the normal distribution.

Users can:
- adjust the mean `μ`
- adjust the standard deviation `σ`
- specify an interval `[a, b]`
- view the probability density function (PDF)
- calculate the probability that a value falls within the selected interval
- inspect z-scores for the interval bounds

This project is intended as a foundational learning tool for:
- probability and statistics
- quantitative finance
- risk management
- financial engineering

## Features

- Interactive normal distribution visualization
- Adjustable `μ` and `σ`
- Interval probability shading
- Probability calculation for `[a, b]`
- z-score display
- Streamlit UI for quick experimentation

## Project Structure

```plaintext
normal-distribution-for-finance/
├── app/
│   ├── main.py
│   ├── plots.py
│   └── stats_utils.py
├── images/
├── README.md
├── requirements.txt
└── .gitignore


## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


---

# 4. 実行方法

仮想環境を作るならこうです。

## Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py


## Windows PowerShell

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/main.py
