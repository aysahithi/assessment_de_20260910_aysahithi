from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 8, 1),
    schedule_interval="@daily",   # runs once per day
    catchup=True,
    default_args=default_args,
) as dag:

    # Daily run: Airflow injects {{ ds }} (execution date)
    extract = BashOperator(
        task_id="extract_weather",
        bash_command="python /opt/airflow/ingestion/extract_load.py {{ ds }}"
    )

    # Optional backfill run: use conf to pass start_date and end_date
    # Example trigger:
    # airflow dags trigger weather_pipeline --conf '{"start_date":"2026-09-01","end_date":"2026-09-10"}'
    extract_range = BashOperator(
        task_id="extract_weather_range",
        bash_command=(
            "python /opt/airflow/ingestion/extract_load.py "
            "{{ dag_run.conf.get('start_date', ds) }} "
            "{{ dag_run.conf.get('end_date', ds) }}"
        )
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run --log-path /home/airflow/dbt_run.log"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test --log-path /home/airflow/dbt_test.log"
    )

    # Default daily flow
    extract >> dbt_run >> dbt_test

    # If you trigger with conf (range), it will run extract_range instead
    extract_range >> dbt_run >> dbt_test
