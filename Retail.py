# Libraries
import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Sales Analysis Dashboard")
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, encoding= "latin1")
    data = data.rename(columns={"Store": "Branch"})
    data["Date"] = pd.to_datetime(data["Date"])
    data["Date"] = pd.to_datetime(data["Date"], format="mixed")

    return data
data_folder = r"C:\Users\DELL\Desktop\UCC CODE PROJECTS"
file_path = os.path.join(data_folder, "retail_store_clean1.csv")
data = load_data(file_path)

# sidebars 
st.sidebar.header("Filters")
selected_branch = st.sidebar.multiselect("Select_Branch", options=data["Branch"].unique(), default=data["Branch"].unique())
selected_category = st.sidebar.multiselect("Select_Category", options=data["Category"].unique(), default=data["Category"].unique())
selected_customer = st.sidebar.multiselect("Select_Customer_Type", options=data["Customer Type"].unique(), default=data["Customer Type"].unique())
selected_gender = st.sidebar.multiselect("Select_Gender", options=data["Gender"].unique(), default=data["Gender"].unique())
min_date = data["Date"].min()
max_date = data["Date"].max()
selected_date = st.sidebar.date_input("Select_Date_Range", value=(min_date, max_date),
                                      min_value=min_date, max_value=max_date)

if not selected_date or len(selected_date) != 2:
    st.write("Kindly Select a valid date")
    st.stop()
                                      
# filters 

branch_filter = data["Branch"].isin(selected_branch)
category_filter = data["Category"].isin(selected_category)
customer_filter = data["Customer Type"].isin(selected_customer)
gender_filter = data["Gender"].isin(selected_gender)
data["Date"] = pd.to_datetime(data["Date"])
start_date = pd.to_datetime(selected_date[0])
end_date = pd.to_datetime(selected_date[1])
date_filter = (data["Date"] >= start_date) & (data["Date"] <= end_date)
filtered_data = data[branch_filter & category_filter & customer_filter & gender_filter &
                     date_filter]
if filtered_data.empty:
    st.warning("No data found for the filters")
    st.stop()
  
# Prepare filtered data for analysis
filtered_data = filtered_data.copy()
filtered_data["Unit Price"] = pd.to_numeric(filtered_data["Unit Price"], errors="coerce")
filtered_data["Total"] = pd.to_numeric(filtered_data["Total"], errors="coerce")
filtered_data["Quantity"] = pd.to_numeric(filtered_data["Quantity"], errors="coerce")
filtered_data["Rating"] = pd.to_numeric(filtered_data["Rating"], errors="coerce")
filtered_data = filtered_data.dropna(subset=["Total", "Quantity", "Unit Price", "Rating", "Transaction ID"]).copy()

# Key Performance indicators

total_sales = filtered_data["Total"].sum()
total_quantity = filtered_data["Quantity"].sum()
avg_unit_price = filtered_data["Unit Price"].mean()
avg_cus_rating = filtered_data["Rating"].mean()
total_transac = filtered_data["Transaction ID"].nunique()

st.subheader('Key Performance Indicators(KPIs)')
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Total Quantity", value=f"{total_quantity:,.0f}")
with col3:
    st.metric(label="Average Unit Price", value=f"${avg_unit_price:,.2f}")
with col4:
    st.metric(label="Total Transaction", value=f"{total_transac:,.0f}")

# Visualization using filtered data
branch_revenue = filtered_data.groupby("Branch")["Total"].sum().reset_index()
fig_branch = px.bar(branch_revenue, title="Revenue Sales by Branch",
                    x="Branch", y="Total", text="Total",
                    color="Branch", color_discrete_sequence=px.colors.sequential.Viridis)

sales_by_product = filtered_data.groupby("Category")["Total"].sum().reset_index()
fig_by_product = px.bar(sales_by_product, title="Sales by Category/Product",
                        y='Total', x="Category", text="Total",
                        color="Category", color_discrete_sequence=px.colors.sequential.Plasma)

scatter_data = filtered_data[["Branch", "Category", "Unit Price", "Quantity", "Total"]].copy()
fig_scatter = px.scatter(
    scatter_data,
    x="Unit Price",
       y="Total",
         size="Quantity",
          color="Branch",
         hover_name="Category",
       title="Sales vs Unit Price analysis",
      labels={"Unit Price": "Unit Price", "Total Amount": "Total Amount"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_scatter.update_traces(marker=dict(line=dict(width=0.5, color="DarkSlateGrey")))

customer_high_transac = filtered_data.groupby("Customer Type")["Total"].sum().reset_index()
fig_cus_high_transac = px.pie(customer_high_transac, title="Customer with the highest Transaction",
                             names="Customer Type",
                             values="Total", color_discrete_sequence=px.colors.sequential.RdBu,
                             hole=0.4)

daily_sales_trend = filtered_data.groupby("Date", as_index=False)["Total"].sum()
fig_sales_trend = px.line(daily_sales_trend, x='Date', y='Total',
                         title="Daily Sales Trend", markers=True,
                         color_discrete_sequence=["#2C3E50"])

# tabs
tab1, tab2, tab3 = st.tabs(["Data Overview", "Sales Analytics", "Business Insights & Recommendation"])
with tab1:
    st.dataframe(data.head(), hide_index=True)
with tab2:
    st.plotly_chart(fig_branch, use_container_width=True)
    st.plotly_chart(fig_by_product, use_container_width=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.plotly_chart(fig_cus_high_transac, use_container_width=True)
    st.plotly_chart(fig_sales_trend, use_container_width=True)
with tab3:
    st.markdown("""
    ### Business Insights
    - The highest-performing branch and product categories are likely driving the majority of revenue and should receive priority inventory and staffing allocation.
    - Sales volume appears to vary by day, indicating a clear opportunity to align staffing, promotions, and restocking to peak demand periods.
    - Customer segments appear to respond differently based on product type and price point, suggesting that offers and recommendations should be targeted rather than one-size-fits-all.
    - Categories with weaker sales momentum may need promotional support, bundle pricing, or repositioning to improve conversion.
    - The relationship between unit price, quantity, and total sales shows that value-oriented shoppers and premium buyers behave differently, so pricing strategy should match demand patterns.

    ### Recommendations
    - Increase stock and replenishment for top-performing branches and categories to avoid stockouts and capitalize on demand.
    - Launch targeted promotions for lower-performing categories to stimulate demand and improve conversion.
    - Plan staffing and marketing campaigns around peak sales days to maximize revenue windows.
    - Use customer-type segmentation to personalize product recommendations and promotions.
    - Monitor product mix regularly and adjust pricing or discount strategies based on category performance.
    - Keep premium and value products positioned separately to appeal to both high-ticket and budget-conscious buyers.
    """)