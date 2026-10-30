import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
)

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://ecommerce_user:"
    "ecommerce_password@localhost:5433/ecommerce",
)

engine = create_engine(DB_URL)


# ============================================================
# HELPERS
# ============================================================

@st.cache_data
def load_data():

    daily_sales = pd.read_sql(
        """
        SELECT *
        FROM marts.mart_daily_sales
        ORDER BY sales_date
        """,
        engine,
    )

    customer = pd.read_sql(
        """
        SELECT *
        FROM marts.mart_customer_behavior
        """,
        engine,
    )

    product = pd.read_sql(
        """
        SELECT *
        FROM marts.mart_product_performance
        """,
        engine,
    )

    seller = pd.read_sql(
        """
        SELECT *
        FROM marts.mart_seller_performance
        """,
        engine,
    )

    return daily_sales, customer, product, seller


daily_sales, customer, product, seller = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🛒 Olist E-Commerce Analytics Dashboard")

st.markdown(
    """
    **Business dashboard powered by PostgreSQL + dbt marts**

    Data pipeline:
    `CSV → Python → PostgreSQL → dbt → Airflow → Dashboard`
    """
)


# ============================================================
# KPI
# ============================================================

total_revenue = daily_sales["total_sales_value"].sum()
total_orders = daily_sales["total_orders"].sum()
total_items = daily_sales["total_products_sold"].sum()
total_customers = customer["customer_unique_id"].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

on_time_rate = None


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"R$ {total_revenue:,.0f}",
)

col2.metric(
    "Total Orders",
    f"{total_orders:,.0f}",
)

col3.metric(
    "Products Sold",
    f"{total_items:,.0f}",
)

col4.metric(
    "Customers",
    f"{total_customers:,.0f}",
)

col5.metric(
    "Avg Order Value",
    f"R$ {average_order_value:,.2f}",
)


st.divider()


# ============================================================
# SALES TREND
# ============================================================

st.subheader("📈 Sales Performance")

monthly_sales = (
    daily_sales
    .assign(
        month=pd.to_datetime(daily_sales["sales_date"])
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month", as_index=False)
    .agg(
        revenue=("total_sales_value", "sum"),
        orders=("total_orders", "sum"),
        products=("total_products_sold", "sum"),
    )
)

fig_sales = px.line(
    monthly_sales,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue",
)

fig_sales.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (R$)",
)

st.plotly_chart(
    fig_sales,
    use_container_width=True,
)


# ============================================================
# PRODUCT + CUSTOMER
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏆 Top Product Categories")

    top_categories = (
        product
        .groupby(
            "product_category_name_english",
            as_index=False,
        )
        .agg(
            revenue=("total_product_revenue", "sum"),
            items=("total_items_sold", "sum"),
        )
        .sort_values(
            "revenue",
            ascending=False,
        )
        .head(10)
    )

    top_categories = top_categories[
        top_categories[
            "product_category_name_english"
        ].notna()
    ]

    fig_product = px.bar(
        top_categories,
        x="revenue",
        y="product_category_name_english",
        orientation="h",
        title="Top 10 Product Categories by Revenue",
    )

    fig_product.update_layout(
        xaxis_title="Revenue (R$)",
        yaxis_title="Category",
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True,
    )


with col2:

    st.subheader("👥 Customer Segments")

    segment = (
        customer
        .groupby(
            "customer_segment",
            as_index=False,
        )
        .agg(
            customers=("customer_unique_id", "nunique"),
            spending=("total_spending", "sum"),
        )
    )

    fig_segment = px.pie(
        segment,
        names="customer_segment",
        values="customers",
        title="Customer Distribution",
        hole=0.4,
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True,
    )


# ============================================================
# SELLER PERFORMANCE
# ============================================================

st.subheader("🏪 Top Sellers")

top_sellers = (
    seller
    .sort_values(
        "total_sales_value",
        ascending=False,
    )
    .head(10)
    .copy()
)

top_sellers["seller"] = (
    top_sellers["seller_city"]
    + ", "
    + top_sellers["seller_state"]
)

fig_seller = px.bar(
    top_sellers,
    x="total_sales_value",
    y="seller",
    orientation="h",
    title="Top 10 Sellers by Sales Value",
)

fig_seller.update_layout(
    xaxis_title="Sales Value (R$)",
    yaxis_title="Seller Location",
)

st.plotly_chart(
    fig_seller,
    use_container_width=True,
)


# ============================================================
# DATA PREVIEW
# ============================================================

with st.expander("🔎 View Daily Sales Data"):

    st.dataframe(
        daily_sales,
        use_container_width=True,
    )
