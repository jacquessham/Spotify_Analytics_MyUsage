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

-- Staging Schema for Cleanse the data from Source Schema before going to Storage Schema
create schema if not exists stg__data;

-- Table to merge full and last 12 mos data and prevent duplication
create table if not exists stg__data.stg__streaming_history__unique(
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
	incognito_mode varchar(512)
);

-- Storage Schema: The Central Storage for all data, serve as single source of truth
create schema if not exists ctr__data;


create table if not exists ctr__data.ctr__streaming_history(
	row_id varchar(512) primary key,
	ts_timestamp timestamp,
	ts_date date,
	username varchar(512),
	platform varchar(512),
	ms_played int,
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
	shuffle boolean,
	skipped boolean,
	offline boolean,
	offline_timestamp timestamp,
	incognito_mode boolean
);
