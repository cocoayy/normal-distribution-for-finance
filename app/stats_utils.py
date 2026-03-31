import numpy as np
import pandas as pd
from scipy.stats import norm, skew, kurtosis, probplot
import yfinance as yf


def generate_x_range(mu: float, sigma: float, num_points: int = 1000) -> np.ndarray:
    """
    正規分布を描画するための x 軸配列を生成する。
    """
    x_min = mu - 4 * sigma
    x_max = mu + 4 * sigma
    return np.linspace(x_min, x_max, num_points)


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    正規分布の確率密度関数 (PDF) を計算する。
    """
    return norm.pdf(x, loc=mu, scale=sigma)


def normal_cdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """
    正規分布の累積分布関数 (CDF) を計算する。
    """
    return norm.cdf(x, loc=mu, scale=sigma)


def interval_probability(lower: float, upper: float, mu: float, sigma: float) -> float:
    """
    区間 [lower, upper] に入る確率を計算する。
    """
    return norm.cdf(upper, loc=mu, scale=sigma) - norm.cdf(lower, loc=mu, scale=sigma)


def z_score(x: float, mu: float, sigma: float) -> float:
    """
    z-score を計算する。
    """
    return (x - mu) / sigma


def generate_samples(mu: float, sigma: float, sample_size: int, random_seed: int) -> np.ndarray:
    """
    正規分布から乱数サンプルを生成する。
    """
    rng = np.random.default_rng(random_seed)
    return rng.normal(loc=mu, scale=sigma, size=sample_size)


def fetch_return_series(ticker: str, period: str = "1y") -> pd.Series:
    """
    yfinance で終値を取得し、日次リターンに変換する。
    """
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"データが取得できませんでした: {ticker}")

    if "Close" not in data.columns:
        raise ValueError("Close 列が見つかりませんでした。")

    close_prices = data["Close"]

    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]

    returns = close_prices.pct_change().dropna()

    if returns.empty:
        raise ValueError("リターン系列が空です。")

    return returns


def fit_normal_to_returns(returns: pd.Series) -> tuple[float, float]:
    """
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
    ヒストリカル VaR を計算する。
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
    正規分布仮定のパラメトリック VaR を計算する。
    """
    alpha = 1.0 - confidence_level
    var_return = float(norm.ppf(alpha, loc=mu, scale=sigma))
    var_amount = -var_return * investment_amount
    return var_return, var_amount


def calculate_distribution_shape_metrics(data: np.ndarray | pd.Series) -> tuple[float, float]:
    """
    歪度と超過尖度を計算する。
    """
    array = np.asarray(data, dtype=float)
    skewness = float(skew(array, bias=False))
    excess_kurt = float(kurtosis(array, fisher=True, bias=False))
    return skewness, excess_kurt


def interpret_shape_metrics(skewness: float, excess_kurt: float) -> str:
    """
    歪度・尖度の簡易解釈を返す。
    """
    if skewness > 0.5:
        skew_part = "右に歪んだ分布"
    elif skewness < -0.5:
        skew_part = "左に歪んだ分布"
    else:
        skew_part = "おおむね対称"

    if excess_kurt > 1.0:
        kurt_part = "裾が厚い"
    elif excess_kurt < -0.5:
        kurt_part = "裾が比較的薄い"
    else:
        kurt_part = "裾の厚さは正規分布に比較的近い"

    return f"{skew_part}、{kurt_part}"


def calculate_qq_plot_data(data: np.ndarray | pd.Series) -> tuple[np.ndarray, np.ndarray, float, float]:
    """
    QQプロット用データを生成する。

    Returns
    -------
    theoretical_quantiles : np.ndarray
        理論正規分布の分位点
    ordered_values : np.ndarray
        実データの並べ替え済み値
    slope : float
        参照直線の傾き
    intercept : float
        参照直線の切片
    """
    array = np.asarray(data, dtype=float)
    (theoretical_quantiles, ordered_values), (slope, intercept, _) = probplot(array, dist="norm")
    return theoretical_quantiles, ordered_values, float(slope), float(intercept)
