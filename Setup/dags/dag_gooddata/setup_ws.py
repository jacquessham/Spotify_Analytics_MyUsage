import json
import request
from airflow.providers.postgres.hooks.postgres import PostgresHook
from connection_ids import psql_conn



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
	query = """select username, workspace from out__data.out__ws_lcm"""
	cursor.execute(query)
	return cursor.fetchall()[1:]

def create_child_ws():
	conn, cursor = declare_conn()
	df_lcm = get_username_list(cursor)
	gd_endpoint = 'http://gooddata-cn-ce:3000/api/v1/entities/workspaces'
	headers = get_headers()
	f = open('child_ws_template.txt','r')
	child_ws_template = f.read()
	for username, workspace_id in df_lcm:
		curr_payload = child_ws_template.replace('\\{\\{username}\\}\\}',
				username).replace('\\{\\{workspace_id}\\}\\}',workspace_id)
		r = requests.post(gd_endpoint, data=curr_payload, headers=headers)
		print(f"Response on creating {workspace_id}: {r.status_cod}")


def apply_ws_filter():
	conn, cursor = declare_conn()
	df_lcm = get_username_list(cursor)
	gd_endpoint = 'http://gooddata-cn-ce:3000/api/v1/entities/workspaces'
	headers = get_headers()
	f = open('ws_filter_template.txt','r')
	ws_filter_payload = json.load(f)
	for username, workspace_id in df_lcm:
		curr_filter = ws_filter(username, workspace_id)
		ws_filter_payload['workspaceDataFilters'][0]\
			['workspaceDataFilterSettings'].append(curr_filter)
	r = requests.post(gd_endpoint, data=curr_payload, headers=headers)
	print(f"Response on applying data filter: {r.status_cod}")

