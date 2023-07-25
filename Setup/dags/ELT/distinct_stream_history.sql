with unique_history as (
	select *
	from ( select *,	
		row_number() over(partition by date_trunc('minute',ts::timestamp), username,
			 master_metadata_track_name
			 -- record_type = full or last_12_mos, so full should come first
			 -- last_12_mos only round to minute, full round to ms
			order by record_type) as row_id
		from src__data.src__streaming_history
	) as i
	where i.row_id = 1
) insert into stg__data.stg__streaming_history__unique
(ts,
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
incognito_mode
) select ts,
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
incognito_mode
from unique_history
where concat(username,ts,master_metadata_track_name) not in (
	select concat(username,ts,master_metadata_track_name) from stg__data.stg__streaming_history__unique
) 
;