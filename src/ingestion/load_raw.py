from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"

DATABASE_URL = (
    "postgresql+psycopg2://"
    "ecommerce_user:ecommerce_password@localhost:5433/ecommerce"
)

CHUNK_SIZE = 10_000


TABLE_CONFIG = {
    "customers": {
        "file": "olist_customers_dataset.csv",
        "table": "customers",
    },
    "orders": {
        "file": "olist_orders_dataset.csv",
        "table": "orders",
    },
    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "table": "order_items",
    },
    "order_payments": {
        "file": "olist_order_payments_dataset.csv",
        "table": "order_payments",
    },
    "order_reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "table": "order_reviews",
    },
    "products": {
        "file": "olist_products_dataset.csv",
        "table": "products",
    },
    "sellers": {
        "file": "olist_sellers_dataset.csv",
        "table": "sellers",
    },
    "geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "table": "geolocation",
    },
    "product_category_translation": {
        "file": "product_category_name_translation.csv",
        "table": "product_category_translation",
    },
}


def create_engine_connection():
    return create_engine(DATABASE_URL)


def truncate_table(engine, table_name):
    with engine.begin() as connection:
        connection.execute(
            text(f"TRUNCATE TABLE raw.{table_name}")
        )


def validate_row_count(engine, table_name, expected_rows):
    query = text(
        f"SELECT COUNT(*) FROM raw.{table_name}"
    )

    with engine.connect() as connection:
        actual_rows = connection.execute(query).scalar()

    if actual_rows != expected_rows:
        raise ValueError(
            f"Row count mismatch for raw.{table_name}: "
            f"expected {expected_rows:,}, "
            f"got {actual_rows:,}"
        )

    print(
        f"Validation passed: "
        f"{table_name} = {actual_rows:,} rows"
    )


def load_table(engine, config):
    file_path = DATA_DIR / config["file"]
    table_name = config["table"]

    print("\n" + "=" * 70)
    print(f"Loading: {file_path.name}")
    print(f"Target : raw.{table_name}")
    print("=" * 70)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    # Full refresh
    truncate_table(engine, table_name)

    total_rows = 0

    for chunk in pd.read_csv(
        file_path,
        chunksize=CHUNK_SIZE
    ):
        chunk.to_sql(
            name=table_name,
            schema="raw",
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        total_rows += len(chunk)

        print(f"Loaded: {total_rows:,} rows")

    print(f"Finished: {total_rows:,} rows")

    validate_row_count(
        engine,
        table_name,
        total_rows
    )


def main():
    engine = create_engine_connection()

    for config in TABLE_CONFIG.values():
        load_table(engine, config)

    engine.dispose()

    print("\nAll tables loaded successfully.")


if __name__ == "__main__":
    main()
