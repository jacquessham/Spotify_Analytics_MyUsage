-- Take care of existing last_12mos data that needs to upgrade to full data
-- Create temp table to save the list to update
create temp table row_diff(
	old_row_id varchar(512),
	new_row_id varchar(512)
);

-- Get the list of last_12mos data
with last12_mos_mod_rows as (
	select *
	from (
		select *, rank() over (partition by split_part(row_id,'_',1)
			order by last_updated_date desc, record_type) as update_rank_desc
		from
		ctr__data.ctr__sql_streaming_history_record_type
	) as i
	where i.record_type = 'last_12mos' and i.update_rank_desc = 1 and
	i.row_id not in (
		select distinct row_id 
		from ctr__data.ctr__sql_streaming_history_record_type
		where record_type = 'full'
	)
),
-- Find the rows that has new full data, and append to the temp table
record_diff as (
	select l.row_id as old_row_id,
		concat(r.username,date_trunc('minute',r.ts::timestamp),r.master_metadata_track_name,'_',r.record_type)
			as new_row_id
	from
	(select split_part(row_id,'_',1) as simple_row_id, row_id
	from last12_mos_mod_rows) as l
	join 
	( select *, concat(username,date_trunc('minute',ts::timestamp),master_metadata_track_name)
		as simple_row_id
	from stg__data.stg__streaming_history__unique
	where record_type = 'full'
	) as r
	on l.simple_row_id = r.simple_row_id
) insert into row_diff(
	old_row_id, new_row_id
)select old_row_id, new_row_id
from record_diff
;

-- delete the old rows to prevent duplicated
delete from ctr__data.ctr__streaming_history
where row_id in (select old_row_id from row_diff)
;

-- Insert the updated rows from staging table
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
offline_timestamp::int,
incognito_mode::boolean
from stg__data.stg__streaming_history__unique
where row_id in (
	select new_row_id from row_diff
)
;

-- Update Log
insert into ctr__data.ctr__sql_streaming_history_record_type(
	record_id,
	row_id,
	record_type,
	last_updated_date
) select floor(random()*pow(10,10))::varchar, 
	new_row_id, 'full', now()::date
from row_diff
;

drop table row_diff;
