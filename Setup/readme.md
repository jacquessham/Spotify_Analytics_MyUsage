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

(Explain the folders)<br>
Note: <i>Data</i> folder is mapped to the <i>Data</i> folder on the local setting.

## Upload Data
Coming soon...

## Airflow Setup
Coming soon...<br>
(dags folder should have all scripts already)<br>
(Refer to another page for DAGs documentation)<br>
(gooddata folder should have all payload too)<br>

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
Coming soon...

## Dash Server Setup
<b>Coming in the next update!</b>