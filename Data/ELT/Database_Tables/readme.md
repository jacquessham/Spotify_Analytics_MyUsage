# Database Tables
This section is the documentation of the database tables with details.

## Source Schema
Ingest data into the database without doing any transformation. The schema name is <b>src__data</b> and the table names prefix are <b>scr__</b>.

### src__streaming_history
Upload all the streaming history records and save in this table. It does not prevent any type of duplicated records, except no records from the same file be uploaded more than once.
<br><br>
Columns:
<ul>
	<li>ts - varchar(512): UTC time when songs finished</li>
	<li>username - varchar(512): Username</li>
	<li>platform - varchar(512): What device platform the songs played</li>
	<li>ms_played - varchar(512): Duration the song played in ms</li>
	<li>conn_country - varchar(512): Physical location when song played</li>
	<li>ip_addr_decrypted - varchar(512): IP address when the song played</li>
	<li>user_agent_decrypted - varchar(512):</li>
	<li>master_metadata_track_name - varchar(512): Song name</li>
	<li>master_metadata_album_artist_name - varchar(512): Artist name</li>
	<li>master_metadata_album_album_name - varchar(512): Album name</li>
	<li>spotify_track_uri - varchar(512): uri of the song used internally in Spotify</li>
	<li>episode_name - varchar(512): Podcast episode name</li>
	<li>episode_show_name - varchar(512): Podcast show name</li>
	<li>spotify_episode_uri - varchar(512):  uri of the podcast used internally in Spotify</li>
	<li>reason_start - varchar(512): Song start reason</li>
	<li>reason_end - varchar(512): Song end reason</li>
	<li>shuffle - varchar(512): Whether the song was shuffle when played</li>
	<li>skipped - varchar(512): Indicate whether the song was skipped</li>
	<li>offline - varchar(512): Indicate whether the song was played offline </li>
	<li>offline_timestamp - varchar(512): If the song played offline, the timestamp when the song ended. It should be the same as ts</li>
	<li>incognito_mode - varchar(512): Indicate whether the song was played in incognito mode</li>
	<li>filename - varchar(512): State the source file name</li>
	<li>upload_time - date: The upload time when this record was uploaded to the database</li>
	<li>record_type - varchar(512): Indicate whether the format of the record is full record or last 12 month</li>
</ul>


### src__upload_log
Save the records of file upload history to prevent the same file with the same file name be uploaded twice. However, it does not prevent the data pipeline to upload the files with the same content.
<br><br>
Columns:
<ul>
	<li>upload_date - date: The file upload date</li>
	<li>filename - varchar: The file name</li>
	<li>source_username - varchar: The record of which the username folder originated from. If the file contains full records, it would be null.</li>
	<li>source_directory - varchar: The directory of the file originated from</li>
	<li>record_type - varchar: Indicate whether the file is full data or last 12 months data format</li>
</ul>

## Staging Schema
Remove the duplicated records in the source schema, ie, the same content from more than one file source. However, it does not distinguish the difference bewtween last 12 months data and full data. It is taken care on the transformation between <i>staging schema</i> and <i>central storage schema</i> The schema name is <b>stg__data</b> and the table names prefix are <b>stg__</b>.

### stg__streaming_history__unique
Remove the duplicated streaming history records, but keep the same record if the record has both last 12 months data format and full data format.
<br><br>
Columns:
<ul>
	<li>row_id - varchar(512) <b>Primary Key</b>: Primary Key of the record. It is a combination of ts in epoch (truncated to minute, due to last 12 months data was truncated to minute), username, and song name. </li>
	<li>ts - varchar(512): UTC time when songs finished</li>
	<li>username - varchar(512): Username</li>
	<li>platform - varchar(512): What device platform the songs played</li>
	<li>ms_played - varchar(512): Duration the song played in ms</li>
	<li>conn_country - varchar(512): Physical location when song played</li>
	<li>ip_addr_decrypted - varchar(512): IP address when the song played</li>
	<li>user_agent_decrypted - varchar(512):</li>
	<li>master_metadata_track_name - varchar(512): Song name</li>
	<li>master_metadata_album_artist_name - varchar(512): Artist name</li>
	<li>master_metadata_album_album_name - varchar(512): Album name</li>
	<li>spotify_track_uri - varchar(512): uri of the song used internally in Spotify</li>
	<li>episode_name - varchar(512): Podcast episode name</li>
	<li>episode_show_name - varchar(512): Podcast show name</li>
	<li>spotify_episode_uri - varchar(512):  uri of the podcast used internally in Spotify</li>
	<li>reason_start - varchar(512): Song start reason</li>
	<li>reason_end - varchar(512): Song end reason</li>
	<li>shuffle - varchar(512): Whether the song was shuffle when played</li>
	<li>skipped - varchar(512): Indicate whether the song was skipped</li>
	<li>offline - varchar(512): Indicate whether the song was played offline </li>
	<li>offline_timestamp - varchar(512): If the song played offline, the timestamp when the song ended. It should be the same as ts</li>
	<li>incognito_mode - varchar(512): Indicate whether the song was played in incognito mode</li>
	<li>record_type - varchar(512): Indicate whether the format of the record is full record or last 12 month</li>
</ul>


## Central Storage Schema
Save all the records to preserve the single source of truth. The schema name is <b>ctr__data</b> and the table names prefix are <b>ctr__</b>.

### ctr__streaming_history
Save all streaming records. The table would have no duplicated records, last 12 mos records would be removed when full records are available. All the columns are defined in the corresponding data type, ie, timestamp, date, or numeric.
<br><br>
Columns:
<ul>
	<li>row_id - varchar(512) <b>Primary Key</b>: Primary Key of the record. It is a combination of ts in epoch (truncated to minute, due to last 12 months data was truncated to minute), username, and song name. </li>
	<li>ts - timestamp: UTC time when songs finished</li>
	<li>ts_epoch - varchar(512): UTC time when songs finished in epoch</li>
	<li>ts_date - date : UTC date  when songs finished</li>
	<li>username - varchar(512): Username</li>
	<li>platform - varchar(512): What device platform the songs played</li>
	<li>ms_played - int: Duration the song played in ms</li>
	<li>conn_country - varchar(512): Physical location when song played</li>
	<li>ip_addr_decrypted - varchar(512): IP address when the song played</li>
	<li>user_agent_decrypted - varchar(512):</li>
	<li>master_metadata_track_name - varchar(512): Song name</li>
	<li>master_metadata_album_artist_name - varchar(512): Artist name</li>
	<li>master_metadata_album_album_name - varchar(512): Album name</li>
	<li>spotify_track_uri - varchar(512): uri of the song used internally in Spotify</li>
	<li>episode_name - varchar(512): Podcast episode name</li>
	<li>episode_show_name - varchar(512): Podcast show name</li>
	<li>spotify_episode_uri - varchar(512):  uri of the podcast used internally in Spotify</li>
	<li>reason_start - varchar(512): Song start reason</li>
	<li>reason_end - varchar(512): Song end reason</li>
	<li>shuffle - boolean: Whether the song was shuffle when played</li>
	<li>skipped - boolean: Indicate whether the song was skipped</li>
	<li>offline - boolean: Indicate whether the song was played offline </li>
	<li>offline_timestamp - int: If the song played offline, the timestamp when the song ended. It should be the same as ts</li>
	<li>incognito_mode - boolean: Indicate whether the song was played in incognito mode</li>
	<li>record_type - varchar(512): Indicate whether the format of the record is full record or last 12 month</li>
</ul>

### ctr__sql_streaming_history_record_type
Save the metadata of each record row, use to keep track whether record is last 12 months data or full data. This tables helps the pipeline to upgrade the record to full record in the <i>ctr__streaming_history</i> when it is available. The records in this table are added incrementally to preserve the history of records updated in the <i>ctr__streaming_history</i> table.

<br><br>
Columns:
<ul>
	<li>record_id - varchar(512) <b>Primary Key</b>: Random number for a unique number for primary key</li>
	<li>row_id - varchar(512): The row id of the record in the <i>ctr__streaming_history</i> table</li>
	<li>record_type - varchar(512): Indicate whether the format of the record is full record or last 12 month</li>
	<li>last_updated_date: The update date of this record</li>
</ul>

### ctr__json_streaming_history_record_type
Save the metadata of each record row, use to keep track whether record is last 12 months data or full data. This tables helps the pipeline to upgrade the record to full record in the <i>Central Storage Flatfile Storage</i> when it is available.

<br><br>
Columns:
<ul>
	<li>record_id - varchar(512) <b>Primary Key</b>: Random number for a unique number for primary key</li>
	<li>row_id - varchar(512): The row id of the record in the <i>ctr__streaming_history</i> table</li>
	<li>record_type - varchar(512): Indicate whether the format of the record is full record or last 12 month</li>
	<li>filename - varchar(512): State the file name where this row has been saved to</li>
	<li>file_directory - varchar(512): State the directory where the file is saved</li>
	<li>last_updated_date: The update date of this record</li>
</ul>

## Central Storage Flatfile Storage
Flatfile folder to storage data in JSON format (Only storage not hosted in Postgres). The records are the same with the <i>Central Storage Schema</i>
<br><br>
The Flatfile folder is saved under [Central Storage Data](../../../Central_Storage_Data). The JSON files are partition by <b>username</b>, <b>year</b>, and <b>month</b>, and the filename format is <i>username_year_month.json</i>.

## Output Stage for Dashboards
The schema for data to be exposed to dashboard applications for both GoodData and Dash Server.

### out__streaming_history
Table for exposing the streaming history for GoodData. This table would not contain any podcast streaming record.
<br><br>
Columns:
<ul>
	<li>row_id - varchar(512) <b>Primary Key</b>: Primary Key of the record. It is a combination of ts in epoch (truncated to minute, due to last 12 months data was truncated to minute), username, and song name. </li>
	<li>ts - timestamp: UTC time when songs finished</li>
	<li>ts_epoch - varchar(512): UTC time when songs finished in epoch</li>
	<li>ts_date - date : UTC date  when songs finished</li>
	<li>username - varchar(512): Username</li>
	<li>platform - varchar(512): What device platform the songs played</li>
	<li>ms_played - int: Duration the song played in ms</li>
	<li>conn_country - varchar(512): Physical location when song played</li>
	<li>track_name - varchar(512): Song name</li>
	<li>artist_name - varchar(512): Artist name</li>
	<li>album_name - varchar(512): Album name</li>
	<li>reason_start - varchar(512): Song start reason</li>
	<li>reason_end - varchar(512): Song end reason</li>
	<li>shuffle - boolean: Whether the song was shuffle when played</li>
	<li>skipped - boolean: Indicate whether the song was skipped</li>
	<li>offline - boolean: Indicate whether the song was played offline </li>
	<li>offline_timestamp - int: If the song played offline, the timestamp when the song ended. It should be the same as ts</li>
</ul>