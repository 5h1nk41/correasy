import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from dateutil.parser import parse

def load_data(file):
    try:
        df = pd.read_csv(file)

        # 日付が含まれるカラム名を特定
        date_column = None
        for col in df.columns:
            if "date" in col.lower() or "updated_at" in col.lower():
                date_column = col
                break

        if date_column:
            df[date_column] = pd.to_datetime(df[date_column], format="%Y年%m月", errors='coerce')

        return df, date_column
    except:
        return None, None


def plot_scatter(filtered_df, x_axis, y_axis):
    fig, ax = plt.subplots()
    sns.regplot(  # regplotを使用して回帰直線を描画
        data=filtered_df,
        x=x_axis,
        y=y_axis,
        ax=ax,
        scatter_kws={"s": 50, "alpha": 0.7},  # 点のサイズと透明度を調整
        line_kws={"color": "blue", "alpha": 0.7},  # 回帰直線の色と透明度を調整
    )
    ax.set_xlabel(x_axis, fontsize=12)
    ax.set_ylabel(y_axis, fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.5)  # グリッド線を追加
    return fig


def analyze_correlation(correlation_coefficient):
    if correlation_coefficient > 0.9:
        return "非常に強い正の相関があります"
    elif correlation_coefficient > 0.7:
        return "強い正の相関があります"
    elif correlation_coefficient > 0.4:
        return "やや強い正の相関があります"
    elif correlation_coefficient > 0.2:
        return "弱い正の相関があります"
    elif correlation_coefficient > -0.2:
        return "相関がほとんどありません"
    elif correlation_coefficient > -0.4:
        return "弱い負の相関があります"
    elif correlation_coefficient > -0.7:
        return "やや強い負の相関があります"
    elif correlation_coefficient > -0.9:
        return "強い負の相関があります"
    else:
        return "非常に強い負の相関があります"

def main():
    st.title("CorrEasy")

    # CSVファイルのアップロード
    st.subheader("CSVファイルをアップロード")
    file = st.file_uploader("ファイルを選択", type="csv")

    if file:
        df, date_column = load_data(file)

        if df is None:
            st.warning("データの読み込みに失敗しました。日付形式を確認してください。")
            return

        # 期間の選択
        if date_column:
            min_date = df[date_column].min().date()
            max_date = df[date_column].max().date()
            date_range = st.slider("期間を選択", min_date, max_date, (min_date, max_date))

            # 選択された期間のデータフィルタ
            filtered_df = df[(df[date_column].dt.date >= date_range[0]) & (df[date_column].dt.date <= date_range[1])]
        else:
            filtered_df = df

        # 相関分析
        st.subheader("データセットの設定")

        available_columns = [col for col in df.columns if col != date_column]
        x_axis = st.selectbox("X軸データセットを選択", available_columns)
        y_axis = st.selectbox("Y軸データセットを選択", available_columns)

        # 散布図の描写
        st.subheader("散布図")

        fig = plot_scatter(filtered_df, x_axis, y_axis)
        st.pyplot(fig)

        # 相関係数の計算
        st.subheader("相関係数")

        correlation_coefficient = filtered_df[x_axis].corr(filtered_df[y_axis])
        st.write(f"{correlation_coefficient:.2f}")

        # 分析結果の表示
        st.subheader("分析結果")

        result = analyze_correlation(correlation_coefficient)
        st.write(result)

if __name__ == "__main__":
    main()
