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
from notes import render_notes_tab


# -------------------------------------------------------
# Page configuration / ページ設定
# -------------------------------------------------------
st.set_page_config(
    page_title="Normal Distribution Visualizer for Finance / 金融向け正規分布ビジュアライザ",
    page_icon="📈",
    layout="wide",
)

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

# -------------------------------------------------------
# Top-level tabs / 上位タブ
# -------------------------------------------------------
tab_visualizer, tab_sampling_finance, tab_notes = st.tabs(
    [
        "Visualizer / 可視化",
        "Sampling & Finance / サンプルと金融",
        "Notes / 解説ノート",
    ]
)

# =======================================================
# Tab 1: Visualizer / 可視化
# =======================================================
with tab_visualizer:
    st.subheader("Distribution Visualizer / 分布可視化")

    st.write(
        """
        **English:**
        Explore the normal distribution by changing parameters and checking interval probability.

        **日本語:**
        パラメータを変更しながら、正規分布と区間確率を確認できます。
        """
    )

    control_col1, control_col2 = st.columns([1, 2])

    with control_col1:
        mode = st.radio(
            "Display Mode / 表示モード",
            options=["PDF", "CDF"],
            index=0,
        )

        mu = st.slider(
            label="Mean (μ) / 平均 (μ)",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=0.1,
        )

        sigma = st.slider(
            label="Standard Deviation (σ) / 標準偏差 (σ)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
        )

        st.markdown("---")
        st.markdown("### Probability Interval / 確率区間")

        lower = st.number_input(
            label="Lower Bound / 下限",
            value=-1.0,
            step=0.1,
        )

        upper = st.number_input(
            label="Upper Bound / 上限",
            value=1.0,
            step=0.1,
        )

        if lower > upper:
            lower, upper = upper, lower

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

    with control_col2:
        st.plotly_chart(fig, use_container_width=True)

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    with summary_col1:
        st.metric("Mean (μ) / 平均", f"{mu:.4f}")
        st.metric("Standard Deviation (σ) / 標準偏差", f"{sigma:.4f}")
    with summary_col2:
        st.metric("Interval Probability / 区間確率", f"{prob:.6f}")
        st.metric("z-score(lower) / 下限 zスコア", f"{z_lower:.4f}")
    with summary_col3:
        st.metric("Mode / モード", mode)
        st.metric("z-score(upper) / 上限 zスコア", f"{z_upper:.4f}")

# =======================================================
# Tab 2: Sampling & Finance / サンプルと金融
# =======================================================
with tab_sampling_finance:
    st.subheader("Sampling and Financial Analysis / サンプル生成と金融分析")

    # ------------------------------------------
    # Sampling section / サンプリング
    # ------------------------------------------
    st.markdown("## Random Sampling / サンプル生成")
    st.write(
        """
        **English:**
        Compare randomly generated samples with the theoretical normal distribution.

        **日本語:**
        正規分布から生成した乱数サンプルと理論分布を比較します。
        """
    )

    sample_col1, sample_col2 = st.columns([1, 2])

    with sample_col1:
        sample_mu = st.slider(
            "Sample Mean (μ) / サンプル用平均 (μ)",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=0.1,
            key="sample_mu",
        )

        sample_sigma = st.slider(
            "Sample Std (σ) / サンプル用標準偏差 (σ)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            key="sample_sigma",
        )

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
        mu=sample_mu,
        sigma=sample_sigma,
        sample_size=sample_size,
        random_seed=int(random_seed),
    )

    x_hist = generate_x_range(mu=sample_mu, sigma=sample_sigma)
    y_hist = normal_pdf(x_hist, mu=sample_mu, sigma=sample_sigma)

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
        st.metric("Sample Mean / 標本平均", f"{sample_mean:.4f}", delta=f"{sample_mean - sample_mu:.4f}")
    with m2:
        st.metric("Sample Std / 標本標準偏差", f"{sample_std:.4f}", delta=f"{sample_std - sample_sigma:.4f}")
    with m3:
        st.metric("Sample Skewness / 標本歪度", f"{sample_skew:.4f}")
    with m4:
        st.metric("Sample Excess Kurtosis / 標本超過尖度", f"{sample_excess_kurt:.4f}")

    st.write(f"**Sample Shape Comment / 標本分布コメント:** {sample_shape_comment}")

    st.markdown("---")

    # ------------------------------------------
    # Finance section / 金融分析
    # ------------------------------------------
    st.markdown("## Financial Return Comparison / 金融リターン比較")
    st.write(
        """
        **English:**
        Download real market data, convert it into daily returns, and compare the histogram to a fitted normal distribution.

        **日本語:**
        実際の市場データを取得して日次リターンに変換し、そのヒストグラムを当てはめた正規分布と比較します。
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

        st.write(f"**Distribution Comment / 分布コメント:** {return_shape_comment}")

        st.markdown("### Simple VaR Display / 簡易 VaR 表示")

        var_col1, var_col2, var_col3 = st.columns(3)
        with var_col1:
            st.markdown("#### Historical VaR / ヒストリカル VaR")
            st.write(f"**VaR Return / VaR リターン:** {hist_var_return:.6f}")
            st.write(f"**VaR Amount / VaR 金額:** {hist_var_amount:,.2f}")

        with var_col2:
            st.markdown("#### Parametric VaR / パラメトリック VaR")
            st.write(f"**VaR Return / VaR リターン:** {param_var_return:.6f}")
            st.write(f"**VaR Amount / VaR 金額:** {param_var_amount:,.2f}")

        with var_col3:
            var_gap = hist_var_amount - param_var_amount
            st.markdown("#### VaR Gap / VaR差分")
            st.write(f"**Gap Amount / 差分金額:** {var_gap:,.2f}")
            st.write("**Meaning / 意味:** positive = historical risk is larger / 正なら過去データベースの方が大きい")

    except Exception as e:
        with finance_col2:
            st.error(
                f"Failed to fetch or process financial data / 金融データの取得または処理に失敗しました: {e}"
            )

# =======================================================
# Tab 3: Notes / 解説ノート
# =======================================================
with tab_notes:
    render_notes_tab()
