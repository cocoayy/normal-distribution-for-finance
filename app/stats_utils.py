import numpy as np
import pandas as pd
from scipy.stats import norm, skew, kurtosis
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
    """
    rng = np.random.default_rng(random_seed)
    return rng.normal(loc=mu, scale=sigma, size=sample_size)


def fetch_return_series(ticker: str, period: str = "1y") -> pd.Series:
    """
    Fetch historical close prices using yfinance and convert them to daily returns.
    yfinance で終値を取得し、日次リターンに変換する。
    """
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    if "Close" not in data.columns:
        raise ValueError("Close price column was not found in downloaded data.")

    close_prices = data["Close"]

    # yfinance の返却形式差異に対応
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
    """
    alpha = 1.0 - confidence_level
    var_return = float(returns.quantile(alpha))
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
    """
    alpha = 1.0 - confidence_level
    var_return = float(norm.ppf(alpha, loc=mu, scale=sigma))
    var_amount = -var_return * investment_amount
    return var_return, var_amount


def calculate_distribution_shape_metrics(data: np.ndarray | pd.Series) -> tuple[float, float]:
    """
    Calculate skewness and excess kurtosis.
    歪度と超過尖度を計算する。
    """
    array = np.asarray(data, dtype=float)
    skewness = float(skew(array, bias=False))
    excess_kurt = float(kurtosis(array, fisher=True, bias=False))
    return skewness, excess_kurt


def interpret_shape_metrics(skewness: float, excess_kurt: float) -> str:
    """
    Provide a simple textual interpretation of skewness and kurtosis.
    歪度・尖度の簡易解釈を返す。
    """
    if skewness > 0.5:
        skew_part = "right-skewed / 右に歪んだ分布"
    elif skewness < -0.5:
        skew_part = "left-skewed / 左に歪んだ分布"
    else:
        skew_part = "roughly symmetric / おおむね対称"

    if excess_kurt > 1.0:
        kurt_part = "fat-tailed / 裾が厚い"
    elif excess_kurt < -0.5:
        kurt_part = "light-tailed / 裾が比較的薄い"
    else:
        kurt_part = "near-normal tail thickness / 正規分布に近い裾の厚さ"

    return f"{skew_part}, {kurt_part}"
