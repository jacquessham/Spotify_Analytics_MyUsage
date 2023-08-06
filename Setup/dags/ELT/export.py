import os
import json
from random import randint
from datetime import datetime
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def declare_conn():
    psql_hook = PostgresHook(postgres_conn_id='postgres_airflow_docker_spotify')
    conn = psql_hook.get_conn()
    cursor = conn.cursor()
    conn.autocommit = True
    return conn, cursor

def get_filename(root_dir, username, year_month):
    # Check if username folder exists
    if not os.path.exists(f"{root_dir}/{username}"):
        os.makedirs(f"{root_dir}/{username}")

    # Check if year folder within thi username folder exists
    curr_year = year_month.split('_')[0]
    if not os.path.exists(f"{root_dir}/{username}/{curr_year}"):
        os.makedirs(f"{root_dir}/{username}/{curr_year}")
    # Done creating folder and safe to save
    return (f"{root_dir}/{username}/{username}_{year_month}.json",
            f"{username}_{year_month}.json")

def update_log(cursor, row_id, record_type, filename, file_fullpath):
    query = f"""
        insert into ctr__data.ctr__json_streaming_history_record_type(
            record_id,
            row_id,
            record_type,
            filename,
            file_directory,
            last_updated_date
        ) values
        ('{str(randint(10**10, 10**11))}', '{row_id.replace("'","''")}', 
        '{record_type}', '{filename}', '{file_fullpath}',
        '{datetime.now().date()}')
    """
    cursor.execute(query)


def export_direct():
    conn, cursor = declare_conn()

    # Obtain the column names
    cursor.execute(
    """
    select column_name from information_schema.columns 
    where table_name = 'ctr__streaming_history';
    """
    )
    ctr_streaming_history_columns = [row[0] for row in cursor.fetchall()]
    ctr_streaming_history_columns.append('year_month')

    # Obtain the the whole dataframe need to export
    cursor.execute(
        """ 
        select r.*, concat(date_part('year',r.ts_timestamp::date),'_',
            date_part('month',r.ts_timestamp::date)) as year_month
        from ctr__data.ctr__sql_streaming_history_record_type as l
        join ctr__data.ctr__streaming_history as r
        on l.row_id = r.row_id
        where l.row_id not in (
            select distinct row_id 
            from ctr__data.ctr__json_streaming_history_record_type
        )""")

    df = pd.DataFrame(cursor.fetchall(), columns=ctr_streaming_history_columns)
    df[list(df)] = df[list(df)].astype(str) # Convert all columns to string
    
    # Obtain all usernames
    cursor.execute(
        """
        select distinct username from ctr__data.ctr__streaming_history
        """)

    usernames = [row[0] for row in cursor.fetchall()]

    # Partition by username first
    for username in usernames:
        df_curruser = df[df['username']==username]
        year_months = df_curruser['year_month'].unique()

        # Partition by year_month within username folder
        for year_month in year_months:
            df_json = {}
            df_curr = df_curruser[df_curruser['year_month']==year_month]

            # Convert each row to a dictionary
            for index, row in df_curr.iterrows():
                curr_row = {}

                # Only save the column that is not null
                for col in ctr_streaming_history_columns:
                    if row[col] != 'None' and row[col] != 'nan' and \
                            col not in ['row_id','year_month']:
                        # Fix float value appear in offline_timestamp 
                        if col == 'offline_timestamp':
                            curr_row[col] = str(int(float(row[col])))
                        else:
                            curr_row[col] = row[col]
                # Use row_id as key in the JSON file
                df_json[row['row_id']] = curr_row
            # Ensure required folder is created
            file_fullpath, filename = get_filename('Central_Storage_Data', username, 
                            year_month)
            # Save dataset
            # If the file exist already, add new records
            if os.path.exists(file_fullpath):
                print(file_fullpath)
                print(os.path.exists(file_fullpath))
                with open(file_fullpath,'r') as f1:
                    df_exist = json.load(f1)
                    df_exist.update(df_json)
                with open(file_fullpath,'w') as f2:
                    json.dump(df_exist, f2, indent=4, ensure_ascii=False)
            # If the file is not existed, create a new one
            else:
                with open(file_fullpath, 'w') as f:
                    json.dump(df_json, f, indent=4, ensure_ascii=False)

            # Update the logs in the 
            # ctr__data.ctr__json_streaming_history_record_type table
            for row_id in df_curr['row_id'].tolist():
                if row_id.endswith('full'):
                    record_type = 'full'
                else:
                    record_type = 'last_12mos'
                update_log(cursor, row_id, record_type, filename, file_fullpath)



        
