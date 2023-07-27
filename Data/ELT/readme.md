# ELT
Coming soon...


## Overview
<img src=elt_step1.png>

## Source Schema
The purpose of this schema simply ingest data into the database without doing any transformation.
<br><br>
Coming soon...

## Stage Schema
The purpose of this schema is to remove the duplicated records in the source schema.
<br><br>
The goal of the staging tables is to ensure duplicated rows are removed if duplicated files uploaded. For example, if there are two files with two different file names but with identical content, the pipeline would detect the duplicated rows and remove it. The pipeline would not update the data between Last 12 Months records and full records, it would be taken care by the data pipeline between staging tables and central storage tables.
<br><br>
Coming soon...

## Central Storage Schema
The purpose of this schema is save all the records to preserve the single source of truth. Any record in this schema is the truth of the dataset with no duplication nor corruption.
<br><br>
Coming soon...

## Central Storage Flatfile Storage
The Storage is to setup for future use if there is any initiative for use cases beyond analytics use.
<br><br>
Coming soon...

## Output Stage for Dashboards
This schema is set to expose to dashboard applications.
<br><br>
Coming soon...