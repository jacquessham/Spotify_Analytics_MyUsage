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
