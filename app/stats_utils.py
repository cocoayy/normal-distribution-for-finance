import numpy as np
from scipy.stats import norm


def generate_x_range(mu: float, sigma: float, num_points: int = 1000) -> np.ndarray:
    """
    Generate x-axis values for plotting a normal distribution.
    正規分布を描画するための x 軸配列を生成する。

    Parameters
    ----------
    mu : float
        Mean / 平均
    sigma : float
        Standard deviation / 標準偏差
    num_points : int
        Number of x-axis points / x 軸上の点の数

    Returns
    -------
    np.ndarray
        x-axis array for plotting / 描画用の x 配列
    """
    x_min = mu - 4 * sigma
    x_max = mu + 4 * sigma
    return np.linspace(x_min, x_max, num_points)


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    Compute the probability density function (PDF) of a normal distribution.
    正規分布の確率密度関数 (PDF) を計算する。
    """
    return norm.pdf(x, loc=mu, scale=sigma)


def normal_cdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    Compute the cumulative distribution function (CDF) of a normal distribution.
    正規分布の累積分布関数 (CDF) を計算する。
    """
    return norm.cdf(x, loc=mu, scale=sigma)


def interval_probability(lower: float, upper: float, mu: float, sigma: float) -> float:
    """
    Compute the probability that X falls in [lower, upper].
    正規分布における区間 [lower, upper] の確率を計算する。
    """
    return norm.cdf(upper, loc=mu, scale=sigma) - norm.cdf(lower, loc=mu, scale=sigma)


def z_score(x: float, mu: float, sigma: float) -> float:
    """
    Compute the z-score of x.
    値 x の z-score を計算する。
    """
    return (x - mu) / sigma
