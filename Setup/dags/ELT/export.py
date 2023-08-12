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

def get_fulldata_rows(cursor, row_ids):
    # Obtain the column names
    cursor.execute(
    """
    select column_name from information_schema.columns 
    where table_name = 'ctr__streaming_history';
    """
    )
    ctr_streaming_history_columns = [row[0] for row in cursor.fetchall()]

    # Obtain the fulldata rows
    query = """
        select * from ctr__data.ctr__streaming_history
        where row_id in (
        """
    n = len(row_ids)
    for i in range(n):
        curr_id = row_ids[i].replace("'","''")
        print(curr_id)
        query += f"'{str(curr_id)}'"
        if i != n-1:
            query += f", "
        else:
            query += f")"
    print(query)
    cursor.execute(query)

    df = pd.DataFrame(cursor.fetchall(), columns=ctr_streaming_history_columns)
    df[list(df)] = df[list(df)].astype(str) # Convert all columns to string

    return df, ctr_streaming_history_columns


def export_update():
    conn, cursor = declare_conn()

    # Obtain the rows need to update
    cursor.execute(
        """
        select l.row_id as new_row_id, r.row_id as old_row_id, 
                r.filename, r.file_directory
        from
        (select distinct row_id, record_type
        from ctr__data.ctr__sql_streaming_history_record_type
        where record_type = 'full') as l
        join 
        (select distinct i.row_id, i.filename, i.file_directory,
            i.latest_type as record_type
        from
            (select row_id, record_type, filename, file_directory,
                first_value(record_type) over(partition by row_id 
                    order by record_type, last_updated_date desc) 
                    as latest_type
            from ctr__data.ctr__json_streaming_history_record_type
        ) as i) as r
        on replace(l.row_id, '_full', '') = 
            replace(r.row_id, '_last_12mos', '') and 
            l.record_type <> r.record_type
        order by 1
        """)

    df_rowids = pd.DataFrame(cursor.fetchall(), 
                        columns=['new_row_id','old_row_id',
                        'filename','file_directory'])

    # Since the files have been partitioned, loop over each file
    # and update all rows within the same file
    # drop_duplicates() will create error if df is empty
    if df_rowids[['filename','file_directory']].shape[0] > 0:
        files_and_directory = df_rowids[['filename','file_directory']].drop_duplicates()
        files_and_directory = files_and_directory.itertuples(index=False)
    else:
        files_and_directory = []

    for curr_filename, curr_file_directory in files_and_directory:
        # Find the row_ids need to update
        df_temp = df_rowids[df_rowids['filename']==curr_filename]
        curr_ids = df_temp['new_row_id'].tolist()

        # Load the file
        with open(curr_file_directory,'r') as f1:
            df_ctr_dict = json.load(f1)

        # Obtain the full data and replace in the file
        df_fulldata, ctr_streaming_history_columns = get_fulldata_rows(cursor, curr_ids)

        # Dispose old records and replace the new records
        for index, row in df_fulldata.iterrows():
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
            
            # Use new row_id as key in the JSON file
            df_ctr_dict[row['row_id']] = curr_row

            # Remove old row_id
            df_ctr_dict.pop(row['row_id'].replace('_full','_last_12mos'))


        # Save the file
        with open(curr_file_directory,'w') as f2:
            json.dump(df_ctr_dict, f2, indent=4, ensure_ascii=False)


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



        
