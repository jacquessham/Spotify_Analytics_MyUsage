import os
import sys
import airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from connection_ids import psql_conn
from dag_gooddata.setup_ws import create_child_ws_api, create_ws_filter_api


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}
with DAG(
	default_args=default_args,
	dag_id='lcm_gooddata',
	start_date=datetime(2023,7,15),
	schedule_interval='0 5 * * Mon'
	) as dag:
	task103 = PostgresOperator(
		task_id='103__create_ws_lcm_table',
		postgres_conn_id=psql_conn,
		sql='dag_gooddata/create_tables_lcm.sql'
		)
	task104 = PostgresOperator(
		task_id='104__update_username_list',
		postgres_conn_id=psql_conn,
		sql='dag_gooddata/update_username_list.sql'
		)
	task105 = PythonOperator(
		task_id='105__create_child_ws',
		python_callable=create_child_ws_api 
		)
	task106 = PythonOperator(
		task_id='106__apply_ws_filter',
		python_callable=create_ws_filter_api
		)

	task103 >> task104 >> task105 >> task106
