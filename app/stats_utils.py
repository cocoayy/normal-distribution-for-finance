import numpy as np
import pandas as pd
from scipy.stats import norm
import yfinance as yf


def generate_x_range(mu: float, sigma: float, num_points: int = 1000) -> np.ndarray:
    """
    Generate x-axis values for plotting a normal distribution.
    正規分布を描画するための x 軸配列を生成する。
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


def generate_samples(mu: float, sigma: float, sample_size: int, random_seed: int) -> np.ndarray:
    """
    Generate random samples from a normal distribution.
    正規分布から乱数サンプルを生成する。

    Parameters
    ----------
    mu : float
        Mean / 平均
    sigma : float
        Standard deviation / 標準偏差
    sample_size : int
        Number of generated samples / サンプル数
    random_seed : int
        Random seed for reproducibility / 再現性確保のための乱数シード

    Returns
    -------
    np.ndarray
        Generated samples / 生成されたサンプル
    """
    rng = np.random.default_rng(random_seed)
    return rng.normal(loc=mu, scale=sigma, size=sample_size)


def compute_histogram_density_range(samples: np.ndarray) -> tuple[float, float]:
    """
    Compute a reasonable x-axis range from sample data.
    サンプルデータからヒストグラム表示用の x 軸範囲を計算する。
    """
    sample_min = float(np.min(samples))
    sample_max = float(np.max(samples))
    return sample_min, sample_max


def fetch_return_series(ticker: str, period: str = "1y") -> pd.Series:
    """
    Fetch historical close prices using yfinance and convert them to daily returns.
    yfinance で終値を取得し、日次リターンに変換する。

    Parameters
    ----------
    ticker : str
        Stock ticker symbol / 銘柄コード
    period : str
        Data period supported by yfinance / 取得期間

    Returns
    -------
    pd.Series
        Daily return series / 日次リターン系列

    Notes
    -----
    Returns are computed using percentage change:
        r_t = (P_t / P_{t-1}) - 1
    """
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    # yfinance の返却形状に備えて Close 列を安全に取得する
    if "Close" not in data.columns:
        raise ValueError("Close price column was not found in downloaded data.")

    close_prices = data["Close"]

    # Series の場合と DataFrame の場合の両方に対応
    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]

    returns = close_prices.pct_change().dropna()

    if returns.empty:
        raise ValueError("Return series is empty after pct_change().")

    return returns


def fit_normal_to_returns(returns: pd.Series) -> tuple[float, float]:
    """
    Estimate mean and standard deviation from return data.
    リターンデータから平均と標準偏差を推定する。
    """
    mu = float(returns.mean())
    sigma = float(returns.std(ddof=1))
    return mu, sigma


def calculate_var_from_returns(
    returns: pd.Series,
    confidence_level: float,
    investment_amount: float,
) -> tuple[float, float]:
    """
    Calculate a simple historical VaR based on return quantiles.
    リターンの分位点を使って簡易的なヒストリカル VaR を計算する。

    Parameters
    ----------
    returns : pd.Series
        Daily return series / 日次リターン
    confidence_level : float
        Confidence level, e.g. 0.95 or 0.99 / 信頼水準
    investment_amount : float
        Portfolio or position amount / 投資額

    Returns
    -------
    tuple[float, float]
        var_return : float
            VaR expressed as return / リターンベースの VaR
        var_amount : float
            VaR expressed as amount / 金額ベースの VaR
    """
    alpha = 1.0 - confidence_level
    var_return = float(returns.quantile(alpha))

    # 損失額として正の値で見せたいので符号を反転している
    var_amount = -var_return * investment_amount

    return var_return, var_amount


def calculate_parametric_var(
    mu: float,
    sigma: float,
    confidence_level: float,
    investment_amount: float,
) -> tuple[float, float]:
    """
    Calculate parametric VaR assuming normal distribution.
    正規分布を仮定したパラメトリック VaR を計算する。

    Returns
    -------
    tuple[float, float]
        var_return : float
            VaR return threshold / VaR のリターン閾値
        var_amount : float
            VaR amount in currency / 金額ベースの VaR
    """
    alpha = 1.0 - confidence_level
    var_return = float(norm.ppf(alpha, loc=mu, scale=sigma))
    var_amount = -var_return * investment_amount
    return var_return, var_amount
