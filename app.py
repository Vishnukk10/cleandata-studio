import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CleanData Studio", layout="wide")

st.title(" CleanData Studio")
st.caption("Automated Data Quality Audit, Cleaning & Visualization")

# Sidebar Upload
st.sidebar.header(" File Upload")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Top KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", df.shape[0])
    c2.metric("Total Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())
    c4.metric("Duplicates", df.duplicated().sum())

    tab1, tab2, tab3, tab4 = st.tabs([" Data Overview", " Auto-Cleaner", " Charts", " Outlier Detection"])

    # Tab 1: Raw Data & Stats
    with tab1:
        st.subheader("Raw Data Preview")
        st.dataframe(df.head(), use_container_width=True)
        st.subheader("Summary Statistics")
        st.dataframe(df.describe().round(2), use_container_width=True)

    # Tab 2: Cleaning Logic
    with tab2:
        st.subheader("Clean & Export")
        fill_opt = st.selectbox("Fill missing numbers with:", ["Mean (Average)", "Median", "Zero (0)"])
        
        if st.button("Run Auto-Clean"):
            clean_df = df.drop_duplicates()
            if fill_opt == "Mean (Average)":
                clean_df = clean_df.fillna(clean_df.mean(numeric_only=True))
            elif fill_opt == "Median":
                clean_df = clean_df.fillna(clean_df.median(numeric_only=True))
            else:
                clean_df = clean_df.fillna(0)

            clean_df = clean_df.round(2)
            st.success("Dataset cleaned successfully!")
            st.dataframe(clean_df.head(), use_container_width=True)

            st.download_button(
                label="📥 Download Cleaned CSV",
                data=clean_df.to_csv(index=False),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

    # Tab 3: Charts
    with tab3:
        st.subheader("Interactive Charts")
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if num_cols:
            col_x = st.selectbox("X-Axis", options=df.columns)
            col_y = st.selectbox("Y-Axis", options=num_cols)
            fig = px.bar(df, x=col_x, y=col_y, title=f"{col_y} vs {col_x}")
            st.plotly_chart(fig, use_container_width=True)

    # Tab 4: Simple Outlier Detection
    with tab4:
        st.subheader("Outlier Detection (Extreme Values)")
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if num_cols:
            selected_col = st.selectbox("Select Column to Check", num_cols)
            # Find values higher than 2 standard deviations from mean
            mean = df[selected_col].mean()
            std = df[selected_col].std()
            outliers = df[abs(df[selected_col] - mean) > 2 * std]
            st.write(f"Found **{len(outliers)}** potential outliers in `{selected_col}`:")
            st.dataframe(outliers)
else:
    st.info("Upload a CSV file in the sidebar to get started.")