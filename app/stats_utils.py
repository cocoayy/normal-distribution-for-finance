import numpy as np
from scipy.stats import norm


def generate_x_range(mu: float, sigma: float, num_points: int = 1000) -> np.ndarray:
    """
    正規分布を描画するための x 軸配列を生成する関数。

    Parameters
    ----------
    mu : float
        平均
    sigma : float
        標準偏差
    num_points : int
        x 軸上の点の数

    Returns
    -------
    np.ndarray
        描画用の x 配列

    Notes
    -----
    平均の前後 4σ を取ることで、分布の形が十分見える範囲を確保している。
    """
    x_min = mu - 4 * sigma
    x_max = mu + 4 * sigma
    return np.linspace(x_min, x_max, num_points)


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    正規分布の確率密度関数 (PDF) を計算する。

    Parameters
    ----------
    x : np.ndarray
        x 軸の値
    mu : float
        平均
    sigma : float
        標準偏差

    Returns
    -------
    np.ndarray
        各 x に対応する確率密度
    """
    return norm.pdf(x, loc=mu, scale=sigma)


def interval_probability(lower: float, upper: float, mu: float, sigma: float) -> float:
    """
    正規分布における区間 [lower, upper] の確率を計算する。

    Parameters
    ----------
    lower : float
        区間下限
    upper : float
        区間上限
    mu : float
        平均
    sigma : float
        標準偏差

    Returns
    -------
    float
        区間確率
    """
    return norm.cdf(upper, loc=mu, scale=sigma) - norm.cdf(lower, loc=mu, scale=sigma)


def z_score(x: float, mu: float, sigma: float) -> float:
    """
    値 x の z-score を計算する。

    z = (x - mu) / sigma

    Parameters
    ----------
    x : float
        観測値
    mu : float
        平均
    sigma : float
        標準偏差

    Returns
    -------
    float
        z-score
    """
    return (x - mu) / sigma
