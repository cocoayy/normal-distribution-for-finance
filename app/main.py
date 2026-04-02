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
    calculate_qq_plot_data,
    calculate_rolling_volatility,
    parse_ticker_list,
    build_multi_ticker_summary,
)
from plots import (
    create_distribution_figure,
    create_histogram_with_pdf,
    create_returns_histogram_with_fit,
    create_qq_plot,
    create_rolling_volatility_plot,
    create_multi_rolling_volatility_plot,
)
from notes import render_notes_tab


# ページ設定
st.set_page_config(
    page_title="金融向け正規分布可視化ツール",
    page_icon="📈",
    layout="wide",
)

st.title("📈 金融向け正規分布可視化ツール")

st.write(
    """
    このアプリでは、平均や標準偏差の変更、区間確率、PDF/CDF の可視化に加えて、
    サンプル生成、金融リターン比較、歪度・尖度、QQプロット、ローリングボラティリティ、
    複数銘柄比較、簡易 VaR 分析を通して、正規分布と金融リスクを対話的に理解できます。
    """
)

st.markdown("---")

tab_visualizer, tab_sampling_finance, tab_notes = st.tabs(
    [
        "可視化",
        "サンプルと金融",
        "解説ノート",
    ]
)

with tab_visualizer:
    st.subheader("分布可視化")
    st.write("パラメータを変更しながら、正規分布と区間確率を確認できます。")

    control_col1, control_col2 = st.columns([1, 2])

    with control_col1:
        mode = st.radio("表示モード", options=["PDF", "CDF"], index=0)
        mu = st.slider("平均 μ", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
        sigma = st.slider("標準偏差 σ", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

        st.markdown("---")
        st.markdown("### 確率区間")
        lower = st.number_input("下限", value=-1.0, step=0.1)
        upper = st.number_input("上限", value=1.0, step=0.1)

        if lower > upper:
            lower, upper = upper, lower

    x = generate_x_range(mu=mu, sigma=sigma)
    y = normal_pdf(x=x, mu=mu, sigma=sigma) if mode == "PDF" else normal_cdf(x=x, mu=mu, sigma=sigma)

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
        st.metric("平均 μ", f"{mu:.4f}")
        st.metric("標準偏差 σ", f"{sigma:.4f}")
    with summary_col2:
        st.metric("区間確率", f"{prob:.6f}")
        st.metric("下限 zスコア", f"{z_lower:.4f}")
    with summary_col3:
        st.metric("表示モード", mode)
        st.metric("上限 zスコア", f"{z_upper:.4f}")

with tab_sampling_finance:
    st.subheader("サンプル生成と金融分析")

    st.markdown("## サンプル生成")
    st.write("正規分布から生成した乱数サンプルと理論分布を比較します。")

    sample_col1, sample_col2 = st.columns([1, 2])

    with sample_col1:
        sample_mu = st.slider("サンプル用平均 μ", -10.0, 10.0, 0.0, 0.1, key="sample_mu")
        sample_sigma = st.slider("サンプル用標準偏差 σ", 0.1, 10.0, 1.0, 0.1, key="sample_sigma")
        sample_size = st.slider("サンプル数", 100, 10000, 1000, 100)
        random_seed = st.number_input("乱数シード", min_value=0, max_value=999999, value=42, step=1)

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
        title="生成サンプルと理論PDFの比較",
    )

    with sample_col2:
        st.plotly_chart(hist_fig, use_container_width=True)

    sample_mean = float(np.mean(samples))
    sample_std = float(np.std(samples, ddof=1))
    sample_skew, sample_excess_kurt = calculate_distribution_shape_metrics(samples)
    sample_shape_comment = interpret_shape_metrics(sample_skew, sample_excess_kurt)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("標本平均", f"{sample_mean:.4f}", delta=f"{sample_mean - sample_mu:.4f}")
    with m2:
        st.metric("標本標準偏差", f"{sample_std:.4f}", delta=f"{sample_std - sample_sigma:.4f}")
    with m3:
        st.metric("標本歪度", f"{sample_skew:.4f}")
    with m4:
        st.metric("標本超過尖度", f"{sample_excess_kurt:.4f}")

    st.write(f"**標本分布コメント:** {sample_shape_comment}")

    st.markdown("---")

    st.markdown("## 単一銘柄の金融リターン比較")
    st.write("実際の市場データを取得して日次リターンに変換し、そのヒストグラムを正規分布と比較します。")

    finance_col1, finance_col2 = st.columns([1, 2])

    with finance_col1:
        ticker = st.text_input("銘柄コード（Ticker）", value="AAPL", help="例: AAPL, MSFT, 7203.T, 6758.T")
        period = st.selectbox("データ期間", options=["6mo", "1y", "2y", "5y"], index=1)
        investment_amount = st.number_input("投資額", min_value=1000.0, value=1000000.0, step=1000.0)
        confidence_level = st.selectbox("信頼水準", options=[0.90, 0.95, 0.99], index=1)
        rolling_window = st.slider("ローリング窓幅（日数）", min_value=5, max_value=120, value=20, step=1)

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
            title=f"{ticker} のリターンと正規分布比較",
            hist_var_return=hist_var_return,
            param_var_return=param_var_return,
        )

        with finance_col2:
            st.plotly_chart(returns_fig, use_container_width=True)

        return_skew, return_excess_kurt = calculate_distribution_shape_metrics(returns)
        return_shape_comment = interpret_shape_metrics(return_skew, return_excess_kurt)

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("平均リターン", f"{return_mu:.6f}")
        with r2:
            st.metric("リターン標準偏差", f"{return_sigma:.6f}")
        with r3:
            st.metric("歪度", f"{return_skew:.4f}")
        with r4:
            st.metric("超過尖度", f"{return_excess_kurt:.4f}")

        st.write(f"**分布コメント:** {return_shape_comment}")

        st.markdown("### QQプロット")
        st.write("実データが正規分布に近いかどうかを確認します。")

        qq_x, qq_y, qq_slope, qq_intercept = calculate_qq_plot_data(returns)
        qq_fig = create_qq_plot(
            theoretical_quantiles=qq_x,
            ordered_values=qq_y,
            slope=qq_slope,
            intercept=qq_intercept,
            title=f"{ticker} のQQプロット",
        )
        st.plotly_chart(qq_fig, use_container_width=True)

        st.markdown("### ローリングボラティリティ")
        st.write("時間とともにボラティリティがどう変化したかを確認します。")

        rolling_vol = calculate_rolling_volatility(
            returns=returns,
            window=rolling_window,
            annualization_factor=252,
        )
        rolling_fig = create_rolling_volatility_plot(
            rolling_vol=rolling_vol,
            title=f"{ticker} のローリングボラティリティ（{rolling_window}日）",
        )
        st.plotly_chart(rolling_fig, use_container_width=True)

        latest_vol = float(rolling_vol.iloc[-1])
        avg_vol = float(rolling_vol.mean())
        max_vol = float(rolling_vol.max())

        rv1, rv2, rv3 = st.columns(3)
        with rv1:
            st.metric("直近ボラティリティ", f"{latest_vol:.4f}")
        with rv2:
            st.metric("平均ボラティリティ", f"{avg_vol:.4f}")
        with rv3:
            st.metric("最大ボラティリティ", f"{max_vol:.4f}")

        st.markdown("### 簡易 VaR 表示")

        var_col1, var_col2, var_col3 = st.columns(3)
        with var_col1:
            st.markdown("#### ヒストリカル VaR")
            st.write(f"**VaR リターン:** {hist_var_return:.6f}")
            st.write(f"**VaR 金額:** {hist_var_amount:,.2f}")

        with var_col2:
            st.markdown("#### パラメトリック VaR")
            st.write(f"**VaR リターン:** {param_var_return:.6f}")
            st.write(f"**VaR 金額:** {param_var_amount:,.2f}")

        with var_col3:
            var_gap = hist_var_amount - param_var_amount
            st.markdown("#### VaR差分")
            st.write(f"**差分金額:** {var_gap:,.2f}")
            st.write("正の値なら、過去データベースのリスク見積もりの方が大きいことを意味します。")

    except Exception as e:
        with finance_col2:
            st.error(f"金融データの取得または処理に失敗しました: {e}")

    st.markdown("---")

    st.markdown("## 複数銘柄比較")
    st.write("複数の銘柄を同じ指標で横並び比較できます。")

    multi_col1, multi_col2 = st.columns([1, 2])

    with multi_col1:
        multi_ticker_text = st.text_input(
            "比較する銘柄コード（カンマ区切り）",
            value="AAPL, MSFT, GOOGL",
            help="例: AAPL, MSFT, GOOGL または 7203.T, 6758.T, 9984.T",
        )
        multi_period = st.selectbox(
            "比較用データ期間",
            options=["6mo", "1y", "2y", "5y"],
            index=1,
            key="multi_period",
        )
        multi_confidence_level = st.selectbox(
            "比較用信頼水準",
            options=[0.90, 0.95, 0.99],
            index=1,
            key="multi_confidence_level",
        )
        multi_investment_amount = st.number_input(
            "比較用投資額",
            min_value=1000.0,
            value=1000000.0,
            step=1000.0,
            key="multi_investment_amount",
        )
        multi_rolling_window = st.slider(
            "比較用ローリング窓幅（日数）",
            min_value=5,
            max_value=120,
            value=20,
            step=1,
            key="multi_rolling_window",
        )

    try:
        multi_tickers = parse_ticker_list(multi_ticker_text)

        if len(multi_tickers) < 2:
            st.warning("複数銘柄比較を行うには、2つ以上の銘柄コードを入力してください。")
        else:
            summary_df, rolling_vol_df = build_multi_ticker_summary(
                tickers=multi_tickers,
                period=multi_period,
                confidence_level=multi_confidence_level,
                investment_amount=multi_investment_amount,
                rolling_window=multi_rolling_window,
            )

            with multi_col2:
                multi_roll_fig = create_multi_rolling_volatility_plot(
                    rolling_vol_df=rolling_vol_df,
                    title=f"複数銘柄のローリングボラティリティ比較（{multi_rolling_window}日）",
                )
                st.plotly_chart(multi_roll_fig, use_container_width=True)

            st.markdown("### 比較サマリー表")
            st.dataframe(summary_df, use_container_width=True)

            st.markdown("### 見方")
            st.write(
                """
                - **平均リターン** が高いほど、その期間の平均的な収益率は高いです。
                - **標準偏差** や **直近ローリングボラティリティ** が大きいほど、変動性が高いです。
                - **超過尖度** が大きいほど、極端な値が出やすい傾向があります。
                - **VaR 金額** が大きいほど、損失見積もりが大きいことを意味します。
                """
            )

    except Exception as e:
        with multi_col2:
            st.error(f"複数銘柄比較の処理に失敗しました: {e}")

with tab_notes:
    render_notes_tab()
