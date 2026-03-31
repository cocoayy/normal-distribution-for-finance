import streamlit as st

from stats_utils import (
    generate_x_range,
    normal_pdf,
    normal_cdf,
    interval_probability,
    z_score,
)
from plots import create_distribution_figure


# Page configuration / ページ設定
st.set_page_config(
    page_title="Normal Distribution Visualizer for Finance / 金融向け正規分布ビジュアライザ",
    page_icon="📈",
    layout="wide",
)

# Title / タイトル
st.title("📈 Normal Distribution Visualizer for Finance / 金融向け正規分布可視化ツール")

st.write(
    """
    **English:**
    This Streamlit app helps users interactively understand the normal distribution through parameter changes,
    interval probability, and PDF/CDF visualization.

    **日本語:**
    この Streamlit アプリでは、平均や標準偏差の変更、区間確率、PDF/CDF の可視化を通して、
    正規分布を対話的に理解できます。
    """
)

st.markdown("---")

# Sidebar / サイドバー
st.sidebar.header("Controls / 操作パネル")

mode = st.sidebar.radio(
    "Display Mode / 表示モード",
    options=["PDF", "CDF"],
    index=0,
)

mu = st.sidebar.slider(
    label="Mean (μ) / 平均 (μ)",
    min_value=-10.0,
    max_value=10.0,
    value=0.0,
    step=0.1,
)

sigma = st.sidebar.slider(
    label="Standard Deviation (σ) / 標準偏差 (σ)",
    min_value=0.1,
    max_value=10.0,
    value=1.0,
    step=0.1,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Probability Interval / 確率区間")

lower = st.sidebar.number_input(
    label="Lower Bound / 下限",
    value=-1.0,
    step=0.1,
)

upper = st.sidebar.number_input(
    label="Upper Bound / 上限",
    value=1.0,
    step=0.1,
)

# Swap if lower > upper / lower > upper の場合は入れ替え
if lower > upper:
    lower, upper = upper, lower

# Generate data / データ生成
x = generate_x_range(mu=mu, sigma=sigma)

if mode == "PDF":
    y = normal_pdf(x=x, mu=mu, sigma=sigma)
else:
    y = normal_cdf(x=x, mu=mu, sigma=sigma)

# Calculate interval probability / 区間確率を計算
prob = interval_probability(lower=lower, upper=upper, mu=mu, sigma=sigma)

# z-scores / z-score 計算
z_lower = z_score(lower, mu, sigma)
z_upper = z_score(upper, mu, sigma)

# Create figure / グラフ作成
fig = create_distribution_figure(
    x=x,
    y=y,
    mu=mu,
    sigma=sigma,
    lower=lower,
    upper=upper,
    mode=mode,
)

# Layout / レイアウト
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Summary / 概要")

    st.write(f"**Mode / モード:** {mode}")
    st.write(f"**Mean (μ) / 平均 (μ):** {mu:.2f}")
    st.write(f"**Standard Deviation (σ) / 標準偏差 (σ):** {sigma:.2f}")
    st.write(f"**Interval / 区間:** [{lower:.2f}, {upper:.2f}]")
    st.write(f"**Probability / 区間確率:** {prob:.6f}")
    st.write(f"**z-score(lower) / 下限の z-score:** {z_lower:.4f}")
    st.write(f"**z-score(upper) / 上限の z-score:** {z_upper:.4f}")

    st.markdown("---")
    st.subheader("Interpretation / 解釈")
    st.write(
        """
        **English:**
        - Increasing μ shifts the distribution horizontally.
        - Increasing σ makes the distribution wider.
        - The interval probability shows how likely values fall within the selected range.

        **日本語:**
        - μ が大きくなると、分布全体が左右に移動します。
        - σ が大きくなると、分布は横に広がります。
        - 区間確率は、指定範囲に値が入る確率を表します。
        """
    )

st.markdown("---")

st.subheader("What is PDF? / PDF とは")
st.write(
    """
    **English:**
    PDF (Probability Density Function) describes the relative likelihood of a continuous random variable.

    **日本語:**
    PDF（確率密度関数）は、連続確率変数が各値の近くを取る「相対的な起こりやすさ」を表します。
    """
)

st.subheader("What is CDF? / CDF とは")
st.write(
    """
    **English:**
    CDF (Cumulative Distribution Function) gives the probability that a random variable is less than or equal to x.

    **日本語:**
    CDF（累積分布関数）は、確率変数が x 以下になる確率を表します。
    """
)

st.subheader("Why This Matters in Finance / なぜ金融で重要か")
st.write(
    """
    **English:**
    Normal distributions appear in introductory statistics, quantitative finance, and risk management.
    They are useful for understanding return distributions, volatility, z-scores, and confidence intervals.

    **日本語:**
    正規分布は、統計学の基礎だけでなく、クオンツ金融やリスク管理の入り口として重要です。
    リターン分布、ボラティリティ、z-score、信頼区間などを理解する土台になります。
    """
)
