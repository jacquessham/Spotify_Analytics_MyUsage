# Release Note

## Version 0.1.0 (Beta)
* Documentation is ready
* Fix bug on ELT Pipeline when creating primary keys
* Change start day of the ELT DAG to last monday to avoid duplicated jobs while having more than one trigger with the same DAG

## Version 0.0.4 (Alpha)
* Update ELT Pipeline to convert the columns Reason Start and Reason End in Output Stage tables from abbreviation code to Readable values.
* Add features DAG on creating shell scripts to create children workspace in GoodData based on usernames

## Version 0.0.3 (Alpha)
* ELT Pipelines print logs on what files the pipeline is reading or saving
* New DAG on setting up GoodData (Database connection, setup master workspace) i s now available.

## Version 0.0.2 (Alpha)
* Add dashboard <i>2. Songs</i> to GoodData master workspace
* Fix <i>extract.py</i> bug, now require user to create username folder in the <i>Data/last_12mos</i> folder to upload data
* ELT Pipeline is now fully function. Task 11-13 are available in <i>elt.py</i>: Transformed data is now also saved in the Central Storage Data Flatfile folder.

## Version 0.0.1 (Alpha)
* Functioning ELT Pipeline with core features (Task 1-10 in <i>elt.py</i>)
* Functioning GoodData with all required metrics and 1 overview dashboard <i>1. Overview</i> in master workspace
