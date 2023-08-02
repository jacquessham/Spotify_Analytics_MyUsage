# Setup
You may follow the instruction here to set up the whole solution after your data is available. You would first run Docker to initiate all the components, including data pipeline, database, and the visualization tools.

## Docker Setup
Docker hosts the environment network and set up all the components in the solutions, here are the tools Docker would host:
<ul>
	<li>Airflow</li>
	<li>Postgres</li>
	<li>GoodData</li>
	<li>Customized Docker Image (For Dash Server)</li>
</ul>

First, execute the following code on command line to trigger Docker to run:

```
# Step 1: Initiate Airflow
docker-compose -d airflow-init

# Step 2: Initiate the whole docker network
docker-compose -d up
```

Note on folder: 
<ul>
	<li><i>Data</i> folder is mapped to the <i>Data</i> folder in the local setting, and where you can upload data and load into the database.</li>
	<li><i>dags</i> folder is mapped to the <i>dags</i> folder in the local setting, and where you can upload elt scripts.</li>
	<li><i>gooddata</i> folder is mapped to the <i>gooddata</i> folder in the local setting, and where you can save the metadata for GoodData configuration</li>
	<li><i>Central_Storage_Data</i> folder is mapped to the <i>Central_Storage_Data</i> in the local setting, it is where the <i>Central Storage Flatfile Storage</i> locates</li>
</ul>

## Upload Data
Once you have the data obtained from Spotify, you may upload the data in the [Data folder](../Data), where you may find the <i>full_data</i> and <i>last_12mos</i> folders, and the instruction how to upload the data.

## Airflow Setup
Once Airflow is ready, you may go to <i>http://localhost:8080/</i> and log into Airflow. The username and password are both <i>airflow</i> if you did not change it in the <i>docker-compose.yaml</i> file. The DAGs for the ELT pipeline is prepared in the <i>dags</i> folder already, and the workflow should automatically execute since the start date is backdated to July 2023. You may find more details about the DAG scripts in the [ELT Pipeline](../Data/ELT/Pipeline) folder.

## GoodData Setup
After GoodData is ready, log in with the default login password for the community edition, which can be found in GoodData's <a href="https://www.gooddata.com/developers/cloud-native/doc/2.4/deploy-and-install/community-edition/">documentation</a> page. After you have login successfully, you may execute the following code on the command line to connect the database, set up the master workspace:

```
# Create new master workspace
sh gooddata/create_master_ws.sh

# Connect GoodData with Postgres
sh gooddata/create_connection.sh

# Set up the master workspace
sh gooddata/setup_master_ws.sh
```

<br><br>
The <i>gooddata</i> folder is also where the pre-defined payload stored, ie, the workspace layout to set up the dashboard automatically with pre-defined metadata.

## Dash Server Setup
<b>Coming in the next update!</b>