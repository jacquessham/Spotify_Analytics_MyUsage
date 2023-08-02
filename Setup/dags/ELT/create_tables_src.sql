-- All source data go to this schema
create schema if not exists src__data;

-- Table for steaming history
create table if not exists src__data.src__streaming_history(
	ts varchar(512),
	username varchar(512),
	platform varchar(512),
	ms_played varchar(512),
	conn_country varchar(512),
	ip_addr_decrypted varchar(512),
	user_agent_decrypted varchar(512),
	master_metadata_track_name varchar(512),
	master_metadata_album_artist_name varchar(512),
	master_metadata_album_album_name varchar(512),
	spotify_track_uri varchar(512),
	episode_name varchar(512),
	episode_show_name varchar(512),
	spotify_episode_uri varchar(512),
	reason_start varchar(512),
	reason_end varchar(512),
	shuffle varchar(512),
	skipped varchar(512),
	offline varchar(512),
	offline_timestamp varchar(512),
	incognito_mode varchar(512),
	filename varchar(512),
	upload_time date,
	record_type varchar(512)
);

-- Table for Logging to keep track what files were fed
create table if not exists src__data.src__upload_log(
	upload_date date, 
	filename varchar(512), 
	source_username varchar(512), -- If last 12 months data, only found in directory
	source_directory varchar(512),
	record_type varchar(512) -- Full/Last 12 month data
);

