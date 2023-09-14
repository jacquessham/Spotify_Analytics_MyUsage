with distinct_usernames as (
	select distinct username from out__data.out__streaming_history
)
insert into out__data.out__ws_lcm(
	username, workspace_id
)
select username, concat('spotify_streaming_history_', username)
from distinct_usernames
where username not in (select username from out__data.out__ws_lcm)
;