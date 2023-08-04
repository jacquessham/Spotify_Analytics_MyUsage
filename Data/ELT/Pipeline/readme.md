# Data Pipeline
Coming soon...

## ELT Pipeline in Airflow
<img src=elt_pipeline_airflow.png>

This section documents the functionality of each task but the scripts can be found in the [dags](../../../Setup/dags) folder under the [Setup](../../../Setup) folder.

### elt.py
This is the core DAG for the data pipeline, including creating table and the whole ELT process. There are ... tasks...
<br><br>
More details coming soon...

### Task 1-4: Create tables for all Schemas
Task 1-4 would create tables (if not exists) in the Postgres database for all schemas. The details of the tables can be found in the [Database Tables](../Database_Tables). Each task would execute the following SQL scripts, respective to the schemas:

<ul>
	<li>Source Schema: create_tables_src.sql</li>
	<li>Staging Schema: create_tables_stg.sql</li>
	<li>Central Storage Schema: create_tables_ctr.sql</li>
	<li>Output Stage Schema: create_tables_out.sql</li>
</ul>

All the SQL scripts are saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.

### Task 5: Extract Full Data
Coming soon...

### Task 6: Extract Last 12 Months Data
Coming soon...

### Task 7: Remove Duplicated Records
Coming soon...

### Task 8: Update Records in Central Storage Schema
Coming soon...

### Task 9: Insert Records to Central Storage Schema
Coming soon...

### Task 10: Distribute Data to Output Stage
Coming soon...