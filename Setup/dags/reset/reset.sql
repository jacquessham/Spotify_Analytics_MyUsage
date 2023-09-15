-- Source Schema
delete from src__data.src__streaming_history;
delete from src__data.src__upload_log;

-- Staging Schema
delete from stg__data.stg__streaming_history__unique;

-- Storing Schema
delete from ctr__data.ctr__streaming_history;
delete from ctr__data.ctr__sql_streaming_history_record_type;
delete from ctr__data.ctr__json_streaming_history_record_type;

-- Output Schema
delete from out__data.out__streaming_history;