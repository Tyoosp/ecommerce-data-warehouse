# E-Commerce Data Warehouse & ELT Pipeline

An end-to-end **Data Engineering project** that builds a scalable e-commerce data warehouse and ELT pipeline using the Brazilian E-Commerce Public Dataset by Olist.

The project simulates a real-world data platform where raw e-commerce data is incrementally ingested into PostgreSQL, transformed using dbt, orchestrated with Apache Airflow, validated through automated data quality tests, and exposed through a Streamlit dashboard.

---

## Architecture

```text
                    Olist CSV Dataset
                           │
                           ▼
                  Python Ingestion
                           │
                           ▼
                  PostgreSQL RAW
                           │
                           ▼
                    dbt STAGING
                           │
                           ▼
                 dbt INTERMEDIATE
                           │
                           ▼
                  dbt WAREHOUSE
                  ┌────────┴────────┐
                  ▼                 ▼
             Dimensions           Facts
                  │                 │
                  └────────┬────────┘
                           ▼
                      dbt MARTS
                           │
                           ▼
                    dbt Data Tests
                           │
                           ▼
                  Apache Airflow
                           │
                           ▼
                  Streamlit Dashboard
```

---

## Project Objectives

This project was designed to demonstrate practical Data Engineering capabilities, including:

- Building a PostgreSQL-based data warehouse
- Designing RAW, staging, intermediate, warehouse, and mart layers
- Developing reusable Python ingestion pipelines
- Implementing incremental data ingestion
- Transforming data using dbt
- Designing fact and dimension tables
- Implementing data quality tests
- Creating data lineage and documentation
- Orchestrating pipelines with Apache Airflow
- Containerizing infrastructure using Docker
- Building a BI dashboard for business users

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion and processing |
| Pandas | CSV processing |
| PostgreSQL | Data warehouse and storage |
| dbt | SQL transformation and data modeling |
| Apache Airflow | Pipeline orchestration |
| Docker | Containerized infrastructure |
| Streamlit | Dashboard and data visualization |
| Plotly | Interactive charts |
| SQL | Data transformation and analysis |
| Git | Version control |

---

## Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translations

The original dataset consists of approximately 100,000 orders and more than 100,000 order-item records.

---

## Data Warehouse Design

The warehouse follows a layered architecture.

### RAW Layer

The RAW layer stores source data with minimal transformation.

Tables include:

```text
raw.customers
raw.orders
raw.order_items
raw.order_payments
raw.order_reviews
raw.products
raw.sellers
raw.geolocation
raw.product_category_translation
```

The RAW layer intentionally preserves source-level data and does not enforce analytical primary/foreign keys.

---

### STAGING Layer

The staging layer standardizes and prepares the RAW data for downstream transformations.

Examples:

```text
stg_customers
stg_orders
stg_order_items
stg_order_payments
stg_order_reviews
stg_products
stg_sellers
stg_geolocation
stg_product_category_translation
```

---

### INTERMEDIATE Layer

The intermediate layer combines related datasets and creates reusable business logic.

Examples:

```text
int_orders_enriched
int_order_items_enriched
int_order_payments
```

This layer separates complex transformation logic from final warehouse models.

---

### WAREHOUSE Layer

The warehouse follows a dimensional modeling approach.

#### Dimension Tables

```text
dim_customer
dim_product
dim_seller
dim_date
```

#### Fact Tables

```text
fact_orders
fact_order_items
fact_payments
```

The fact tables are designed around business events such as orders, order items, and payments.

---

### MART Layer

The mart layer contains business-oriented datasets optimized for analytics and reporting.

```text
mart_daily_sales
mart_customer_behavior
mart_product_performance
mart_seller_performance
```

These models provide aggregated metrics for business analysis and dashboarding.

---

## Incremental Data Ingestion

The pipeline includes a simulated monthly incremental ingestion process.

Instead of loading the complete dataset every time, the ingestion process:

1. Determines the month being processed
2. Filters orders for that period
3. Identifies related order IDs
4. Loads related order items
5. Loads related payments
6. Loads related reviews
7. Updates the pipeline watermark

A control table is used to track the ingestion state:

```text
raw.pipeline_control
```

Example:

```text
pipeline_name              last_loaded_date
------------------------------------------------
olist_monthly_ingestion    2017-08-01
```

This simulates how a production pipeline could process newly arriving data periodically.

---

## Data Quality

Automated dbt tests are implemented to validate warehouse integrity.

Examples include:

- `unique`
- `not_null`
- `relationships`

Key validations include:

```text
dim_customer.customer_unique_id
dim_product.product_id
dim_seller.seller_id
fact_orders.order_id
fact_payments.order_id
```

Relationships are also tested between:

```text
fact_orders → dimensions
fact_order_items → fact_orders
fact_order_items → dim_product
fact_order_items → dim_seller
fact_payments → fact_orders
```

The pipeline currently passes all configured dbt data quality tests.

---

## Orchestration

Apache Airflow orchestrates the complete monthly pipeline.

The workflow is:

```text
incremental_ingestion
        │
        ▼
    dbt_build
        │
        ▼
     dbt_test
```

Each step must complete successfully before the next step runs.

The pipeline has been tested end-to-end using Airflow with:

```text
incremental ingestion
        ↓
dbt build
        ↓
dbt test
```

---

## Dashboard

The project includes a Streamlit dashboard providing business-level insights from the marts.

The dashboard includes:

### Key Performance Indicators

- Total Revenue
- Total Orders
- Products Sold
- Customers
- Average Order Value

### Visualizations

- Monthly Revenue
- Top Product Categories by Revenue
- Customer Segmentation
- Top Sellers
- Daily Sales

The dashboard consumes data from the PostgreSQL data warehouse rather than directly querying the raw CSV files.

---

## Project Structure

```text
ecommerce-data-warehouse/
│
├── airflow/
│   ├── dags/
│   │   └── ecommerce_monthly_pipeline.py
│   ├── dbt_profiles/
│   │   └── profiles.yml
│   ├── logs/
│   └── plugins/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dbt/
│
├── ecommerce_dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   ├── warehouse/
│   │   └── marts/
│   ├── macros/
│   ├── logs/
│   ├── target/
│   └── dbt_project.yml
│
├── docs/
│
├── sql/
│   └── 001_create_raw_schema.sql
│
├── src/
│   └── ingestion/
│       ├── load_raw.py
│       ├── incremental_load.py
│       └── profile_source.py
│
├── docker-compose.yml
├── docker-compose.airflow.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY>
cd ecommerce-data-warehouse
```

### 2. Create Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

### 5. Load RAW data

```bash
python src/ingestion/load_raw.py
```

### 6. Run dbt

```bash
cd ecommerce_dbt

dbt build
dbt test
```

### 7. Start Airflow

From the project root:

```bash
docker compose -f docker-compose.airflow.yml up -d --build
```

Airflow is available at:

```text
http://localhost:8082
```

### 8. Start Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard is available at:

```text
http://localhost:8501
```

---

## Key Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

**Data Ingestion**
- Batch ingestion
- Incremental ingestion
- Watermark management
- Chunk-based CSV processing

**Data Modeling**
- Dimensional modeling
- Fact tables
- Dimension tables
- Analytical marts
- Grain definition

**ELT**
- RAW → STAGING → INTERMEDIATE → WAREHOUSE → MART
- SQL-based transformations
- dbt model dependencies

**Data Quality**
- Uniqueness validation
- Null validation
- Referential integrity
- Automated dbt testing

**Orchestration**
- Airflow DAGs
- Task dependencies
- Pipeline scheduling
- End-to-end workflow execution

**Infrastructure**
- Docker
- PostgreSQL
- Container networking

---

## Future Improvements

Potential production-oriented improvements include:

- Replace CSV ingestion with an API or streaming source
- Add Kafka for event streaming
- Add cloud storage such as S3
- Deploy the warehouse to a cloud platform
- Add CI/CD for dbt tests
- Add monitoring and alerting
- Implement Slowly Changing Dimensions
- Add more advanced business metrics
- Deploy the dashboard publicly

---

## Author

Built as a Data Engineering portfolio project to demonstrate practical experience in:

**Python · SQL · PostgreSQL · dbt · Airflow · Docker · Data Warehousing · ELT · Data Quality · Streamlit**
