import streamlit as st
import pandas as pd 
import plotly.express as px

#  Setting page Name
st.set_page_config(page_title="Pharmacy Sales Dashboard")

st.markdown("""
<style>
    .header {background-color: #2C3E50;
    color: #FFFFFF;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
        }
</style>
<div class="header">
     <h1>Pharmacy Sales Analysis</h1>
     </div>
     """, unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path, encoding="latin")
    data.columns = data.columns.str.lower().str.strip().str.replace(" ", "_")
    data["date"] = pd.to_datetime(data["date"], errors="coerce").dt.date
    data["unit_price"] = data["unit_price"].str.replace("GHS", "").astype(float)
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = data["unit_price"].fillna(data["unit_price"].mean())

    data["total_amount"] = data["total_amount"].fillna(data["total_amount"].mean())
    data["payment_method"] = data["payment_method"].fillna("unknown")
    data["pharmacist_name"] = data["pharmacist_name"].fillna("unknown")
    data["rating"] = data["rating"].fillna(data["rating"].mean())
    data = data.dropna(subset=["date"])
    data["total_amount"] = data["unit_price"] * data["quantity"]

    return data
file_path = "pharmacy_messy.csv"
data = load_data(file_path)

st.sidebar.title("👨‍💻 Developer Profile")
st.sidebar.write("*Desmond Pimpong*")
st.sidebar.caption("Data Analyst &  Developer")

st.sidebar.markdown("---")

# Quick links buttons
st.sidebar.subheader("🔗 Links & Portfolio")
st.sidebar.link_button("📂 GitHub Repository", "https://github.com/Desmond-dev12/pharmacy-sales-dashboard")
st.sidebar.link_button("💼 LinkedIn Profile", "https://linkedin.com/in/desmond-pimpong-563899433")

st.sidebar.markdown("---")

# Tech stack breakdown
st.sidebar.subheader("🛠️ Built With")
st.sidebar.text("• Python 3.10+\n• Streamlit\n• Pandas & Plotly")

# sidebar Creation

st.sidebar.header("Filters")
selected_branch = st.sidebar.multiselect("Select_branch", options= data["branch"].unique(),
                                          default=data["branch"].unique())
selected_customer_type = st.sidebar.multiselect("Select_customer_type", options=data["customer_type"].unique(), 
                       default=data["customer_type"].unique())
selected_gender = st.sidebar.multiselect("Gender", options=data["gender"].unique(),
                        default=data["gender"].unique())
selected_drug_category = st.sidebar.multiselect("Drug_category", options=data["drug_category"].unique(),
                        default=data["drug_category"].unique())
min_date = data["date"].min()
max_date = data["date"].max()
selected_date = st.sidebar.date_input("selected date range", 
                                      value=(min_date, max_date),
                                      min_value=min_date,
                                      max_value=max_date)
if not selected_date or len(selected_date) != 2:
    st.warning("Please select a valid date range")
    st.stop()

# Filters

branch_filter = data["branch"].isin(selected_branch)
customer_type_filter = data["customer_type"].isin(selected_customer_type)   
gender_filter = data["gender"].isin(selected_gender)
drug_category_filter = data["drug_category"].isin(selected_drug_category)
data["date"] = pd.to_datetime(data["date"])
start_date = pd.to_datetime(selected_date[0])
end_date = pd.to_datetime(selected_date[1])
date_filter = (data["date"] >= start_date) & (data["date"] <= end_date)
filtered_data = data[branch_filter & customer_type_filter & gender_filter &
                     drug_category_filter & date_filter]
if filtered_data.empty:
    st.warning("No Data found for the filters")
    st.stop()
    st.dataframe(filtered_data.head())  

# Round figures to two decimal places

filtered_data["total_amount"] = filtered_data["total_amount"].round(2)
filtered_data["total_amount"] = filtered_data["total_amount"].round(2)
filtered_data["unit_price"] = filtered_data["unit_price"].round(2)
filtered_data["rating"] = filtered_data["rating"].round(2)
filtered_data["branch"] = filtered_data["branch"]
filtered_data["receipt_id"] = filtered_data["receipt_id"].round(2)

# Key Performance Indicator(KPIS)

total_sales = filtered_data["total_amount"].sum()
total_quantity = filtered_data["quantity"].sum()
average_unit_price = filtered_data["unit_price"].mean()
average_rating_by_customer = filtered_data["rating"].mean()
total_transactions = filtered_data["receipt_id"].nunique()


st.subheader('Key Performance Indicators (KPIs)')
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Total Quantity", value=f"{total_quantity:,.0f}")
with col3:
    st.metric(label="Average unit Price", value=f'{average_unit_price:,.1f}')
with col4:
    st.metric(label="Total Transactions", value=f"{total_transactions}")

# Calculation of current and previous month analysis

data["date"] = pd.to_datetime(data["date"], errors="coerce")
current_month = data["date"].dt.month.max()
previous_month = current_month - 1
filtered_data["date"] = pd.to_datetime(filtered_data["date"], errors="coerce")
current_sales = filtered_data[filtered_data["date"].dt.month == current_month]["total_amount"].sum()
previous_sales = filtered_data[filtered_data["date"].dt.month == previous_month]["total_amount"].sum()
growth_pct = ((current_sales - previous_sales) / previous_sales) * 100
st.metric(label="Total Sales(This Month)",
          value=f"GHS{current_sales:,.2f}",
          delta=f'{growth_pct:,.1f}% vs last month')

# Data visualization

total_sales_by_branch = filtered_data.groupby("branch")["total_amount"].sum().round(2).reset_index()
fig_by_branch = px.bar(total_sales_by_branch,
                       title="Total Sales by Branch",
                        x="branch",
                         y="total_amount",
                          text="total_amount",
                          text_auto=".2s",
                           color="branch")

total_drug_sales = filtered_data.groupby("drug_category")["total_amount"].sum().reset_index()
avg_rating_by_drug_category = filtered_data.groupby("drug_category")["rating"].mean().reset_index()
st.subheader("Total Sales and Rating by Drug Category")
col1,col2 = st.columns(2)
with col1:
    fig_by_sales_drug_cat = px.bar(total_drug_sales,
                                   title="Overall Sales by Drug Category",
                                   x="drug_category",
                                   y="total_amount",
                                   text="total_amount",
                                    text_auto=".2s",
                                   color_discrete_sequence=px.colors.sequential.Plasma
                                   )
    fig_by_sales_drug_cat.update_layout(xaxis=dict(tickangle=-45),
                                        margin=dict(b=100, t=40))
    
    fig_avg_sales_by_drug = px.bar(avg_rating_by_drug_category,
                                   title="Average Sales by Drug Category",
                                   x="drug_category",
                                   y="rating",
                                   text="rating",
                                   text_auto=".2s",
                                   color="drug_category",
                                   color_discrete_sequence=px.colors.sequential.Viridis
                                   )
    fig_avg_sales_by_drug.update_layout(xaxis=dict(tickangle=-60),
    margin=dict(b=100, t=40,))
    
    sales_by_customer = filtered_data.groupby("customer_type")["total_amount"].sum().round(2).reset_index()
    sales_by_payment_method = filtered_data.groupby("payment_method")["total_amount"].sum().reset_index()
    daily_sales_trend = filtered_data.groupby("date")["total_amount"].sum().reset_index()
    sales_by_customer["customer_type"]= sales_by_customer["customer_type"].round(2)
    sales_by_payment_method["payment_method"]= sales_by_payment_method["payment_method"].round(1)
    daily_sales_trend["date"]= daily_sales_trend["date"]

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["day_of_week"] = data["date"].dt.day_name()
    revenue_by_day = data.groupby("day_of_week")["total_amount"].sum().round(2).reset_index()
    data["day_of_week"] = data["day_of_week"]

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
revenue_by_day["day_of_week"]= pd.Categorical(revenue_by_day["day_of_week"],
                                              categories=day_order,
                                              ordered=True)
revenue_by_day = revenue_by_day.sort_values(by="day_of_week", ascending=True)

fig_by_customer = px.bar(sales_by_customer,
                         title="Sales Distribution by each Customer Type",
                         x='customer_type',
                         y="total_amount",
                         text="total_amount",
                         color="customer_type",
                         text_auto=".2s",
                         color_discrete_sequence=px.colors.sequential.Plasma
                         )

fig_by_payment = px.pie(sales_by_payment_method,
                        names="payment_method",
                        values="total_amount",
                        title="Total Revenue Share by Payment Method",
                        hole=0.4
                        )
                        
fig_sales_trend = px.line(daily_sales_trend,
                          x="date",
                                                   y="total_amount",
                                                   title="Daily Sales Trend",
                                                   markers=True,
                                                   color_discrete_sequence=["#2C3E50"]
                                                
                                                    )

fig_day_revenue = px.bar(revenue_by_day, title="Revenue from Each Day of the week",
                         x="day_of_week",
                         y="total_amount",
                         text="total_amount",
                         color="day_of_week",
                         text_auto=".2s",
                         color_discrete_sequence=px.colors.sequential.Plasma)
# tabs
tab1, tab2 = st.tabs(["**Data Overview**", "**Sales Analysis**"])
with tab1:
    st.dataframe(data.head(10), hide_index=True)

with tab2:
    st.plotly_chart(fig_by_branch, use_container_width=True)
    st.plotly_chart(fig_by_sales_drug_cat, use_container_width=True)
    st.plotly_chart(fig_avg_sales_by_drug, use_container_width=True)
    st.plotly_chart(fig_by_customer, use_container_width=True)
    st.plotly_chart(fig_by_payment, use_container_width=True)
    st.plotly_chart(fig_day_revenue, use_container_width=True)
    st.plotly_chart(fig_sales_trend,use_container_width=True)

    st.divider()
    col1,col2,col3 = st.columns(3)
with col1:
    st.markdown("**GitHub Repository**")
    st.markdown("[**GitHub Connect**](https://github-Desmond-dev12)")
with col2:
    st.markdown("**Linkedin Profile**")
    st.markdown("[**LinkedIn Connect**](https://www.linkedin.com/in/desmond-pimpong-563899433/)")
st.divider()
st.info("Click Here to View Executive Summary")
with st.expander("Executive Summary and Business Insights"):
 st.markdown(""" ### **Key Business Insights**
* **Accra Central Dominates Branch Sales**: Accra Central leads overall revenue significantly at 44k, almost double the sales of Kumasi (24k) and Takoradi (26k).
* **Painkillers and Skincare Drive Product Revenue**: Painkillers (22k) and Skincare (20k) are the top-earning categories, whereas Diabetes & BP drugs lag furthest behind at 7.5k.
* **Customer Satisfaction vs. Revenue Mismatch**: Painkillers command the highest satisfaction rating at 6.9, but high-selling Antibiotics (18k) trail in customer rating at 5.9, and Diabetes & BP sits at the lowest rating (5.6).
* **Insurance and Prescription Reliance**: Revenue is mostly anchored by Insurance (34k) and Prescription (32k) customers, while casual Walk-in purchases trail at 28k.
* **Mobile Money and Insurance Dominate Payments**: Mobile Money (31.6%) and Insurance (28.8%) account for over 60% of total transaction volume, while Cash represents the smallest payment slice at 16.1%.
* **Thursday–Friday Peak Sales Window**: Daily revenue surges on Thursday and Friday (18k each) before dropping to a midweek low on Tuesday (7.9k).
### **Recommendations**
* **Reallocate Regional Inventory to Accra Central**: Increase stock distribution ratios toward Accra Central to sustain high sales velocity and prevent stockouts on top-moving items.
* **Audit Low-Rated Drug Categories**: Investigate customer feedback and supplier quality for Diabetes & BP (5.6 rating) and Antibiotics (5.9 rating) to improve satisfaction scores.
* **Capitalize on Painkiller & Skincare Demand**: Expand shelf presence, promotional bundles, and cross-selling strategies for high-margin, top-rated categories like Painkillers and Skincare.
* **Optimize Midweek Staffing & Restocking**: Schedule major inventory replenishment on Wednesday afternoons ahead of the Thursday-Friday peak (18k sales volume), while scaling back shift hours during the Tuesday slump (7.9k).
* **Strengthen Digital & Insurance Partnerships**: Partner directly with Mobile Money providers and health insurance vendors to run streamlined checkout promotions and reduce cash-handling friction.
* **Drive Walk-in Customer Conversion**: Launch OTC (Over-The-Counter) loyalty initiatives to incentivize walk-in shoppers (28k) to convert into recurring prescription or insurance-backed customers."""


 )