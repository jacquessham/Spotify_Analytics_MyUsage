# GoodData.CN Shell Scripts Folder
This is the folder where the shell scripts and supporting files are stored. You can find the scripts related to:
<ul>
	<li>Creating connection</li>
	<li>Creating master workspace</li>
	<li>Creating children workspaces</li>
	<li>Setting up or deleting data filter</li>
	<li>Removing cache</li>
</ul>

## Creating Connection
You may execute <i>creating_connection.sh</i> like below to establish the connection between the postgres and GoodData.CN, as well as the following tasks, including Scan and register the layout of the physical model of Postgres with GoodData. 

```
# Creating Connection, all steps are taken care of
sh create_connection.sh
```

## Creating Master Workspace
The first step is to create an environment with the dashbord layout as a parent environment for children enviornment to inherited from within GoodData.CN. In order to do so, you may execute <i>create_master_ws.sh</i> to create a master workspace. Then, you may import the pre-defined dashboard layout to this workspace by executing <i>setup_master_ws.sh</i> which would import the layout saved as <i>spotify_streaming_history_master_layout.json</i> to the master workspace. Once the layout is imported, the dashboards in the master workspace are ready to access. 

```
# Create Master Workspace
sh create_master_ws.sh

# Import layout to Master Workspace
sh setup_master_ws.sh
```

## Create Children Workspace
In order to separate data to different environment, you may create children workspaces for each user where only the data belong to such user would be displayed on the dashboards within its workspace. The DAG <i>lcm_gooddata</i> would automatically generate the payloads. Once the payloads are ready, execute <i>create_all_children_ws.sh</i> which would create all children workspaces for the users and create a data filter to distribute the data to the appropriated workspaces.

```
# Create all Children Workspace and data filter
sh create_all_children_ws.sh
```

## Delete Data Filter
You may execute <i>reset_ws_filter.sh</i> to delete data filter. It is not recommended to delete data filter if any child workspace is created.

## Remove Cache
Everytime the data is ingested to Postgres, you should remove cache (Refresh data) in GoodData.CN by executing <i>refresh_output_tables.sh</i>.

```
# Remove cache
sh refresh_output_tables.sh
```