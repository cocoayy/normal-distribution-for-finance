import streamlit as st
import numpy as np

from stats_utils import (
    generate_x_range,
    normal_pdf,
    normal_cdf,
    interval_probability,
    z_score,
    generate_samples,
    fetch_return_series,
    fit_normal_to_returns,
    calculate_var_from_returns,
    calculate_parametric_var,
    calculate_distribution_shape_metrics,
    interpret_shape_metrics,
)
from plots import (
    create_distribution_figure,
    create_histogram_with_pdf,
    create_returns_histogram_with_fit,
)


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
    interval probability, PDF/CDF visualization, random sampling, financial return comparison, and simple VaR analysis.

    **日本語:**
    この Streamlit アプリでは、平均や標準偏差の変更、区間確率、PDF/CDF の可視化に加えて、
    サンプル生成、金融リターン比較、簡易 VaR 分析を通して、正規分布を対話的に理解できます。
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

if lower > upper:
    lower, upper = upper, lower

# Main distribution data / メイン分布データ
x = generate_x_range(mu=mu, sigma=sigma)

if mode == "PDF":
    y = normal_pdf(x=x, mu=mu, sigma=sigma)
else:
    y = normal_cdf(x=x, mu=mu, sigma=sigma)

prob = interval_probability(lower=lower, upper=upper, mu=mu, sigma=sigma)
z_lower = z_score(lower, mu, sigma)
z_upper = z_score(upper, mu, sigma)

fig = create_distribution_figure(
    x=x,
    y=y,
    mu=mu,
    sigma=sigma,
    lower=lower,
    upper=upper,
    mode=mode,
)

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

# =======================================================
# Random sampling section / サンプル生成セクション
# =======================================================
st.subheader("Random Sampling and Histogram / サンプル生成とヒストグラム")

st.write(
    """
    **English:**
    This section compares randomly generated samples with the theoretical normal distribution.

    **日本語:**
    このセクションでは、正規分布から生成した乱数サンプルと理論分布を比較できます。
    """
)

sample_col1, sample_col2 = st.columns([1, 2])

with sample_col1:
    sample_size = st.slider(
        "Sample Size / サンプル数",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
    )

    random_seed = st.number_input(
        "Random Seed / 乱数シード",
        min_value=0,
        max_value=999999,
        value=42,
        step=1,
    )

samples = generate_samples(
    mu=mu,
    sigma=sigma,
    sample_size=sample_size,
    random_seed=int(random_seed),
)

x_hist = generate_x_range(mu=mu, sigma=sigma)
y_hist = normal_pdf(x_hist, mu=mu, sigma=sigma)

hist_fig = create_histogram_with_pdf(
    samples=samples,
    x_curve=x_hist,
    y_curve=y_hist,
    title="Generated Samples vs Theoretical PDF / 生成サンプルと理論PDFの比較",
)

with sample_col2:
    st.plotly_chart(hist_fig, use_container_width=True)

sample_mean = float(np.mean(samples))
sample_std = float(np.std(samples, ddof=1))
sample_skew, sample_excess_kurt = calculate_distribution_shape_metrics(samples)
sample_shape_comment = interpret_shape_metrics(sample_skew, sample_excess_kurt)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Sample Mean / 標本平均", f"{sample_mean:.4f}", delta=f"{sample_mean - mu:.4f}")
with m2:
    st.metric("Sample Std / 標本標準偏差", f"{sample_std:.4f}", delta=f"{sample_std - sigma:.4f}")
with m3:
    st.metric("Sample Skewness / 標本歪度", f"{sample_skew:.4f}")
with m4:
    st.metric("Sample Excess Kurtosis / 標本超過尖度", f"{sample_excess_kurt:.4f}")

st.write(
    f"""
    **Sample Shape Comment / 標本分布コメント:**
    {sample_shape_comment}
    """
)

st.markdown("---")

# =======================================================
# Financial return comparison / 金融リターン比較
# =======================================================
st.subheader("Financial Return Comparison / 金融リターン比較")

st.write(
    """
    **English:**
    Download real market data, convert it into daily returns, and compare the histogram to a fitted normal distribution.

    **日本語:**
    実際の市場データを取得して日次リターンに変換し、そのヒストグラムを当てはめた正規分布と比較できます。
    """
)

finance_col1, finance_col2 = st.columns([1, 2])

with finance_col1:
    ticker = st.text_input(
        "Ticker Symbol / 銘柄コード",
        value="AAPL",
        help="Examples: AAPL, MSFT, 7203.T, 6758.T",
    )

    period = st.selectbox(
        "Data Period / データ期間",
        options=["6mo", "1y", "2y", "5y"],
        index=1,
    )

    investment_amount = st.number_input(
        "Investment Amount / 投資額",
        min_value=1000.0,
        value=1000000.0,
        step=1000.0,
    )

    confidence_level = st.selectbox(
        "Confidence Level / 信頼水準",
        options=[0.90, 0.95, 0.99],
        index=1,
    )

try:
    returns = fetch_return_series(ticker=ticker, period=period)
    return_mu, return_sigma = fit_normal_to_returns(returns)

    hist_var_return, hist_var_amount = calculate_var_from_returns(
        returns=returns,
        confidence_level=confidence_level,
        investment_amount=investment_amount,
    )

    param_var_return, param_var_amount = calculate_parametric_var(
        mu=return_mu,
        sigma=return_sigma,
        confidence_level=confidence_level,
        investment_amount=investment_amount,
    )

    x_returns = np.linspace(float(returns.min()), float(returns.max()), 1000)
    y_returns = normal_pdf(x_returns, return_mu, return_sigma)

    returns_fig = create_returns_histogram_with_fit(
        returns=returns.to_numpy(),
        x_curve=x_returns,
        y_curve=y_returns,
        title=f"{ticker} Returns vs Fitted Normal / {ticker} のリターンと正規分布比較",
        hist_var_return=hist_var_return,
        param_var_return=param_var_return,
    )

    with finance_col2:
        st.plotly_chart(returns_fig, use_container_width=True)

    return_skew, return_excess_kurt = calculate_distribution_shape_metrics(returns)
    return_shape_comment = interpret_shape_metrics(return_skew, return_excess_kurt)

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Mean Return / 平均リターン", f"{return_mu:.6f}")
    with r2:
        st.metric("Return Std / リターン標準偏差", f"{return_sigma:.6f}")
    with r3:
        st.metric("Skewness / 歪度", f"{return_skew:.4f}")
    with r4:
        st.metric("Excess Kurtosis / 超過尖度", f"{return_excess_kurt:.4f}")

    st.write(
        f"""
        **Distribution Comment / 分布コメント:**
        {return_shape_comment}
        """
    )

    st.write(
        """
        **English:**
        If the histogram and fitted curve differ substantially, it suggests real-world returns may not follow a perfect normal distribution.

        **日本語:**
        ヒストグラムと当てはめ曲線に大きな差がある場合、実際の金融リターンは完全な正規分布ではない可能性があります。
        """
    )

    st.markdown("---")

    # ===================================================
    # VaR section / VaR セクション
    # ===================================================
    st.subheader("Simple VaR Display / 簡易 VaR 表示")

    st.write(
        """
        **English:**
        VaR (Value at Risk) is a simple risk indicator that estimates potential loss under a given confidence level.

        **日本語:**
        VaR（Value at Risk）は、ある信頼水準のもとで想定される損失を表す基本的なリスク指標です。
        """
    )

    var_col1, var_col2, var_col3 = st.columns(3)

    with var_col1:
        st.markdown("### Historical VaR / ヒストリカル VaR")
        st.write(f"**VaR Return / VaR リターン:** {hist_var_return:.6f}")
        st.write(f"**VaR Amount / VaR 金額:** {hist_var_amount:,.2f}")

    with var_col2:
        st.markdown("### Parametric VaR / パラメトリック VaR")
        st.write(f"**VaR Return / VaR リターン:** {param_var_return:.6f}")
        st.write(f"**VaR Amount / VaR 金額:** {param_var_amount:,.2f}")

    with var_col3:
        var_gap = hist_var_amount - param_var_amount
        st.markdown("### VaR Gap / VaR差分")
        st.write(f"**Gap Amount / 差分金額:** {var_gap:,.2f}")
        st.write(
            "**Meaning / 意味:** "
            "positive = historical risk is larger / 正なら過去データベースの方が大きい"
        )

    st.write(
        f"""
        **English:**
        At the {int(confidence_level * 100)}% confidence level, the vertical lines on the return histogram show
        where historical VaR and normal-assumption VaR are located.

        **日本語:**
        信頼水準 {int(confidence_level * 100)}% において、ヒストグラム上の縦線は
        ヒストリカル VaR と正規分布仮定の VaR がどこに位置するかを示しています。
        """
    )

except Exception as e:
    with finance_col2:
        st.error(
            f"Failed to fetch or process financial data / 金融データの取得または処理に失敗しました: {e}"
        )

st.markdown("---")

st.subheader("What is PDF? / PDF とは")
st.write(
    """
    **English:**
    PDF (Probability Density Function) describes the relative likelihood of a continuous random variable.

    **日本語:**
    PDF（確率密度関数）は、連続確率変数が各値の近くを取る相対的な起こりやすさを表します。
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

st.subheader("What are Skewness and Kurtosis? / 歪度と尖度とは")
st.write(
    """
    **English:**
    Skewness measures asymmetry in a distribution.
    Excess kurtosis measures tail heaviness relative to a normal distribution.

    **日本語:**
    歪度は分布の左右非対称性を表します。
    超過尖度は、正規分布と比べて裾がどれくらい厚いかを表します。
    """
)

st.subheader("Why This Matters in Finance / なぜ金融で重要か")
st.write(
    """
    **English:**
    Normal distributions appear in introductory statistics, quantitative finance, and risk management.
    Comparing theoretical curves, sampled data, real returns, skewness, kurtosis, and VaR helps users understand
    both the usefulness and the limitations of the normality assumption.

    **日本語:**
    正規分布は、統計学の基礎だけでなく、クオンツ金融やリスク管理の入り口として重要です。
    理論曲線、標本、実データ、歪度、尖度、VaR を比較することで、
    正規分布仮定の有用性と限界の両方を理解しやすくなります。
    """
)
