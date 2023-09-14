import os
import sys
from datetime import datetime, timedelta, date
import json
import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from ELT.extract import extract_full, extract_last12mos
from ELT.export import export_direct, export_update
from connection_ids import psql_conn


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}

today = date.today()
last_monday = today - timedelta(days=today.weekday(), weeks=0)
last_monday = datetime.combine(last_monday, datetime.min.time())

with DAG(
	default_args=default_args,
	dag_id='elt_v1',
	start_date=last_monday,
	schedule_interval='0 4 * * Mon'
	) as dag:
	task1 = PostgresOperator(
		task_id='1__create_tables_src',
		postgres_conn_id=psql_conn,
		sql='ELT/create_tables_src.sql'
		)
	task2 = PostgresOperator(
		task_id='2__create_tables_stg',
		postgres_conn_id=psql_conn,
		sql='ELT/create_tables_stg.sql'
		)
	task3 = PostgresOperator(
		task_id='3__create_tables_ctr',
		postgres_conn_id=psql_conn,
		sql='ELT/create_tables_ctr.sql'
		)
	task4 = PostgresOperator(
		task_id='4__create_tables_out',
		postgres_conn_id=psql_conn,
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
		postgres_conn_id=psql_conn,
		sql='ELT/distinct_stream_history.sql'
		)
	task8 = PostgresOperator(
		task_id='8__transform_streaming_history_upgrade',
		postgres_conn_id=psql_conn,
		sql='ELT/transform_stream_history_upgrade.sql'
		)
	task9 = PostgresOperator(
		task_id='9__transform_streaming_history_direct_insert',
		postgres_conn_id=psql_conn,
		sql='ELT/transform_stream_history_direct_insert.sql'
		)
	task10 = PostgresOperator(
		task_id='10__insert_out_streaming_history',
		postgres_conn_id=psql_conn,
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
	"""
	# Now require to remove cache manually until network problem resolved
	task13 = BashOperator(
		task_id='13__refresh_output_tables',
		bash_command='ELT/refresh_output_tables.sh'
		)
	"""


	task1 >> [task5, task6] 
	task2 >> [task5, task6] 
	task3 >> [task5, task6] 
	task4 >> [task5, task6] 
	task5 >> task7
	task6 >> task7
	task7 >> task8 >> task9 >> task10 # >> task13
	task9 >> task11 >> task12

