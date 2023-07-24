-- Output Stage Schema for Dashboards
create schema if not exists out__data;


create table if not exists out__data.out__streaming_history(
	row_id varchar(512) primary key,
	ts_timestamp timestamp,
	ts_epoch varchar(512),
	ts_date date,
	username varchar(512),
	platform varchar(512),
	ms_played int,
	conn_country varchar(512),
	track_name varchar(512),
	artist_name varchar(512),
	album_name varchar(512),
	reason_start varchar(512),
	reason_end varchar(512),
	shuffle boolean,
	skipped boolean,
	offline boolean,
	offline_timestamp timestamp
);