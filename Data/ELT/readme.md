# ELT
The ELT section explains the overview of the database and how the ELT data pipeline works. We will be using Postgres as the database, and utilize Airflow to manage the data pipeline along with Python and SQL scripts.


## Overview
<img src=elt_step1.png>

<br><br>
The whole solution will use Postgres as the database, and <b>spotify</b> is the database name the solution will be using. The coming sections are the overview of all the schema within the <b>spotify</b> database. For the documentation of the table and data pipeline details, you may find more details in the [Database tables](/Database_Tables) folder and the [Data Pipeline](/Pipeline).

## Source Schema
The purpose of this schema simply ingest data into the database without doing any transformation. The data pipeline may prevent the same file with the same file name be uploaded multiple times, but it does not prevent files with same content with different file names.

## Staging Schema
The purpose of this schema is to remove the duplicated records in the source schema.
<br><br>
The goal of the staging tables is to ensure duplicated rows are removed if duplicated files uploaded. As mentioned in the <i>source schema</i> section, if there are two files with two different file names but with identical content, the pipeline would detect the duplicated rows and remove it. The pipeline would not update the data between Last 12 Months records and full records, it would be taken care by the data pipeline between staging tables and central storage tables.

## Central Storage Schema
The purpose of this schema is save all the records to preserve the single source of truth. Any record in this schema is the truth of the dataset with no duplication nor corruption.
<br><br>
Another purpose of this schema is to try its best to update the Last 12 Months data to Full Data: The data pipeline would periodically check the <i>staging schema</i> and update the Last 12 Months Data to Full Data if it is available.

## Central Storage Flatfile Storage
The Storage is to setup for future use if there is any initiative for use cases beyond analytics use.
<br><br>
The data pipeline would convert the records in the <i>central storage schema</i> to JSON files in this storage folder and update the records from Last 12 Months data to Full data once it is available.

## Output Stage for Dashboards
This schema is set to expose to dashboard applications for both GoodData and Dash Server.
