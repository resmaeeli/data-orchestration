import sys
from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

# sys.path.insert(0, "/opt/airflow/data-portfolio/python")
sys.path.insert(0, "/opt/airflow/data-portfolio/powerbi")

# from run import run_job
from build_dataset import main


def export_task():
    main()
    # run_job("orders_per_year", "csv")


with DAG(
    dag_id="data_portfolio_export",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-portfolio", "export"],
) as dag:

    export = PythonOperator(
        task_id="build_all_datasets",
        python_callable=export_task,
    )
