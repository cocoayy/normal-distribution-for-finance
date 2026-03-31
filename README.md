# Normal Distribution Visualizer for Finance / 金融向け正規分布可視化ツール

A Streamlit-based project for interactive normal distribution visualization, sampling, financial return comparison, skewness/kurtosis inspection, simple VaR analysis, and built-in explanatory notes.
Streamlit ベースで、正規分布の可視化、サンプル生成、金融リターン比較、歪度・尖度の確認、簡易 VaR 分析、そして解説ノート表示を行うプロジェクトです。

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
- built-in notes tab for explanations

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
- アプリ内の解説ノートタブ

---

## App Tabs / アプリのタブ構成

### 1. Visualizer / 可視化
- PDF / CDF display
- interval probability
- z-score
- parameter controls for `μ` and `σ`

### 2. Sampling & Finance / サンプルと金融
- random sampling and histogram
- sample skewness and kurtosis
- market return comparison
- fitted normal distribution
- historical and parametric VaR
- VaR vertical lines

### 3. Notes / 解説ノート
- purpose of the app
- explanations of formulas
- meanings of graphs
- finance interpretation

---

## Why This Project Is Strong / このプロジェクトが強い理由

**English:**
This project is not just a visualization toy.
It connects:
- mathematics
- probability
- simulation
- market data
- risk interpretation

**日本語:**
このプロジェクトは単なるグラフ描画ではありません。
以下をつないで見せられます。
- 数学
- 確率
- シミュレーション
- 実市場データ
- リスク解釈

---

## Project Structure / ディレクトリ構成

```plaintext
normal-distribution-for-finance/
├── app/
│   ├── main.py
│   ├── plots.py
│   ├── stats_utils.py
│   └── notes.py
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
