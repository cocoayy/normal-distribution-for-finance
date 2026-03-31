import numpy as np
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

    # ヒストリカル VaR より左側の理論分布を塗る
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

    # パラメトリック VaR の縦線
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
