# Normal Distribution Visualizer for Finance / 金融向け正規分布可視化ツール

A Streamlit-based project for interactive normal distribution visualization, sampling, financial return comparison, skewness/kurtosis inspection, and simple VaR analysis.
Streamlit ベースで、正規分布の可視化、サンプル生成、金融リターン比較、歪度・尖度の確認、簡易 VaR 分析を行うプロジェクトです。

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
- skewness and kurtosis display
- simple VaR estimation

**日本語:**
このプロジェクトでは、以下を通して正規分布を対話的に理解できます。
- PDF/CDF の可視化
- 区間確率
- z-score 表示
- 乱数サンプル生成
- ヒストグラム比較
- 金融リターン分析
- 歪度・尖度の表示
- 簡易 VaR 推定

---

## Why These Features Matter / なぜこれらの機能が重要か

### 1. Random Sampling + Histogram / サンプル生成 + ヒストグラム
**English:**
This connects theory and experiment.
It shows how generated samples approximate a theoretical normal distribution.

**日本語:**
理論と実験をつなぐ機能です。
生成データが理論分布にどのように近づくかを確認できます。

### 2. Financial Return Comparison / 金融リターン比較
**English:**
This makes the project clearly finance-oriented.
It compares actual market return distributions with a fitted normal distribution.

**日本語:**
プロジェクトを金融寄りにする重要な機能です。
実際の市場リターン分布と当てはめた正規分布を比較できます。

### 3. Skewness and Kurtosis / 歪度・尖度
**English:**
These metrics quantify how real data differs from an ideal normal distribution.

**日本語:**
実データが理想的な正規分布とどの程度異なるかを数値で示せます。

### 4. Simple VaR / 簡易 VaR
**English:**
This adds a basic risk-management perspective and connects probability modeling to finance.

**日本語:**
リスク管理の視点を加え、確率モデルを金融分析につなげます。

### 5. VaR Lines on Histogram / ヒストグラム上の VaR 線
**English:**
These lines make risk thresholds visually intuitive.

**日本語:**
リスクの閾値がどこにあるのかを視覚的に理解しやすくします。

---

## Features / 主な機能

- Interactive normal distribution visualization / 正規分布の対話的可視化
- Adjustable mean `μ` / 平均 `μ` の変更
- Adjustable standard deviation `σ` / 標準偏差 `σ` の変更
- PDF and CDF switching / PDF と CDF の切り替え
- Interval probability calculation / 区間確率の計算
- z-score display / z-score の表示
- Random sampling and histogram overlay / サンプル生成とヒストグラム重ね描き
- Sample skewness and kurtosis / 標本の歪度・尖度
- Real financial return comparison / 実データの金融リターン比較
- Return skewness and kurtosis / リターンの歪度・尖度
- Historical and parametric VaR / ヒストリカル VaR とパラメトリック VaR
- VaR vertical lines on histogram / ヒストグラム上の VaR 縦線
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


---

## 仮想環境を作るならこうです。

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
