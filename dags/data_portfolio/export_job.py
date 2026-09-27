import sys
from datetime import datetime, timedelta

from airflow.sdk import DAG, task

sys.path.insert(0, "/opt/airflow/data-portfolio/python")


from config import load_jobs
from run import run_job


@task
def get_jobs():
    return load_jobs()


@task(retries=2, retry_delay=timedelta(minutes=1))
def export_job(job):
    output_format = job.get("file_format")
    run_job(job["name"], output_format)


with DAG(
    dag_id="data_portfolio_export",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data-portfolio", "export"],
) as dag:

    jobs = get_jobs()

    export_job.expand(job=jobs)
