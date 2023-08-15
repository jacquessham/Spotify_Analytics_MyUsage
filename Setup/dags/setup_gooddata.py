import os
import sys
import airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator



env_home = os.getenv('AIRFLOW_HOME')
sys.path.insert(0,env_home+"/gooddata")


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

	task100 >> task101 >> task102