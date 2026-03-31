# Normal Distribution Visualizer for Finance / 金融向け正規分布可視化ツール

A Streamlit-based MVP project for interactive visualization of the normal distribution, sampling, financial return comparison, and simple VaR analysis.
Streamlit ベースで、正規分布の可視化、サンプル生成、金融リターン比較、簡易 VaR 分析を行うプロジェクトです。

---

## Overview / 概要

**English:**
This project helps users understand the normal distribution interactively through:
- PDF/CDF visualization
- interval probability
- z-score display
- random sample generation
- histogram comparison
- financial return analysis
- simple VaR estimation

**日本語:**
このプロジェクトでは、以下を通して正規分布を対話的に理解できます。
- PDF/CDF の可視化
- 区間確率
- z-score 表示
- 乱数サンプル生成
- ヒストグラム比較
- 金融リターン分析
- 簡易 VaR 推定

---

## Why These Features Matter / なぜこれらの機能が重要か

### 1. Random Sampling + Histogram / サンプル生成 + ヒストグラム
**English:**
This feature connects theory and experiment.
Instead of only drawing a formula-based curve, the app shows how sampled data approximates the theoretical distribution.

**日本語:**
この機能は、理論と実験をつなぎます。
式から描いた理論曲線だけでなく、実際に生成したデータがどのように理論分布に近づくかを確認できます。

### 2. Financial Return Comparison / 金融リターン比較
**English:**
This makes the project more finance-oriented.
Users can compare actual market return distributions with a fitted normal distribution.

**日本語:**
この機能によって、プロジェクトが金融寄りになります。
実際の市場データのリターン分布と、当てはめた正規分布を比較できます。

### 3. Simple VaR Display / 簡易 VaR 表示
**English:**
This adds a risk-management perspective.
The app moves from “distribution visualization” toward “basic quantitative finance analysis.”

**日本語:**
この機能で、リスク管理の視点が加わります。
単なる分布の可視化から、基礎的な金融分析ツールへ一歩進みます。

---

## Features / 主な機能

- Interactive normal distribution visualization / 正規分布の対話的可視化
- Adjustable mean `μ` / 平均 `μ` の変更
- Adjustable standard deviation `σ` / 標準偏差 `σ` の変更
- PDF and CDF switching / PDF と CDF の切り替え
- Interval probability calculation / 区間確率の計算
- z-score display / z-score の表示
- Random sampling and histogram overlay / サンプル生成とヒストグラム重ね描き
- Real financial return comparison / 実データの金融リターン比較
- Historical and parametric VaR / ヒストリカル VaR とパラメトリック VaR
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
