# Data
Listening Records Data is coming from Spotify upon request: Either 1 year interval or since the beginning.
<br><br>
Currently, we are only support the attributes offered by Spotify. The data provided from Spotify does not have sufficient attribute data on songs' metadata. It may be followed up in the future.

## How to Request Data from Spotify
The listening records are obtained from Spotify directly. You may request the data through: Spotify User Profile -> Privacy Settings -> Download Your Data. You may request your Account Data, including last 12 months of listening records, in about 5 days. You may also request your Spotify lifetime records, although it may take up to 30 days.
<br><br>
Due to privacy, my full listening record will not be posted in this repository but saved in my local machine. However, the pipeline is designed to ingest dynamically which is not user-specify. Therefore, you may still able to utilize the pipeline for your own use.

## Type of Data
### Listening Records
The listen record data is obtained from Spotify that is the record of what songs and podcast a user has listened in Spotify within an interval of time, ie, last 12 months, or lifetime. It is the core fact data we will be utilized in this project. You may find more details about the dataset in the [Structures of Source Data](/Structure) folder.

## ETL Pipeline
The proposed ETL pipeline looks like this:
<img src=etl_pipeline.png>

<br>
You may find more details in the [ELT](/ELT) folder.
<br><br>
Coming soon...

### How to Upload Data?
There are two folder at this directory for you to upload data: <b>full_data</b> and <b>last_12mos</b>.
<br><br>
If you are uploading the full data (The dataset takes 30 days to request), you may simply save the JSON files to the <b>full_data</b> folder.
<br><br>
If you are uploading the Last 12 Months data (The dataset takes 3-5 days to request), you would need to first create a folder named with the username. Then, you may save the JSON files to the individual folder. If you are going with this approach, you are expected to saved the records in the individual username folder.
<br><br>
Coming soon...