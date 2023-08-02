delete from out__data.out__streaming_history;


insert into out__data.out__streaming_history(
	row_id,
	ts_timestamp,
	ts_epoch,
	ts_date,
	username,
	platform,
	ms_played,
	conn_country,
	track_name,
	artist_name,
	album_name,
	reason_start,
	reason_end,
	shuffle,
	skipped,
	offline,
	offline_timestamp
) select row_id,
	ts_timestamp,
	ts_epoch,
	ts_date,
	username,
	platform,
	ms_played,
	conn_country,
	master_metadata_track_name,
	master_metadata_album_artist_name,
	master_metadata_album_album_name,
	reason_start,
	reason_end,
	shuffle,
	skipped,
	offline,
	offline_timestamp
from ctr__data.ctr__streaming_history
where episode_name is null and episode_show_name is null and 
	spotify_episode_uri is null and
	row_id not in (
		select row_id from out__data.out__streaming_history
		)
; -- Only want song data, fitler out podcast data
