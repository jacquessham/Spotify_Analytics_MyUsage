import json
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook
from connection_ids import psql_conn
import os



def declare_conn():
    psql_hook = PostgresHook(postgres_conn_id=psql_conn)
    conn = psql_hook.get_conn()
    cursor = conn.cursor()
    conn.autocommit = True
    return conn, cursor

def get_headers():
		headers = {
			"Authorization": "Bearer YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz",
			"Content-Type": "application/vnd.gooddata.api+json",
			"Accept": "application/vnd.gooddata.api+json"
		}
		return headers

def ws_filter(username, workspace_id):
		return {
	          "id": f"{username}_streaminghistory_filter",
	          "title": f"Workspace Filter for {username}",
	          "filterValues": [
	            f"{username}"
	          ],
	          "workspace": {
	            "id": f"{workspace_id}",
	            "type": "workspace"
	          }
	        }

def get_username_list(cursor):
		query = """select username, workspace_id from out__data.out__ws_lcm"""
		cursor.execute(query)
		return cursor.fetchall()[0:]

def create_child_ws():
		conn, cursor = declare_conn()
		df_lcm = get_username_list(cursor)
		print(df_lcm)
		gd_endpoint = 'http://gooddata-cn-spotify:3000/api/v1/entities/workspaces'
		headers = get_headers()
		f = open('/opt/airflow/dags/dag_gooddata/child_ws_template.txt','r')
		child_ws_template = f.read()
		for username, workspace_id in df_lcm:
				print(f"We are creating workspace {workspace_id} for {username}")
				curr_payload = json.loads(child_ws_template)
				curr_payload['data']['id'] = workspace_id
				workspace_name = f"Spotify Streaming History Analysis ({username})"
				curr_payload['data']['attributes']['name'] = workspace_name
				print(f"Requesting to {gd_endpoint}")
				print('Here is the payload:')
				print(curr_payload)
				r = requests.post(gd_endpoint, data=curr_payload, headers=headers)
				print(f"Response on creating {workspace_id}: {r.status_code}")


def apply_ws_filter():
		conn, cursor = declare_conn()
		df_lcm = get_username_list(cursor)
		gd_endpoint = 'http://gooddata-cn-spotify:3000/api/v1/entities/workspaces'
		headers = get_headers()
		f = open('/opt/airflow/dags/dag_gooddata/ws_filter_template.json','r')
		ws_filter_payload = json.load(f)
		for username, workspace_id in df_lcm:
			curr_filter = ws_filter(username, workspace_id)
			ws_filter_payload['workspaceDataFilters'][0]\
				['workspaceDataFilterSettings'].append(curr_filter)
		r = requests.put(gd_endpoint, data=ws_filter_payload, headers=headers)
		print(f"Response on applying data filter: {r.status_code}")

