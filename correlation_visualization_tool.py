import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from dateutil.parser import parse

def load_data(file):
    try:
        df = pd.read_csv(file)

        # Identify column names containing dates
        date_column = df.select_dtypes(include=[np.datetime64]).columns[0] if not df.select_dtypes(include=[np.datetime64]).empty else None

        if date_column:
            df[date_column] = pd.to_datetime(df[date_column], format="%Y年%m月", errors='coerce')

        return df, date_column
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None, None


def plot_scatter(filtered_df, x_axis, y_axis):
    fig, ax = plt.subplots()
    sns.regplot( 
        data=filtered_df,
        x=x_axis,
        y=y_axis,
        ax=ax,
        scatter_kws={"s": 50, "alpha": 0.7},  
        line_kws={"color": "blue", "alpha": 0.7},  
    )
    ax.set_xlabel(x_axis, fontsize=14)
    ax.set_ylabel(y_axis, fontsize=14)
    ax.grid(True, linestyle="--", alpha=0.5)
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
    
def is_outlier(s):
    lower_limit = s.quantile(0.25) - 1.5 * (s.quantile(0.75) - s.quantile(0.25))
    upper_limit = s.quantile(0.75) + 1.5 * (s.quantile(0.75) - s.quantile(0.25))
    return ~s.between(lower_limit, upper_limit)

def highlight_outliers(val, is_outlier_col):
    if is_outlier_col:
        if val:
            return 'background-color: yellow'
    return ''

def main():
    st.title("CorrEasy")

    # Upload CSV file.
    st.subheader("Upload CSV file")
    file = st.file_uploader("Select file", type="csv")

    filtered_df = None

    if file:
        df, date_column = load_data(file)

        if df is None:
            st.warning("Failed to load data. Check date format.")
            return
        else:
            filtered_df = df
        
    if filtered_df is not None:

        # Display table
        st.subheader("Data-set")

        styled_df = filtered_df.copy()
        numeric_columns = styled_df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            styled_df[f'{col}_is_outlier'] = is_outlier(styled_df[col])


        def style_func(val, is_outlier):
            if is_outlier:
                return highlight_outliers(val, True)
            else:
                return highlight_outliers(val, False)

        for col in numeric_columns:
            styled_df.style.applymap(
                lambda val: style_func(val, styled_df[f"{col}_is_outlier"]),
                subset=col,
            )

        # Remove is_outlier columns
        styled_df = styled_df[numeric_columns]
        
        st.table(styled_df)

        # Choice of period
        if date_column:
            min_date = df[date_column].min().date()
            max_date = df[date_column].max().date()
            date_range = st.slider("Select a period of time", min_date, max_date, (min_date, max_date))

            # 選択された期間のデータフィルタ
            filtered_df = df[(df[date_column].dt.date >= date_range[0]) & (df[date_column].dt.date <= date_range[1])]
        else:
            filtered_df = df

        # correlation analysis
        st.subheader("Data set configuration")

        available_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if date_column in available_columns:
            available_columns.remove(date_column)

        x_axis = st.selectbox("Select X-axis data set", available_columns, index=0)
        y_axis = st.selectbox("Select Y-axis data set", available_columns, index=1 if len(available_columns) > 1 else 0)

        # Scatterplot depiction
        st.subheader("scatter diagram")

        fig = plot_scatter(filtered_df, x_axis, y_axis)
        st.pyplot(fig)

        # Calculation of correlation coefficients
        st.subheader("correlation coefficient")

        correlation_coefficient = filtered_df[x_axis].corr(filtered_df[y_axis])
        st.write(f"{correlation_coefficient:.2f}")

        # Display of analysis results
        st.subheader("Analysis Results")

        result = analyze_correlation(correlation_coefficient)
        st.write(result)

if __name__ == "__main__":
    main()
