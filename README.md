# Normal Distribution Visualizer for Finance / 金融向け正規分布可視化ツール

A Streamlit-based MVP project for interactive visualization of the normal distribution.
Streamlit ベースで正規分布を対話的に可視化する MVP プロジェクトです。

---

## Overview / 概要

**English:**
This project allows users to interactively explore the normal distribution by changing parameters such as mean and standard deviation.
It also supports PDF/CDF switching, interval probability calculation, and z-score inspection.

**日本語:**
このプロジェクトでは、平均や標準偏差を変更しながら正規分布を対話的に確認できます。
さらに、PDF/CDF の切り替え、区間確率の計算、z-score の確認にも対応しています。

---

## Features / 主な機能

- Interactive normal distribution visualization / 正規分布の対話的可視化
- Adjustable mean `μ` / 平均 `μ` の変更
- Adjustable standard deviation `σ` / 標準偏差 `σ` の変更
- PDF and CDF switching / PDF と CDF の切り替え
- Interval probability calculation / 区間確率の計算
- z-score display / z-score の表示
- Streamlit UI / Streamlit による UI

---

## Project Structure / ディレクトリ構成

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
