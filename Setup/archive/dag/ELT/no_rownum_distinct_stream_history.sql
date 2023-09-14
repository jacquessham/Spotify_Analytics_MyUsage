with unique_history as (
	select distinct
		date_trunc('minute',ts::timestamp) ts_trunc, username, platform, ms_played,
		conn_country, ip_addr_decrypted, user_agent_decrypted,
		master_metadata_track_name, master_metadata_album_artist_name,
		master_metadata_album_album_name, spotify_track_uri, episode_name,
		episode_show_name, spotify_episode_uri, reason_start, reason_end, shuffle,
		skipped, offline, offline_timestamp, incognito_mode, record_type
	from src__data.src__streaming_history
) insert into stg__data.stg__streaming_history__unique(
	row_id,
	ts,
	username,
	platform,
	ms_played,
	conn_country,
	ip_addr_decrypted,
	user_agent_decrypted,
	master_metadata_track_name,
	master_metadata_album_artist_name,
	master_metadata_album_album_name,
	spotify_track_uri,
	episode_name,
	episode_show_name,
	spotify_episode_uri,
	reason_start,
	reason_end,
	shuffle,
	skipped,
	offline,
	offline_timestamp,
	incognito_mode,
	record_type
) select concat(username,ts_trunc,master_metadata_track_name,'_',record_type) as row_id,
ts_trunc,
username,
platform,
ms_played,
conn_country,
ip_addr_decrypted,
user_agent_decrypted,
master_metadata_track_name,
master_metadata_album_artist_name,
master_metadata_album_album_name,
spotify_track_uri,
episode_name,
episode_show_name,
spotify_episode_uri,
reason_start,
reason_end,
shuffle,
skipped,
offline,
offline_timestamp,
incognito_mode, 
record_type
from unique_history
where concat(username,ts_trunc,master_metadata_track_name,'_',record_type) not in (
	select row_id from stg__data.stg__streaming_history__unique
)
;