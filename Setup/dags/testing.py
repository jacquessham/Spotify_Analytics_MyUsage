from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def testing_storage():
	with open('gooddata/testing.txt','w') as f:
		f.write('Hello GoodData!')

	with open('Central_Storage_Data/testing.txt','w') as j:
		j.write('Hello Storage!')



default_args = {
	'owner': 'Jacques Sham',
	'retries': 5,
	'retry_delay': timedelta(minutes=5)
}

with DAG(
	default_args=default_args,
	dag_id='testing',
	start_date=datetime(2023,7,15),
	schedule_interval='0 4 * * Mon'
	) as dag:
	task1 = PythonOperator(
		task_id='testing_storage',
		python_callable=testing_storage
		)