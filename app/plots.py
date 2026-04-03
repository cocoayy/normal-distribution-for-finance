import numpy as np
import pandas as pd
import plotly.graph_objects as go


def create_distribution_figure(
    x: np.ndarray,
    y: np.ndarray,
    mu: float,
    sigma: float,
    lower: float,
    upper: float,
    mode: str,
) -> go.Figure:
    """
    PDF または CDF の可視化用グラフを作成する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=mode,
        )
    )

    mask = (x >= lower) & (x <= upper)
    x_fill = x[mask]
    y_fill = y[mask]

    if len(x_fill) > 1:
        if mode == "PDF":
            fig.add_trace(
                go.Scatter(
                    x=np.concatenate(([x_fill[0]], x_fill, [x_fill[-1]])),
                    y=np.concatenate(([0], y_fill, [0])),
                    fill="toself",
                    mode="lines",
                    name="指定区間",
                )
            )
        elif mode == "CDF":
            fig.add_trace(
                go.Scatter(
                    x=x_fill,
                    y=y_fill,
                    mode="lines",
                    name="指定区間",
                    line=dict(width=4),
                )
            )

    fig.add_vline(
        x=mu,
        line_dash="dash",
        annotation_text=f"μ = {mu:.2f}",
        annotation_position="top",
    )

    fig.add_vline(
        x=lower,
        line_dash="dot",
        annotation_text=f"下限 = {lower:.2f}",
        annotation_position="bottom left",
    )
    fig.add_vline(
        x=upper,
        line_dash="dot",
        annotation_text=f"上限 = {upper:.2f}",
        annotation_position="bottom right",
    )

    title_map = {
        "PDF": "正規分布の確率密度関数（PDF）",
        "CDF": "正規分布の累積分布関数（CDF）",
    }

    yaxis_map = {
        "PDF": "確率密度",
        "CDF": "累積確率",
    }

    fig.update_layout(
        title=title_map.get(mode, "分布"),
        xaxis_title="x",
        yaxis_title=yaxis_map.get(mode, "値"),
        template="plotly_white",
        legend_title="凡例",
    )

    fig.add_annotation(
        x=0.98,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"μ = {mu:.2f}<br>σ = {sigma:.2f}<br>モード = {mode}",
        showarrow=False,
        align="right",
        borderpad=6,
    )

    return fig


def create_histogram_with_pdf(
    samples: np.ndarray,
    x_curve: np.ndarray,
    y_curve: np.ndarray,
    title: str,
    nbins: int = 40,
) -> go.Figure:
    """
    サンプルのヒストグラムに理論 PDF を重ねる。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=samples,
            nbinsx=nbins,
            histnorm="probability density",
            name="ヒストグラム",
            opacity=0.75,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_curve,
            y=y_curve,
            mode="lines",
            name="正規分布PDF",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="値",
        yaxis_title="密度",
        template="plotly_white",
        barmode="overlay",
        legend_title="凡例",
    )

    return fig


def create_returns_histogram_with_fit(
    returns: np.ndarray,
    x_curve: np.ndarray,
    y_curve: np.ndarray,
    title: str,
    hist_var_return: float | None = None,
    param_var_return: float | None = None,
    nbins: int = 50,
) -> go.Figure:
    """
    リターンのヒストグラムに当てはめた正規分布を重ね、
    VaR の縦線と左尾の塗りつぶしを表示する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=nbins,
            histnorm="probability density",
            name="リターンヒストグラム",
            opacity=0.75,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_curve,
            y=y_curve,
            mode="lines",
            name="当てはめ正規分布",
        )
    )

    if hist_var_return is not None:
        mask_hist = x_curve <= hist_var_return
        x_hist_tail = x_curve[mask_hist]
        y_hist_tail = y_curve[mask_hist]

        if len(x_hist_tail) > 1:
            fig.add_trace(
                go.Scatter(
                    x=np.concatenate(([x_hist_tail[0]], x_hist_tail, [x_hist_tail[-1]])),
                    y=np.concatenate(([0], y_hist_tail, [0])),
                    fill="toself",
                    mode="lines",
                    name="ヒストリカルVaR左尾",
                )
            )

        fig.add_vline(
            x=hist_var_return,
            line_dash="dash",
            annotation_text="ヒストリカルVaR",
            annotation_position="top left",
        )

    if param_var_return is not None:
        fig.add_vline(
            x=param_var_return,
            line_dash="dot",
            annotation_text="パラメトリックVaR",
            annotation_position="top right",
        )

    fig.update_layout(
        title=title,
        xaxis_title="日次リターン",
        yaxis_title="密度",
        template="plotly_white",
        barmode="overlay",
        legend_title="凡例",
    )

    return fig


def create_qq_plot(
    theoretical_quantiles: np.ndarray,
    ordered_values: np.ndarray,
    slope: float,
    intercept: float,
    title: str,
) -> go.Figure:
    """
    QQプロットを作成する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=ordered_values,
            mode="markers",
            name="実データ",
        )
    )

    line_x = np.array([theoretical_quantiles.min(), theoretical_quantiles.max()])
    line_y = slope * line_x + intercept

    fig.add_trace(
        go.Scatter(
            x=line_x,
            y=line_y,
            mode="lines",
            name="基準直線",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="理論分位点",
        yaxis_title="実データ分位点",
        template="plotly_white",
        legend_title="凡例",
    )

    return fig


def create_rolling_volatility_plot(
    rolling_vol: pd.Series,
    title: str,
) -> go.Figure:
    """
    ローリングボラティリティの時系列グラフを作成する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=rolling_vol.index,
            y=rolling_vol.values,
            mode="lines",
            name="ローリングボラティリティ",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="日付",
        yaxis_title="年率換算ボラティリティ",
        template="plotly_white",
        legend_title="凡例",
    )

    return fig


def create_multi_rolling_volatility_plot(
    rolling_vol_df: pd.DataFrame,
    title: str,
) -> go.Figure:
    """
    複数銘柄のローリングボラティリティ比較グラフを作成する。
    """
    fig = go.Figure()

    for column in rolling_vol_df.columns:
        fig.add_trace(
            go.Scatter(
                x=rolling_vol_df.index,
                y=rolling_vol_df[column],
                mode="lines",
                name=column,
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="日付",
        yaxis_title="年率換算ボラティリティ",
        template="plotly_white",
        legend_title="銘柄",
    )

    return fig


def create_correlation_heatmap(
    corr_df: pd.DataFrame,
    title: str,
) -> go.Figure:
    """
    相関行列のヒートマップを作成する。
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.index,
            zmin=-1,
            zmax=1,
            text=np.round(corr_df.values, 3),
            texttemplate="%{text}",
            textfont={"size": 12},
            colorbar={"title": "相関係数"},
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="銘柄",
        yaxis_title="銘柄",
        template="plotly_white",
    )

    return fig


def create_cumulative_return_plot(
    cumulative_returns: pd.Series,
    title: str,
) -> go.Figure:
    """
    単一銘柄の累積リターン時系列グラフを作成する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=cumulative_returns.index,
            y=cumulative_returns.values,
            mode="lines",
            name="累積リターン",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="日付",
        yaxis_title="累積リターン",
        template="plotly_white",
        legend_title="凡例",
    )

    return fig


def create_multi_cumulative_return_plot(
    cumulative_returns_df: pd.DataFrame,
    title: str,
) -> go.Figure:
    """
    複数銘柄の累積リターン比較グラフを作成する。
    """
    fig = go.Figure()

    for column in cumulative_returns_df.columns:
        fig.add_trace(
            go.Scatter(
                x=cumulative_returns_df.index,
                y=cumulative_returns_df[column],
                mode="lines",
                name=column,
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="日付",
        yaxis_title="累積リターン",
        template="plotly_white",
        legend_title="銘柄",
    )

    return fig


# =========================================================
# シミュレーション用
# =========================================================
def create_clt_histogram(
    sample_means: np.ndarray,
    title: str,
    nbins: int = 40,
) -> go.Figure:
    """
    中心極限定理用の標本平均ヒストグラムを作成する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=sample_means,
            nbinsx=nbins,
            histnorm="probability density",
            name="標本平均のヒストグラム",
            opacity=0.8,
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="標本平均",
        yaxis_title="密度",
        template="plotly_white",
        legend_title="凡例",
    )

    return fig


def create_monte_carlo_pi_scatter(
    x: np.ndarray,
    y: np.ndarray,
    inside_mask: np.ndarray,
    title: str,
    max_points_to_plot: int = 3000,
) -> go.Figure:
    """
    モンテカルロ法による円周率推定用の散布図を作成する。
    点が多すぎると重いので、表示点数は制限する。
    """
    if len(x) > max_points_to_plot:
        x = x[:max_points_to_plot]
        y = y[:max_points_to_plot]
        inside_mask = inside_mask[:max_points_to_plot]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x[inside_mask],
            y=y[inside_mask],
            mode="markers",
            name="円の内側",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x[~inside_mask],
            y=y[~inside_mask],
            mode="markers",
            name="円の外側",
        )
    )

    theta = np.linspace(0, 2 * np.pi, 400)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)

    fig.add_trace(
        go.Scatter(
            x=circle_x,
            y=circle_y,
            mode="lines",
            name="単位円",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="y",
        template="plotly_white",
        legend_title="凡例",
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
    )

    return fig
