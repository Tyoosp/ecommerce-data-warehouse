from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = "/opt/project"
DBT_DIR = f"{PROJECT_DIR}/ecommerce_dbt"

with DAG(
    dag_id="ecommerce_monthly_pipeline",
    description="Monthly incremental Olist ELT pipeline",
    start_date=datetime(2017, 3, 1),
    schedule="@monthly",
    catchup=False,
    tags=["ecommerce", "dbt", "data-engineering"],
) as dag:

    incremental_ingestion = BashOperator(
        task_id="incremental_ingestion",
        bash_command=f"""
        cd {PROJECT_DIR} &&
        python src/ingestion/incremental_load.py \
        --month {{{{ data_interval_start.strftime('%Y-%m') }}}}
        """,
        env={
            "DATABASE_URL":
                "postgresql+psycopg2://ecommerce_user:"
                "ecommerce_password@ecommerce-postgres:5432/ecommerce"
        },
        append_env=True,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"""
        cd {DBT_DIR} &&
        dbt build --profiles-dir /opt/project/airflow/dbt_profiles
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_DIR} &&
        dbt test --profiles-dir /opt/project/airflow/dbt_profiles
        """,
    )

    incremental_ingestion >> dbt_build >> dbt_test
