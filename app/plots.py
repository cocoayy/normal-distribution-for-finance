import plotly.graph_objects as go
import numpy as np


def create_normal_distribution_figure(
    x: np.ndarray,
    y: np.ndarray,
    mu: float,
    sigma: float,
    lower: float,
    upper: float,
) -> go.Figure:
    """
    正規分布の曲線と、指定区間の塗りつぶしを含む Plotly グラフを作成する。

    Parameters
    ----------
    x : np.ndarray
        x 軸データ
    y : np.ndarray
        PDF の値
    mu : float
        平均
    sigma : float
        標準偏差
    lower : float
        区間下限
    upper : float
        区間上限

    Returns
    -------
    go.Figure
        描画用 Figure オブジェクト
    """

    # メインの分布曲線
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="Normal PDF",
        )
    )

    # 指定区間だけを切り出して塗りつぶし用データを作る
    mask = (x >= lower) & (x <= upper)
    x_fill = x[mask]
    y_fill = y[mask]

    # 区間部分を塗りつぶす
    fig.add_trace(
        go.Scatter(
            x=np.concatenate(([x_fill[0]], x_fill, [x_fill[-1]])),
            y=np.concatenate(([0], y_fill, [0])),
            fill="toself",
            name="Selected Interval",
            mode="lines",
        )
    )

    # 平均位置を縦線で表示
    fig.add_vline(
        x=mu,
        line_dash="dash",
        annotation_text=f"μ = {mu:.2f}",
        annotation_position="top"
    )

    # レイアウト設定
    fig.update_layout(
        title="Normal Distribution (PDF)",
        xaxis_title="x",
        yaxis_title="Density",
        template="plotly_white",
        legend_title="Legend",
    )

    # 補足情報を注釈で追加
    fig.add_annotation(
        x=0.98,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"μ = {mu:.2f}<br>σ = {sigma:.2f}",
        showarrow=False,
        align="right",
        borderpad=6,
    )

    return fig
