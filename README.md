# Retail Sales Analysis Dashboard

An interactive Streamlit dashboard for exploring retail sales performance across branches, product categories, customer segments, and date ranges.

## Overview

This project analyzes retail transaction data to help businesses understand:

- which branches generate the most revenue
- which product categories perform best
- how customer type and gender affect sales
- how sales trend over time
- which products or segments deserve more attention

The dashboard is designed to turn raw retail data into actionable business insights using Python, Pandas, Plotly, and Streamlit.

## Features

- interactive sidebar filters for branch, category, customer type, gender, and date range
- KPI cards for total sales, total quantity, average unit price, and total transactions
- revenue analysis by branch
- sales by category
- scatter plot for unit price vs total sales
- customer distribution chart
- daily sales trend visualization
- business insights and recommendations section

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

- `Retail.py` — main dashboard application
- `requirements.txt` — project dependencies
- `README.md` — project documentation
- `retail_store_clean1.csv` — retail sales dataset used by the dashboard

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment if needed.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

From the project folder, run:

```bash
streamlit run Retail.py
```

Then open the local URL shown in the terminal in your browser.

## Data Requirements

The dashboard expects a CSV file with columns such as:

- Branch
- Category
- Customer Type
- Gender
- Date
- Total
- Quantity
- Unit Price
- Transaction ID
- Rating
 

## Business Use Case

This dashboard is useful for:

- retail managers tracking branch performance
- sales teams reviewing category trends
- analysts comparing customer segments
- business teams planning inventory and promotions

## Example Insights

- identify top-performing branches
- detect seasonal or daily sales patterns
- monitor category performance
- compare sales behavior across customer types
- support inventory planning and marketing decisions

## 👤 Author

*Desmond Pimpong*

## 📬 Contact

- LinkedIn: https://linkedin.com/in/desmond-pimpong-563899433

## License

This project is intended for learning, portfolio development, and business analytics practice.
