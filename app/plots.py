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
    Create a Plotly figure for PDF or CDF visualization.
    PDF または CDF の可視化用 Plotly グラフを作成する。
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
                    name="Selected Interval / 指定区間",
                )
            )
        elif mode == "CDF":
            fig.add_trace(
                go.Scatter(
                    x=x_fill,
                    y=y_fill,
                    mode="lines",
                    name="Selected Interval / 指定区間",
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
        annotation_text=f"lower = {lower:.2f}",
        annotation_position="bottom left",
    )
    fig.add_vline(
        x=upper,
        line_dash="dot",
        annotation_text=f"upper = {upper:.2f}",
        annotation_position="bottom right",
    )

    title_map = {
        "PDF": "Normal Distribution PDF / 正規分布の確率密度関数",
        "CDF": "Normal Distribution CDF / 正規分布の累積分布関数",
    }

    yaxis_map = {
        "PDF": "Density / 確率密度",
        "CDF": "Cumulative Probability / 累積確率",
    }

    fig.update_layout(
        title=title_map.get(mode, "Distribution / 分布"),
        xaxis_title="x",
        yaxis_title=yaxis_map.get(mode, "Value / 値"),
        template="plotly_white",
        legend_title="Legend / 凡例",
    )

    fig.add_annotation(
        x=0.98,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"μ = {mu:.2f}<br>σ = {sigma:.2f}<br>Mode = {mode}",
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
    Create a histogram of samples and overlay a theoretical PDF curve.
    サンプルのヒストグラムに理論 PDF 曲線を重ねる。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=samples,
            nbinsx=nbins,
            histnorm="probability density",
            name="Histogram / ヒストグラム",
            opacity=0.75,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_curve,
            y=y_curve,
            mode="lines",
            name="Normal PDF / 正規分布PDF",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Value / 値",
        yaxis_title="Density / 密度",
        template="plotly_white",
        barmode="overlay",
        legend_title="Legend / 凡例",
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
    Create a histogram for return data and overlay the fitted normal PDF.
    Also draw VaR lines when provided.
    金融リターンのヒストグラムに当てはめた正規分布を重ね、
    必要に応じて VaR の縦線も表示する。
    """
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=returns,
            nbinsx=nbins,
            histnorm="probability density",
            name="Returns Histogram / リターンヒストグラム",
            opacity=0.75,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_curve,
            y=y_curve,
            mode="lines",
            name="Fitted Normal PDF / 当てはめ正規分布",
        )
    )

    # ヒストリカル VaR の位置を縦線で描画
    if hist_var_return is not None:
        fig.add_vline(
            x=hist_var_return,
            line=dict(color="red", width=2),
            line_dash="dash",
            annotation_text="Historical VaR / ヒストリカルVaR",
            annotation_position="top left",
        )

    # パラメトリック VaR の位置を縦線で描画
    if param_var_return is not None:
        fig.add_vline(
            x=param_var_return,
            line=dict(color="blue", width=2),
            line_dash="dot",
            annotation_text="Parametric VaR / パラメトリックVaR",
            annotation_position="top right",
        )

    fig.update_layout(
        title=title,
        xaxis_title="Daily Return / 日次リターン",
        yaxis_title="Density / 密度",
        template="plotly_white",
        barmode="overlay",
        legend_title="Legend / 凡例",
    )

    return fig
