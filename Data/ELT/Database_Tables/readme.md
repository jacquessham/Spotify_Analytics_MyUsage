# Database Tables
This section is the documentation of the database tables with details.

## Source Schema
Ingest data into the database without doing any transformation. The schema name is <b>src__data</b> and the table names prefix are <b>scr__</b>.

### src__streaming_history
Upload all the streaming history records and save in this table. It does not prevent any type of duplicated records, except no records from the same file be uploaded more than once.

<ul>
	<li></li>
</ul>


### src__upload_log
Save the records of file upload history to prevent the same file with the same file name be uploaded twice. However, it does not prevent the data pipeline to upload the files with the same content.

<ul>
	<li></li>
</ul>

## Staging Schema
Remove the duplicated records in the source schema, ie, the same content from more than one file source. However, it does not distinguish the difference bewtween last 12 months data and full data. It is taken care on the transformation between <i>staging schema</i> and <i>central storage schema</i> The schema name is <b>stg__data</b> and the table names prefix are <b>stg__</b>.

### stg__streaming_history__unique
Remove the duplicated streaming history records, but keep the same record if the record has both last 12 months data format and full data format.

<ul>
	<li></li>
</ul>


## Central Storage Schema
Save all the records to preserve the single source of truth. The schema name is <b>ctr__data</b> and the table names prefix are <b>ctr__</b>.

### ctr__streaming_history
Save all streaming records. The table would have no duplicated records, last 12 mos records would be removed when full records are available. All the columns are defined in the corresponding data type, ie, timestamp, date, or numeric.

<ul>
	<li></li>
</ul>

### ctr__sql_streaming_history_record_type
Save the metadata of each record row, use to keep track whether record is last 12 months data or full data. This tables helps the pipeline to upgrade the record to full record in the <i>ctr__streaming_history</i> when it is available.


<ul>
	<li></li>
</ul>

### ctr__json_streaming_history_record_type
Save the metadata of each record row, use to keep track whether record is last 12 months data or full data. This tables helps the pipeline to upgrade the record to full record in the <i>Central Storage Flatfile Storage</i> when it is available.


<ul>
	<li></li>
</ul>

## Central Storage Flatfile Storage
Flatfile folder to storage data in JSON format (Only storage not hosted in Postgres). The records are the same with the <i>Central Storage Schema</i>
<br><br>
Coming soon...

## Output Stage for Dashboards
The schema for data to be exposed to dashboard applications for both GoodData and Dash Server.

### out__streaming_history
Table for exposing the streaming history for GoodData. 
<br><br>
Coming soon...