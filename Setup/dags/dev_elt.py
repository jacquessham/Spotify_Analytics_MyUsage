import os
import sys
from datetime import datetime, timedelta
import json
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from ELT.extract import extract_full, extract_last12mos
from ELT.export import export_direct


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}

with DAG(
	default_args=default_args,
	dag_id='dev_elt_v2',
	start_date=datetime(2023,7,15),
	schedule_interval='0 4 * * Mon'
	) as dag:
	task1 = PostgresOperator(
		task_id='1__create_tables_src',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/create_tables_src.sql'
		)
	task2 = PostgresOperator(
		task_id='2__create_tables_stg',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/create_tables_stg.sql'
		)
	task3 = PostgresOperator(
		task_id='3__create_tables_ctr',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/create_tables_ctr.sql'
		)
	task4 = PostgresOperator(
		task_id='4__create_tables_out',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/create_tables_out.sql'
		)
	task5 = PythonOperator(
		task_id='5__extract_full',
		python_callable=extract_full
		)
	task6 = PythonOperator(
		task_id='6__extract_last12mos',
		python_callable=extract_last12mos
		)
	task7 = PostgresOperator(
		task_id='7__distinct_streaming_history',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/distinct_stream_history.sql'
		)
	task8 = PostgresOperator(
		task_id='8__transform_streaming_history_upgrade',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/transform_stream_history_upgrade.sql'
		)
	task9 = PostgresOperator(
		task_id='9__transform_streaming_history_direct_insert',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/transform_stream_history_direct_insert.sql'
		)
	task10 = PostgresOperator(
		task_id='10__insert_out_streaming_history',
		postgres_conn_id='postgres_airflow_docker_spotify',
		sql='ELT/out_stream_history.sql'
		)
	task11 = PythonOperator(
		task_id='11__export_json_update',
		python_callable=export_update
		)
	task12 = PythonOperator(
		task_id='12__export_json_direct',
		python_callable=export_direct
		)
	task13 = BashOperator(
		task_id='13__refresh_output_tables',
		bash_command='sh gooddata/refresh_output_tables.sh'
		)


	task1 >> [task5, task6] 
	task2 >> [task5, task6] 
	task3 >> [task5, task6] 
	task4 >> [task5, task6] 
	task5 >> task7
	task6 >> task7
	task7 >> task8 >> task9 >> task10 >> task13
	task9 >> task11 >> task12

