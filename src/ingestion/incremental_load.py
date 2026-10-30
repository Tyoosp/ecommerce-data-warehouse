import os
import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

DB_URL = os.getenv(
	"DATABASE_URL",
	"postgresql+psycopg2://ecommerce_user:"
	"ecommerce_password@localhost:5433/ecommerce"
)

engine = create_engine(DB_URL)

ORDERS_FILE = RAW_DATA_DIR / "olist_orders_dataset.csv"
ORDER_ITEMS_FILE = RAW_DATA_DIR / "olist_order_items_dataset.csv"
PAYMENTS_FILE = RAW_DATA_DIR / "olist_order_payments_dataset.csv"
REVIEWS_FILE = RAW_DATA_DIR / "olist_order_reviews_dataset.csv"


# ============================================================
# CONTROL TABLE
# ============================================================

def create_control_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw.pipeline_control (
                pipeline_name VARCHAR(100) PRIMARY KEY,
                last_loaded_date DATE
            )
        """))


def get_last_loaded_date():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT last_loaded_date
            FROM raw.pipeline_control
            WHERE pipeline_name = 'olist_incremental'
        """)).scalar()

    return result


def update_last_loaded_date(load_date):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO raw.pipeline_control (
                pipeline_name,
                last_loaded_date
            )
            VALUES (
                'olist_incremental',
                :load_date
            )
            ON CONFLICT (pipeline_name)
            DO UPDATE SET
                last_loaded_date = EXCLUDED.last_loaded_date
        """), {
            "load_date": load_date
        })


# ============================================================
# LOAD DATA
# ============================================================

def load_month(month_start, month_end):

    print("=" * 60)
    print("INCREMENTAL LOAD")
    print("=" * 60)

    print(f"Period : {month_start} → {month_end}")

    # --------------------------------------------------------
    # ORDERS
    # --------------------------------------------------------

    orders = pd.read_csv(
        ORDERS_FILE,
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    orders = orders[
        (orders["order_purchase_timestamp"] >= month_start)
        & (orders["order_purchase_timestamp"] < month_end)
    ].copy()

    print(f"Orders found: {len(orders):,}")

    if orders.empty:
        print("No orders found for this period.")
        return

    order_ids = orders["order_id"].tolist()

    # --------------------------------------------------------
    # ORDER ITEMS
    # --------------------------------------------------------

    order_items = pd.read_csv(
        ORDER_ITEMS_FILE,
        parse_dates=["shipping_limit_date"]
    )

    order_items = order_items[
        order_items["order_id"].isin(order_ids)
    ].copy()

    # --------------------------------------------------------
    # PAYMENTS
    # --------------------------------------------------------

    payments = pd.read_csv(
        PAYMENTS_FILE
    )

    payments = payments[
        payments["order_id"].isin(order_ids)
    ].copy()

    # --------------------------------------------------------
    # REVIEWS
    # --------------------------------------------------------

    reviews = pd.read_csv(
        REVIEWS_FILE,
        parse_dates=[
            "review_creation_date",
            "review_answer_timestamp"
        ]
    )

    reviews = reviews[
        reviews["order_id"].isin(order_ids)
    ].copy()

    # --------------------------------------------------------
    # INSERT INTO RAW
    # --------------------------------------------------------

    orders.to_sql(
        "orders",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi"
    )

    order_items.to_sql(
        "order_items",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi"
    )

    payments.to_sql(
        "order_payments",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi"
    )

    reviews.to_sql(
        "order_reviews",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi"
    )

    print()
    print("Loaded:")
    print(f"  orders       : {len(orders):,}")
    print(f"  order_items  : {len(order_items):,}")
    print(f"  payments     : {len(payments):,}")
    print(f"  reviews      : {len(reviews):,}")

    # --------------------------------------------------------
    # UPDATE WATERMARK
    # --------------------------------------------------------

    update_last_loaded_date(
        pd.Timestamp(month_end).date()
    )

    print()
    print(f"Watermark updated → {pd.Timestamp(month_end).date()}")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Incremental Olist data ingestion"
    )

    parser.add_argument(
        "--month",
        required=True,
        help="Month to load, format YYYY-MM"
    )

    args = parser.parse_args()

    create_control_table()

    month_start = pd.Timestamp(
        f"{args.month}-01"
    )

    month_end = month_start + pd.offsets.MonthBegin(1)

    last_loaded = get_last_loaded_date()

    if last_loaded is not None:
        print(f"Last loaded date: {last_loaded}")

        if month_start.date() < last_loaded:
            raise ValueError(
                f"Month {args.month} is older than "
                f"last loaded date {last_loaded}"
            )

    load_month(
        month_start,
        month_end
    )


if __name__ == "__main__":
    main()
