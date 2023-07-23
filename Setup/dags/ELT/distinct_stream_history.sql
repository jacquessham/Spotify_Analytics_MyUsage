with unique_history as (
	select *
	from ( select *,	
		row_num() over(partition by ts, username order by record_type) as row_id
	) as i -- record_type = full or last_12_mos, so full should come first
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
;