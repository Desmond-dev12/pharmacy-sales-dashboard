import os
import pandas as pd
import plotly.express as px
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Universal Data Cleaner", layout="wide")

st.title("💿Universal Data Cleaner")
st.write("Convert your files between CSV and Excel formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}. Please upload a CSV or Excel file.")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        st.write("**Preview the head of the Dataframe**")
        st.dataframe(df.head())

        st.subheader(f"📋 Summary Report for {file.name}")

        report_cols = st.columns(4)
        report_cols[0].metric("Rows", len(df))
        report_cols[1].metric("Columns", len(df.columns))
        report_cols[2].metric("Missing Values", int(df.isna().sum().sum()))
        report_cols[3].metric("Duplicates", int(df.duplicated().sum()))

        sales_aliases = ["total_sales", "sales", "revenue", "total_revenue", "amount", "gross_sales", "total_amount"]
        quantity_aliases = ["quantity", "qty", "total_quantity", "units", "items", "total_units"]
        transactions_aliases = ["transactions", "total_transactions", "order_count", "num_orders", "orders"]

        def find_column_name(columns, aliases):
            normalized = {str(col).strip().lower().replace(" ", "_"): col for col in columns}
            for alias in aliases:
                if alias in normalized:
                    return normalized[alias]
            return None
        
# find the actual column names based on aliases
        sales_col = find_column_name(df.columns, sales_aliases)
        quantity_col = find_column_name(df.columns, quantity_aliases)
        transactions_col = find_column_name(df.columns, transactions_aliases)

        kpi_cols = st.columns(4)
        metric_count = 0

        if sales_col is not None:
            total_sales = pd.to_numeric(df[sales_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Sales", f"${total_sales:,.2f}")
            metric_count += 1

        if quantity_col is not None:
            total_quantity = pd.to_numeric(df[quantity_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Quantity", f"{total_quantity:,.0f}")
            metric_count += 1

        if transactions_col is not None:
            total_transactions = pd.to_numeric(df[transactions_col], errors="coerce").sum()
            kpi_cols[metric_count].metric("Total Transactions", f"{total_transactions:,.0f}")
            metric_count += 1

        if sales_col is not None and transactions_col is not None:
            total_sales = pd.to_numeric(df[sales_col], errors="coerce").sum()
            total_transactions = pd.to_numeric(df[transactions_col], errors="coerce").sum()
            aov = total_sales / total_transactions if total_transactions else 0
            kpi_cols[metric_count].metric("AOV", f"${aov:,.2f}")
            metric_count += 1

        if metric_count == 0:
            st.info("No sales or transaction KPI columns were found in this dataset.")

        st.subheader(f"🧹 Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate from {file.name}"):
                    df = df.drop_duplicates()
                    st.success("Duplicates removed successfully")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
                    if len(numeric_cols):
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("Missing values have been filled!")
                    else:
                        st.warning("No numeric columns were found to fill.")

        st.subheader("Select Columns to convert")
        columns = st.multiselect(
            f"Choose columns for {file.name}",
            df.columns,
            default=df.columns,
            key=f"columns_{file.name}",
        )
        df = df[columns]

        st.subheader("📊Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}", key=f"visualize_{file.name}"):
            numeric_columns = df.select_dtypes(include="number").columns.tolist()
            all_columns = df.columns.tolist()

            if not all_columns:
                st.warning("Select at least one column to visualize.")
            elif not numeric_columns:
                st.info("Visualization requires at least one numeric column.")
            else:
                chart_type = st.selectbox(
                    "Chart type",
                    ["Bar", "Line", "Scatter", "Histogram"],
                    key=f"chart_type_{file.name}",
                )

                if chart_type == "Histogram":
                    histogram_column = st.selectbox(
                        "Column",
                        numeric_columns,
                        key=f"histogram_column_{file.name}",
                    )
                    chart = px.histogram(df, x=histogram_column, title=f"Distribution of {histogram_column}")
                elif chart_type == "Scatter":
                    if len(numeric_columns) < 2:
                        st.info("Scatter plots require at least two numeric columns.")
                        chart = None
                    else:
                        x_column, y_column = st.columns(2)
                        with x_column:
                            x_axis = st.selectbox("X-axis", numeric_columns, key=f"scatter_x_{file.name}")
                        with y_column:
                            y_axis = st.selectbox("Y-axis", numeric_columns, index=1, key=f"scatter_y_{file.name}")
                        chart = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                else:
                    x_axis, y_axis = st.columns(2)
                    with x_axis:
                        x_column = st.selectbox("X-axis", all_columns, key=f"{chart_type}_x_{file.name}")
                    with y_axis:
                        y_column = st.selectbox("Y-axis", numeric_columns, key=f"{chart_type}_y_{file.name}")
                    chart = px.bar(df, x=x_column, y=y_column, title=f"{y_column} by {x_column}") if chart_type == "Bar" else px.line(df, x=x_column, y=y_column, title=f"{y_column} by {x_column}")

                if chart is not None:
                    st.plotly_chart(chart, use_container_width=True)

                st.write("**Summary Statistics**")
                st.dataframe(df[numeric_columns].describe())

        st.subheader("Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=f"conversion_type_{file.name}"
        )

        if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                output_name = os.path.splitext(file.name)[0] + ".csv"
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                output_name = os.path.splitext(file.name)[0] + ".xlsx"
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=output_name,
                 mime=mime_type,
                  key=f"download_{file.name}",
            )

