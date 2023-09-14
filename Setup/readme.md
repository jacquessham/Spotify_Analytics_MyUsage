# Setup
You may follow the instruction here to set up the whole solution after your data is available. You would first run Docker to initiate all the components, including data pipeline, database, and the visualization tools.

## Step 1: Docker Setup
Docker hosts the environment network and set up all the components in the solutions, here are the tools Docker would host:
<ul>
	<li>Airflow</li>
	<li>Postgres</li>
	<li>GoodData</li>
	<li>Customized Docker Image (For Dash Server)</li>
</ul>

First, execute the following code on command line to trigger Docker to run:

```
# Step 1.1: Initiate Airflow
docker-compose up -d airflow-init

# Step 1.2: Initiate the whole docker network
docker-compose up -d
```

Note on folder: 
<ul>
	<li><i>Data</i> folder is mapped to the <i>Data</i> folder in the local setting, and where you can upload data and load into the database.</li>
	<li><i>dags</i> folder is mapped to the <i>dags</i> folder in the local setting, and where you can upload elt scripts.</li>
	<li><i>gooddata</i> folder is mapped to the <i>gooddata</i> folder in the local setting, and where you can save the metadata for GoodData configuration</li>
	<li><i>Central_Storage_Data</i> folder is mapped to the <i>Central_Storage_Data</i> in the local setting, it is where the <i>Central Storage Flatfile Storage</i> locates</li>
</ul>

## Step 2: Upload Data
Once you have the data obtained from Spotify, you may upload the data in the [Data folder](../Data), where you may find the <i>full_data</i> and <i>last_12mos</i> folders, and the instruction how to upload the data.

## Step 3: Airflow Setup for Data Pipeline
Once Airflow is ready, you may go to <i>http://localhost:8080/</i> and log into Airflow. The username and password are both <i>airflow</i> if you did not change it in the <i>docker-compose.yaml</i> file. There are two DAGs have been setup for the applications: <b>elt</b> and <b>lcm_gooddata</b>. <b>elt</b> is the DAGs for the ELT pipeline, which is prepared in the <i>dags</i> folder already. Enable this workflow and the workflow should automatically execute since the start date is backdated to July 2023. You may find more details about the DAG scripts in the [ELT Pipeline](../Data/ELT/Pipeline) folder.

## Step 4: GoodData Setup
After GoodData is ready, log in with the default login password for the community edition, which can be found in GoodData's <a href="https://www.gooddata.com/developers/cloud-native/doc/2.4/deploy-and-install/community-edition/">documentation</a> page. After you have login successfully, you may execute the following code on the command line to connect the database, and set up the master workspace if you want to set up GoodData manually:

```
# Create new master workspace
sh gooddata/create_master_ws.sh

# Connect GoodData with Postgres
sh gooddata/create_connection.sh

# Set up the master workspace
sh gooddata/setup_master_ws.sh
```

<br><br>
The <i>gooddata</i> folder is also where the pre-defined payload stored, ie, the workspace layout,<i>spotify_streaming_history_master_layout.json</i> , to set up the dashboard automatically with pre-defined metadata.
<br><br>
After you have created and set up the master workspace, you may create children workspaces for the users (The environment for each individual user). Go back to Airflow and enable <b>elt</b> DAG which will generate the necessary payloads to make API calls to create new children workspaces and data filter for distributing the data according to data permission. The <b>lcm_gooddata</b> DAG will identify the usernames available in the database and generate the payload of each API call. The <b>lcm_gooddata</b> DAG should automatically execute since the start date is backdated to July 2023 and saved the payloads in the <i>gooddata</i> folder. Change your command line directory to the <i>gooddata</i> folder and execute the following shell script that will automatically create all children workspaces for each user:

```
# Change directory
cd gooddata

# Create new children workspace
sh create_all_children_ws.sh
```


<br>
Special Note: <b>Currently the script do not check existing workspaces and create all children workspace each time you execute the script. Expect errors if the workspace exists! An update will be made in the coming version!</b>
<br><br>
Note 1: GoodData.CN community edition do not have a good user management system, currently it is not possible to create user within GoodData.CN community edition and set workspace permission. 
<br><br>

Note 2: You may find the details of the shell scripts related to GoodData.CN setup in the [gooddata](/gooddata) folder.

## Dash Server Setup
<b>Coming in the future update!</b>