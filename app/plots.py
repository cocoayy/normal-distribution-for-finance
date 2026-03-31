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

    Parameters
    ----------
    x : np.ndarray
        x-axis values / x 軸データ
    y : np.ndarray
        y-axis values (PDF or CDF) / PDF または CDF の値
    mu : float
        Mean / 平均
    sigma : float
        Standard deviation / 標準偏差
    lower : float
        Lower bound / 区間下限
    upper : float
        Upper bound / 区間上限
    mode : str
        "PDF" or "CDF"

    Returns
    -------
    go.Figure
        Plotly Figure object / 描画用 Figure オブジェクト
    """
    fig = go.Figure()

    # Main curve / メイン曲線
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
            # Fill under the PDF curve / PDF の下側を塗りつぶす
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
            # Highlight the CDF segment / CDF の該当区間を強調
            fig.add_trace(
                go.Scatter(
                    x=x_fill,
                    y=y_fill,
                    mode="lines",
                    name="Selected Interval / 指定区間",
                    line=dict(width=4),
                )
            )

    # Mean line / 平均位置の縦線
    fig.add_vline(
        x=mu,
        line_dash="dash",
        annotation_text=f"μ = {mu:.2f}",
        annotation_position="top",
    )

    # Lower and upper bounds / 区間境界
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

    # Annotation / 注釈
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
