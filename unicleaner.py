import os
import seaborn as sns
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Universal Data Cleaner & Visualizer", layout="wide")
st.title("📊 Manager Analytics & Data Cleaning Suite")
st.write("Upload raw CSV or Excel files to automatically clean, filter, and visualize your business data.")

uploaded_file = st.file_uploader("Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error(f"Unsupported file type: {file_ext}. Please upload a CSV or Excel file.")
        st.stop()

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("1. Data Cleaning Options")
    date_cols = df.columns.tolist()
    selected_date_col = st.sidebar.selectbox(
        "Select Date Column to Convert (pd.to_datetime)",
        ["None"] + date_cols,
    )

    if selected_date_col != "None":
        try:
            df[selected_date_col] = pd.to_datetime(df[selected_date_col])
            st.sidebar.success(f"Converted '{selected_date_col}' to Datetime!")
        except Exception as e:
            st.sidebar.error(f"Error converting column: {e}")

    null_handling = st.sidebar.radio(
        "Handle Missing Values:",
        ["Keep as is", "Drop Rows with Missing Values", "Fill Missing Values with 0"],
    )
    if null_handling == "Drop Rows with Missing Values":
        df = df.dropna()
    elif null_handling == "Fill Missing Values with 0":
        df = df.fillna(0)

    st.sidebar.header("2. Filter Data")
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if categorical_cols:
        filter_col = st.sidebar.selectbox("Filter by Category Column:", ["None"] + categorical_cols)
        if filter_col != "None":
            unique_vals = df[filter_col].dropna().unique().tolist()
            selected_vals = st.sidebar.multiselect(
                f"Select values for {filter_col}:",
                unique_vals,
                default=unique_vals,
            )
            df = df[df[filter_col].isin(selected_vals)]

    st.subheader("Processed Data Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    st.dataframe(df)

    st.subheader("📈 Visualizations")
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if numeric_cols:
        x_axis = st.selectbox("Select X-axis:", df.columns.tolist())
        y_axis = st.selectbox("Select Y-axis (Numeric):", numeric_cols)
        chart_type = st.selectbox("Chart Type:", ["Bar Chart", "Line Chart", "Scatter Plot"])

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 4))
        if chart_type == "Bar Chart":
            df.groupby(x_axis)[y_axis].sum().plot(kind="bar", ax=ax)
        elif chart_type == "Line Chart":
            df.groupby(x_axis)[y_axis].sum().plot(kind="line", ax=ax, marker="o")
        elif chart_type == "Scatter Plot":
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)

        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.subheader("💾 Download Cleaned Dataset")
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_business_data.csv",
        mime="text/csv",
    )
else:
    st.info("Please upload a CSV or Excel file to get started.")
