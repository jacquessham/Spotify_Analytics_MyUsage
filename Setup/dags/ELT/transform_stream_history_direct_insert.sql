-- Insert rows newly uploaded
-- Create temp table to save the list to update
create temp table rows2add(
	new_row_id varchar(512)
);

insert into rows2add(
	new_row_id
) select distinct row_id
from stg__data.stg__streaming_history__unique
where row_id in (
	select distinct i.row_id 
	from
	(select *,
		row_number() over (partition by concat(username,date_trunc('minute',ts::timestamp),master_metadata_track_name)
			order by record_type) as type_rank -- full should come first
	from stg__data.stg__streaming_history__unique
	) as i
	where i.type_rank = 1
) and row_id not in (
	select row_id from ctr__data.ctr__streaming_history
)
;


insert into ctr__data.ctr__streaming_history(
row_id,
ts_timestamp,
ts_epoch,
ts_date,
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
) select
row_id,
date_trunc('minute',ts::timestamp)::timestamp,
date_part('epoch', date_trunc('minute',ts::timestamp)),
date_trunc('minute',ts::timestamp)::date,
username,
platform,
ms_played::int,
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
shuffle::boolean,
skipped::boolean,
offline::boolean,
left(offline_timestamp,10)::int,
incognito_mode::boolean
from stg__data.stg__streaming_history__unique
where row_id in (
	select new_row_id from rows2add
)
;



-- Update Log
insert into ctr__data.ctr__sql_streaming_history_record_type(
	record_id,
	row_id,
	record_type,
	last_updated_date
) select floor(random()*pow(10,10))::varchar, 
	l.row_id, 
	l.record_type, 
	now()::date
from stg__data.stg__streaming_history__unique as l
join rows2add as r
on l.row_id = r.new_row_id
;

