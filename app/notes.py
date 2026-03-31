import streamlit as st


def render_notes_tab() -> None:
    """
    Render the notes/documentation tab.
    解説ノート用タブを表示する。
    """
    st.header("Notes / 解説ノート")

    st.write(
        """
        **English:**
        This tab explains what the app does, why it was built, what each formula means,
        and how to interpret the graphs.

        **日本語:**
        このタブでは、このアプリが何をするものか、なぜ作ったのか、
        各数式の意味、グラフの読み方を解説します。
        """
    )

    st.markdown("---")

    st.subheader("1. Purpose of This App / このアプリの目的")
    st.write(
        """
        **English:**
        This app is designed to help users understand the normal distribution and its connection to finance.
        It starts from mathematical basics and extends to sampling, market return comparison, and simple risk metrics.

        **日本語:**
        このアプリは、正規分布と金融とのつながりを理解するために作っています。
        数学の基礎から始めて、サンプル生成、市場リターン比較、簡易リスク指標までつなげています。
        """
    )

    st.subheader("2. Main Functions / 主な機能")
    st.markdown(
        """
        - **PDF / CDF visualization / PDF・CDF 可視化**
          正規分布の形と累積確率を確認できます。

        - **Interval probability / 区間確率**
          ある範囲に値が入る確率を確認できます。

        - **z-score / zスコア**
          値が平均から何標準偏差離れているかを確認できます。

        - **Random sampling / サンプル生成**
          理論分布から乱数を生成し、ヒストグラムで比較できます。

        - **Financial return comparison / 金融リターン比較**
          実データの日次リターン分布と正規分布の違いを確認できます。

        - **Skewness and kurtosis / 歪度・尖度**
          分布の非対称性や裾の厚さを数値で見られます。

        - **VaR / バリュー・アット・リスク**
          一定信頼水準での損失の目安を確認できます。
        """
    )

    st.markdown("---")

    st.subheader("3. Core Formulas / 主な数式")

    st.markdown("### 3.1 Normal Distribution PDF / 正規分布の確率密度関数")
    st.latex(r"f(x) = \frac{1}{\sqrt{2\pi}\sigma}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)")
    st.write(
        """
        **English:**
        This formula gives the density of a normal distribution with mean μ and standard deviation σ.

        **日本語:**
        この式は、平均 μ、標準偏差 σ を持つ正規分布の密度を表します。
        """
    )

    st.markdown("### 3.2 Normal Distribution CDF / 正規分布の累積分布関数")
    st.latex(r"F(x) = P(X \le x)")
    st.write(
        """
        **English:**
        The CDF gives the probability that the random variable X is less than or equal to x.

        **日本語:**
        CDF は、確率変数 X が x 以下になる確率を表します。
        """
    )

    st.markdown("### 3.3 Interval Probability / 区間確率")
    st.latex(r"P(a \le X \le b) = F(b) - F(a)")
    st.write(
        """
        **English:**
        The probability of being inside an interval is computed by subtracting two CDF values.

        **日本語:**
        区間に入る確率は、CDF の差で求めます。
        """
    )

    st.markdown("### 3.4 z-score / zスコア")
    st.latex(r"z = \frac{x - \mu}{\sigma}")
    st.write(
        """
        **English:**
        A z-score tells us how many standard deviations a value is away from the mean.

        **日本語:**
        zスコアは、ある値が平均から何標準偏差離れているかを示します。
        """
    )

    st.markdown("### 3.5 Daily Return / 日次リターン")
    st.latex(r"r_t = \frac{P_t}{P_{t-1}} - 1")
    st.write(
        """
        **English:**
        Daily return measures the relative price change from one day to the next.

        **日本語:**
        日次リターンは、前日から当日への価格変化率を表します。
        """
    )

    st.markdown("### 3.6 Historical VaR / ヒストリカル VaR")
    st.latex(r"\mathrm{VaR}_{\alpha} = \text{quantile of returns at } (1-\alpha)")
    st.write(
        """
        **English:**
        Historical VaR is based on the lower-tail quantile of past return data.

        **日本語:**
        ヒストリカル VaR は、過去のリターン分布の下側分位点を使って求めます。
        """
    )

    st.markdown("### 3.7 Parametric VaR / パラメトリック VaR")
    st.latex(r"\mathrm{VaR}_{\alpha} = \mu + \sigma z_{1-\alpha}")
    st.write(
        """
        **English:**
        Parametric VaR assumes returns follow a normal distribution.

        **日本語:**
        パラメトリック VaR は、リターンが正規分布に従うと仮定して計算します。
        """
    )

    st.markdown("---")

    st.subheader("4. Meaning of the Graphs / グラフの意味")

    st.markdown("### 4.1 PDF Graph / PDFグラフ")
    st.write(
        """
        **English:**
        The PDF graph shows the shape of the normal distribution.
        The center corresponds to the mean, and the width depends on the standard deviation.

        **日本語:**
        PDF グラフは、正規分布の形そのものを表します。
        真ん中が平均で、横方向の広がりが標準偏差に対応します。
        """
    )

    st.markdown("### 4.2 CDF Graph / CDFグラフ")
    st.write(
        """
        **English:**
        The CDF graph accumulates probability from left to right.
        It helps interpret probabilities such as “less than x.”

        **日本語:**
        CDF グラフは、左から右へ確率を積み上げたものです。
        「x 以下の確率」を読むのに向いています。
        """
    )

    st.markdown("### 4.3 Histogram of Samples / サンプルヒストグラム")
    st.write(
        """
        **English:**
        This histogram shows generated random data.
        Comparing it with the theoretical PDF helps connect probability theory and simulation.

        **日本語:**
        このヒストグラムは、生成した乱数データの分布です。
        理論 PDF と比べることで、理論とシミュレーションの関係が見えます。
        """
    )

    st.markdown("### 4.4 Return Histogram / リターンヒストグラム")
    st.write(
        """
        **English:**
        This graph shows actual market return data.
        Comparing it with a fitted normal distribution reveals how real financial data differs from theory.

        **日本語:**
        このグラフは、実際の市場リターンの分布です。
        正規分布を重ねることで、実データが理論からどうズレるかを見られます。
        """
    )

    st.markdown("### 4.5 VaR Vertical Lines / VaR の縦線")
    st.write(
        """
        **English:**
        These lines indicate risk thresholds in the left tail of the return distribution.
        They help visualize where a “bad outcome” region begins.

        **日本語:**
        これらの線は、リターン分布の左尾にあるリスク閾値を示します。
        どこから損失側の危険領域に入るのかを視覚的に示します。
        """
    )

    st.markdown("---")

    st.subheader("5. Meaning of Skewness and Kurtosis / 歪度と尖度の意味")
    st.write(
        """
        **English:**
        - **Skewness** measures asymmetry.
        - **Excess kurtosis** measures how heavy the tails are relative to a normal distribution.

        **日本語:**
        - **歪度** は左右非対称性を表します。
        - **超過尖度** は、正規分布と比べて裾がどれくらい厚いかを表します。
        """
    )

    st.markdown(
        """
        - **Skewness ≈ 0 / 歪度が 0 付近**
          roughly symmetric / おおむね対称

        - **Positive skewness / 正の歪度**
          longer right tail / 右側の裾が長い

        - **Negative skewness / 負の歪度**
          longer left tail / 左側の裾が長い

        - **Excess kurtosis ≈ 0 / 超過尖度が 0 付近**
          similar to normal distribution / 正規分布に近い

        - **Large excess kurtosis / 超過尖度が大きい**
          fat tails / 裾が厚い
        """
    )

    st.markdown("---")

    st.subheader("6. Why This Matters in Finance / なぜ金融で重要か")
    st.write(
        """
        **English:**
        In finance, returns are often introduced using the normal distribution,
        but real data frequently shows skewness, fat tails, and deviations from normality.
        This app helps users see both the usefulness and limitations of normal-distribution-based modeling.

        **日本語:**
        金融では、リターン分布を最初に正規分布で説明することが多いですが、
        実データには歪みや裾の厚さが見られ、正規分布から外れることも多いです。
        このアプリは、正規分布ベースの考え方の有用性と限界の両方を理解する助けになります。
        """
    )

    st.subheader("7. What This App Tries to Achieve / このアプリでやりたいこと")
    st.write(
        """
        **English:**
        This app aims to connect:
        mathematics → probability → simulation → market data → risk interpretation.

        **日本語:**
        このアプリでは、
        数学 → 確率 → シミュレーション → 市場データ → リスク解釈
        までを一つにつなげることを目指しています。
        """
    )
