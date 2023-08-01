-- Storage Schema: The Central Storage for all data, serve as single source of truth
create schema if not exists ctr__data;


create table if not exists ctr__data.ctr__streaming_history(
	row_id varchar(512) primary key,
	ts_timestamp timestamp,
	ts_epoch varchar(512),
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
	offline_timestamp int,
	incognito_mode boolean
);

create table if not exists ctr__data.ctr__sql_streaming_history_record_type(
	record_id varchar(512) primary key,
	row_id varchar(512),
	record_type varchar(512),
	last_updated_date date
);

create table if not exists ctr__data.ctr__json_streaming_history_record_type(
	record_id varchar(512) primary key,
	row_id varchar(512),
	record_type varchar(512),
	filename varchar(512),
	file_directory varchar(512),
	last_updated_date date
);