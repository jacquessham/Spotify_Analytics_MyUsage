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
	offline_timestamp timestamp,
	incognito_mode boolean
);