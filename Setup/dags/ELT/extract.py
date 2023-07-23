import os
import json
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def declare_conn():
    psql_hook = PostgresHook(postgres_conn_id='postgres_airflow_docker_spotify')
    conn = psql_hook.get_conn()
    cursor = conn.cursor()
    conn.autocommit = True
    return conn, cursor

def get_allfiles(cursor, root_dir):
    cursor.execute(
        """ select distinct filename from src__data.src__upload_log;"""
        )
    files_uploaded = [row[0] for row in cursor.fetchall()]

    files_dir = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file not in files_uploaded:
                files_dir.append(os.path.join(root, file))
    return files_dir

def build_insert_query(data_type, record, filename):
    query = f"insert into src__data.src__steaming_history"
    if data_type == 'full':
        # Make sure keys order are consistent
        cols = [k for k in record]
        # Build query and include all cols
        query += f"("
        for col in cols:
            query += f"{str(col)}, "
        # Filename and upload_time are not in the file
        query += f"filename, upload_time, record_type) values ("
        # Pass value
        for col in cols:
            query += f"'{str(record[col])}'', "
        query += f"'{filename}'', {datetime.now()}, '{data_type}')"
    elif data_type == 'last_12mos':
        query += (f"(ts, master_metadata_album_artist_name,"
                f"master_metadata_track_name,ms_played,record_type) values"
                f"('{record['endTime']}', '{record['artistName']}',"
                f"'{record['trackName']}','{record['msPlayed']}',"
                f"'{data_type}')")
    else:
        query = ''

    return query

def read_files(conn, data_type, list_files):
    for filename in list_files:
        with open(filename) as j:
            records = json.load(j)
        for record in records:
            insert_query = build_insert_query(data_type, record, 
                filename.split('/')[-1])
            cursor.execute(insert_query)

def extract_full():
    root_dir = 'Data/full_data'
    conn, cursor = declare_conn()
    list_files = get_allfiles(cursor, root_dir)
    read_files(conn, 'full', list_files)
    conn.close()

def extract_last12mos():
    root_dir = 'Data/last_12mos'
    conn, cursor = declare_conn()
    list_files = get_allfiles(cursor, root_dir)
    read_files(conn, 'last_12mos', list_files)
    conn.close()