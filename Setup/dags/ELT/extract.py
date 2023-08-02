import os
import json
from datetime import datetime
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
        """ select distinct filename from src__data.src__upload_log"""
        )
    files_uploaded = [row[0] for row in cursor.fetchall()]
    print(files_uploaded)

    files_dir = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file not in files_uploaded and '.json' in file:
                files_dir.append(os.path.join(root, file))
    print(files_dir)
    return files_dir

def build_insert_query(data_type, record, filename, username=None):
    query = f"insert into src__data.src__streaming_history"
    if data_type == 'full':
        # Make sure keys order are consistent
        cols = [k for k in record]
        # Build query and include all cols
        query += f"("
        for col in cols:
            if record[col] is not None:
                query += f"{str(col)}, "
        # Filename and upload_time are not in the file
        query += f"filename, upload_time, record_type) values ("
        # Pass value
        for col in cols:
            if record[col] is not None:
                value = str(record[col]).replace("'","''")
                query += f"'{value}', "
        query += f"'{filename}', '{datetime.now().date()}'::date, '{data_type}')"
    elif data_type == 'last_12mos':
        artist = record['artistName'].replace("'","''")
        trackName = record['trackName'].replace("'","''")
        query += (f"(ts, master_metadata_album_artist_name,"
                f"master_metadata_track_name, ms_played, record_type,"
                f"username) values"
                f"('{record['endTime']}', '{artist}',"
                f"'{trackName}','{record['msPlayed']}',"
                f"'{data_type}', '{username}')")
    else:
        query = ''
    return query

def read_files(cursor, data_type, list_files):
    for filename in list_files:
        with open(filename, encoding='utf-8') as j:
            records = json.load(j)
        for record in records:
            if data_type == 'full':
                insert_query = build_insert_query(data_type, record, 
                    filename.split('/')[-1])
            elif data_type == 'last_12mos':
                source_name = filename.split('/')
                insert_query = build_insert_query(data_type, record, 
                    source_name[-1], source_name[-2])
            cursor.execute(insert_query)

def update_log(cursor, data_type, list_files):
    for file in list_files:
        source_name = file.split('/')
        source_directory = '/'.join(source_name[:-1])
        filename = source_name[-1]
        if data_type == 'full':            
            query = """
                insert into src__data.src__upload_log(
                    upload_date, filename,
                    source_directory, record_type
                ) values (
            """
            query += f"'{datetime.now().date()}'::date, '{filename}',"
            query += f"'{source_directory}', '{data_type}')"


        elif data_type == 'last_12mos':
            source_username = source_name[-2]
            query = """
                insert into src__data.src__upload_log(
                    upload_date, filename, source_username,
                    source_directory, record_type
                ) values (
            """
            query += f"'{datetime.now().date()}'::date, '{filename}',"
            query += f"'{source_username}',"
            query += f"'{source_directory}', '{data_type}')"

        else:
            query = ''

        cursor.execute(query)

def extract_full():
    root_dir = 'Data/full_data'
    conn, cursor = declare_conn()
    list_files = get_allfiles(cursor, root_dir)
    read_files(cursor, 'full', list_files)
    update_log(cursor, 'full', list_files)
    conn.close()

def extract_last12mos():
    root_dir = 'Data/last_12mos'
    conn, cursor = declare_conn()
    list_files = get_allfiles(cursor, root_dir)
    read_files(cursor, 'last_12mos', list_files)
    update_log(cursor, 'last_12mos', list_files)
    conn.close()
