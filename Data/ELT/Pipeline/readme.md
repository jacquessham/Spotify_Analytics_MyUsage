# Data Pipeline
Coming soon...

## ELT Pipeline in Airflow
<img src=elt_pipeline_airflow.png>

This section documents the functionality of each task but the scripts can be found in the [dags](../../../Setup/dags) folder under the [Setup](../../../Setup) folder.

### elt.py
This is the core DAG for the data pipeline, including creating table and the whole ELT process. There are ... tasks...
<br><br>
More details coming soon...

#### Task 1-4: Create tables for all Schemas
Task 1-4 would create tables (if not exists) in the Postgres database for all schemas. The details of the tables can be found in the [Database Tables](../Database_Tables). Each task would execute the following SQL scripts, respective to the schemas:

<ul>
	<li>Source Schema: create_tables_src.sql</li>
	<li>Staging Schema: create_tables_stg.sql</li>
	<li>Central Storage Schema: create_tables_ctr.sql</li>
	<li>Output Stage Schema: create_tables_out.sql</li>
</ul>

All the SQL scripts are saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.

#### Task 5: Extract Full Data
Task 5 would extract the datasets available in the <b>full_data</b> folder under the [Data](../../) folder. This task would load the JSON files saved in the <b>full_data</b> folder into <i>src__data.src__streaming_history</i> table, and record the operation in the <i>src__data.src__upload_log</i> table. The task would only load a file with the same file name once only by checking the logs in the <i>src__data.src__upload_log</i> table. <b>Users should keep the format of the JSON files to prevent any potential error!</b>
<br><br>
This task would utilize the functions available in <i>extract.py</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.

#### Task 6: Extract Last 12 Months Data
Task 6 would extract the datasets available in the <b>last_12mos</b> folder under the [Data](../../) folder. This task would load the JSON files saved in the <b>username</b> folder in the <b>last_12mos</b> folder into <i>src__data.src__streaming_history</i> table, and record the operation in the <i>src__data.src__upload_log</i> table. The task would only load a file with the same file name once only by checking the logs in the <i>src__data.src__upload_log</i> table. <b>Users should keep the format of the JSON files to prevent any potential error!</b>
<br><br>
This task would utilize the functions available in <i>extract.py</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.
<br><br>
<b>If the files do not saved under a username folder, the data in those files would not be extracted and uploaded to database!</b>

#### Task 7: Remove Duplicated Records
Task 7 would remove duplicated records if there are two files with two different file names but with identical content, the pipeline would detect the duplicated rows and remove it. The pipeline would not update the data between Last 12 Months records and full records. For example, if there are two identical stream history loaded from <i>a.json</i> and <i>b.json</i>, <i>src__data.src__streaming_history</i> table should contain both records:

```
## Record found in src__data.src__streaming_history
# Loaded from a.json,
{
    "endTime" : "2023-04-29 06:37",
    "artistName" : "Hikaru Utada",
    "trackName" : "Automatic",
    "msPlayed" : 328600
}
...
# Loaded from b.json
{
    "endTime" : "2023-04-29 06:37",
    "artistName" : "Hikaru Utada",
    "trackName" : "Automatic",
    "msPlayed" : 328600
}

## Record found in stg__streaming_history__unique
{
    "endTime" : "2023-04-29 06:37",
    "artistName" : "Hikaru Utada",
    "trackName" : "Automatic",
    "msPlayed" : 328600
}
## ** All records are available in tabular format instead
```
Task 7 would detect that and remove the duplicated history, and insert one into <i>stg__streaming_history__unique</i>. However, Task 7 only distinguish with the same record type source. If we have one record of full data format, and two records of last 12 months format, Task 7 would insert one record of full data format and one record of last 12 month format.
<br><br>
This task would utilize the functions available in <i>distinct_stream_history.sql</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.



#### Task 8: Update Records in Central Storage Schema
Task 8 update records of last 12 months format in <i>ctr__streaming_history</i> if new records in full data format found in the <i>stg__streaming_history__unique</i>. If so, the task would delete the last 12 months data in <i>ctr__streaming_history</i> and insert the new full data format to <i>ctr__streaming_history</i>. After that, the task would insert a log of such operation into <i>ctr__sql_streaming_history_record_type</i>. <b>This task only update the records available in <i>ctr__streaming_history</i> from last 12 months format to full data format</b>.
<br><br>
This task would utilize the functions available in <i>transform_stream_history_upgrade.sql</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.


#### Task 9: Insert Records to Central Storage Schema
Task 9 insert new records available in the <i>stg__streaming_history__unique</i> to <i>ctr__streaming_history</i>, regardsless of the format, and update the log of operation to <i>ctr__sql_streaming_history_record_type</i>.
<br><br>
This task would utilize the functions available in <i>transform_stream_history_direct_insert.sql</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.

#### Task 10: Distribute Data to Output Stage
Task 10 conduct a full load (Delete existing data and load all data into the output stage table) from <i>ctr__streaming_history</i> to <i>out__streaming_history</i> to expose the data to the dashboards.
<br><br>
<b>Incremental load is currently not available, such function will be replaced with full load in the future release</b>.
<br><br>
This task would utilize the functions available in <i>out_stream_history.sql</i> saved under the [ELT](../../../Setup/dags/ELT) folder under the [dags](../../../Setup/dags) folder.

#### Task 11: Update Records in Central Flatfile Storage Schema
Not available. This task will be updated in the future release.

#### Task 12: Insert Records in the Central Flatfile Storage Schema
Not available. This task will be updated in the future release.

#### Task 13: Remove Caches in GoodData after Output Table has Refreshed
Not available. This task will be updated in the future release.