import streamlit as st

from stats_utils import generate_x_range, normal_pdf, interval_probability, z_score
from plots import create_normal_distribution_figure


# Streamlit ページ設定
st.set_page_config(
    page_title="Normal Distribution for Finance",
    page_icon="📈",
    layout="wide",
)

# アプリタイトル
st.title("📈 Normal Distribution Visualizer for Finance")
st.write(
    """
    このアプリは、正規分布の形状をインタラクティブに可視化する MVP です。
    平均 μ と標準偏差 σ を変更しながら、確率密度関数 (PDF) と区間確率を確認できます。

    金融工学・統計・リスク管理の基礎理解を目的としています。
    """
)

# サイドバー: パラメータ設定
st.sidebar.header("Parameters")

mu = st.sidebar.slider(
    label="Mean (μ)",
    min_value=-10.0,
    max_value=10.0,
    value=0.0,
    step=0.1,
)

sigma = st.sidebar.slider(
    label="Standard Deviation (σ)",
    min_value=0.1,
    max_value=10.0,
    value=1.0,
    step=0.1,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Probability Interval")

lower = st.sidebar.number_input(
    label="Lower Bound",
    value=-1.0,
    step=0.1,
)

upper = st.sidebar.number_input(
    label="Upper Bound",
    value=1.0,
    step=0.1,
)

# lower > upper のときは入れ替える
if lower > upper:
    lower, upper = upper, lower

# データ生成
x = generate_x_range(mu=mu, sigma=sigma)
y = normal_pdf(x=x, mu=mu, sigma=sigma)

# 区間確率を計算
prob = interval_probability(lower=lower, upper=upper, mu=mu, sigma=sigma)

# グラフ作成
fig = create_normal_distribution_figure(
    x=x,
    y=y,
    mu=mu,
    sigma=sigma,
    lower=lower,
    upper=upper,
)

# レイアウト
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Summary")
    st.write(f"**Mean (μ):** {mu:.2f}")
    st.write(f"**Standard Deviation (σ):** {sigma:.2f}")
    st.write(f"**Interval:** [{lower:.2f}, {upper:.2f}]")
    st.write(f"**Probability:** {prob:.6f}")

    # 区間の両端について z-score を表示
    z_lower = z_score(lower, mu, sigma)
    z_upper = z_score(upper, mu, sigma)

    st.write(f"**z-score(lower):** {z_lower:.4f}")
    st.write(f"**z-score(upper):** {z_upper:.4f}")

    st.markdown("---")
    st.subheader("Interpretation")
    st.write(
        """
        - μ が変わると、分布全体が左右に移動します。
        - σ が大きいほど、分布は横に広がります。
        - 区間確率は、指定した範囲に値が入る確率を表します。
        """
    )

st.markdown("---")
st.subheader("Why This Matters in Finance")
st.write(
    """
    正規分布は、金融データ分析やリスク管理の初歩で頻繁に登場します。
    実際の金融リターンは完全には正規分布に従わないことも多いですが、
    まずは基礎として平均・分散・z-score・区間確率を理解することが重要です。
    """
)
