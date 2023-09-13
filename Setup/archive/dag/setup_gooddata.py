import os
import sys
import airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from connection_ids import psql_conn
from dag_gooddata.setup_ws import create_child_ws, apply_ws_filter


default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}
with DAG(
	default_args=default_args,
	dag_id='init_gooddata',
	start_date=datetime(2023,7,15),
	schedule_interval=None
	) as dag:
	task100 = BashOperator(
		task_id='100__create_connection',
		bash_command='dag_gooddata/create_connection.sh'
		)
	task101 = BashOperator(
		task_id='101__create_master_workspace',
		bash_command='dag_gooddata/create_master_ws.sh'
		)
	task102 = BashOperator(
		task_id='102__import_layout_to_master_workspace',
		bash_command='dag_gooddata/setup_master_ws.sh'
		)
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
		python_callable=create_child_ws
		)
	task106 = PythonOperator(
		task_id='106__apply_ws_filter',
		python_callable=apply_ws_filter
		)

	task100 >> task101 >> task102 >> task105
	task103 >> task104 >> task105
	task105 >> task106