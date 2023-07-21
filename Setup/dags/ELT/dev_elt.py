import os
import sys
from datetime import datetime, timedelta
import json
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from ELT.extract import extract_full, extract_last12mos


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}

with DAG(
	default_args=default_args,
	dag_id='dev_elt_v1',
	start_date=datetime(2023,7,1),
	schedule_interval='0 4 * * Mon'
	) as dag:
	task1 = PostgresOperator(
		task_id='create_tables',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='dags/ELT/create_tables.sql'
		)
	task2 = PythonOperator(
		task_id='extract_full',
		python_callable=extract_full
		)
	task2 = PythonOperator(
		task_id='extract_last12mos',
		python_callable=extract_last12mos
		)


	task1 >> [task2, task3]