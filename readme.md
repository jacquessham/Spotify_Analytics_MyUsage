# Spotify Analytics on my Usage
As every Spotify user receive a Year-end story and playlist from Spotify about his annual listening habit and insights, it may be more interesting to have a dashboard for yourself to check out anytime of the year with a broader dimension. It is also important to store your precious data generated by yourself on your end. Therefore, our goal of this project is to build a mini data lake and interactive dashboard to do analytics for your listening habit on Spotify.
<br><br>
The application is <b>currently in development</b>, <b>v0.1.0</b> (Beta).
<br><br>
The solution is available for testing purpose, you may run the solution and test the dashboard in GoodData. But it is still in development and this is not the final version.


## Goals and Requirements
The goals are to develop the ETL pipeline to systematically store the listening records obtained from Spotify in a centralized data lake and use this backend to power the dashboards or machine learning infrastructure.
<br><br>
You may find more detailed requirements in the [Goals and Requirements](/Goals) folder.

### Who Would Use This?
Anyone who is interested to do analytics for your listening habit on Spotify! However, there are two expected personas: <b>Administrators</b> and <b>Causal Users</b>. Administrators are the one who responsible for seting up and maintaining the backend of the whole applications; causal users are simply the users who browses and use the dashboards.

## Data
The listening records are obtained from Spotify directly. You may request the data through: Spotify User Profile -> Privacy Settings -> Download Your Data. You may request your Account Data, including last 12 months of listening records, in about 5 days. You may also request your Spotify lifetime records, although it may take up to 30 days.
<br><br>
Due to privacy, my full listening record will not be posted in this repository but saved in my local machine. However, the pipeline is designed to ingest dynamically which is not user-specify. Therefore, you may still able to utilize the pipeline for your own use.
<br><br>
You may find more details about the data from Spotify, data lake structure, or anything about data in the [Data](/Data) folder, the Dataset Structure from Spotify in the [Data Structure](/Data/Structure) folder , or the ELT Overview in the [ELT](/Data/ELT) folder. However, the scripts of the pipeline are available in the [DAGs](/Setup/dags) folder under the [Setup](/Setup) folder.
<br><br>
Currently, we are only support the attributes offered by Spotify. The data provided from Spotify does not have sufficient attribute data on songs' metadata. It may be followed up in the future.

## Tools
We will be using the following tools:

<ul>
	<li>Docker</li>
	<li>Postgres</li>
	<li>Airflow</li>
	<li>Python 
		<ul>
			<li>Pandas</li>
		</ul>
	</li>
	<li>Plotly/Dash</li>
	<li>GoodData</li>
</ul>

## Databases and Flatfile Storage
The applications are expected run in Docker Containers and utilize open-source resouce only. The database choice is Postgres and local folders for flatfile storage.
<br><br>
You may find more details about the data from Spotify, data lake structure, or anything about data in the [Data](/Data) folder.

## Dashboard
You may access the dashboard hosted by GoodData.CN at <i>http://localhost:3000</i> after GoodData is configured and ran. The following is the default dashboard layout:

<img src=gd_example.png>

<br><br>
You may visit the [Gallery](/Instruction/Gallery) folder to look at the dashboard screenshots.

## Setup
If you are an administrator to initiate the backend and dashboard, you would first initiate the Docker network defined in the Setup folder and it would automatically set up for you. Once Airflow is ready, you are expected to supply the data set and maintain the data pipeline. And finally, you would also setup and maintain the backend of GoodData.CN. You may find more details on how to setup the application with Docker in the [Setup](/Setup) folder.

## Instructions for Causal Users
Once the application is setup, causal users may access the dashboard hosted by GoodData.CN at <i>http://localhost:3000</i> after GoodData is configured. You may find the Instructions on how to use the GoodData Dashboard in the [Instruction](/Instruction) folder.

## Future Development
<ul>
	<li>v0.1.0 (beta) - Functional Backend and functional GoodData Dashboards for Basics and KPIs report</li>
	<li>v0.2.0 (beta) - Plotly Dash on Trend Analysis and Anomaly Detection</li>
	<li>v1.0.0 - Official Launch</li>
	<li>v1.1.0 - Playlist Analysis via Plotly Dash</li>
</ul>


<br><br>
More details in the [Release Notes](/Release_Notes)

Note:
<ul>
	<li>Playtlist Analysis discover low play rate songs and make recommendation to remove from playlist</li>
</ul>

