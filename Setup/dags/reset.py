import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}

with DAG(
	default_args=default_args,
	dag_id='dev_reset_v1',
	start_date=datetime(2023,7,15),
	schedule_interval=None
	) as dag:
	task1 = PostgresOperator(
		task_id='reset_tables',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='reset/reset.sql'
		)
	task1
