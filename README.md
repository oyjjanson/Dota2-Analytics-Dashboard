# Dota2-Analytics-Dashboard
Dashboard of an end-to-end pipeline from OpenDota API to streamlit.
- Developed an automated ETL pipeline integrating OpenDota API data using Python and Pandas.
- Implemented Apache Airflow DAGs to orchestrate scheduled data extraction, transformation and database updates.
- Containerised workflow orchestration using Docker.
- Integrated PostgreSQL (Neon) with Streamlit to deliver interactive analytical dashboards.
- Implemented data validation, error handling and automated database updates.

## Project Overview
This project requests data from the OpenDota API, cleans, validates and loads it onto PostgreSQL hosted on Neon.
Dashboard is created using streamlit and hosted onto streamlit cloud.

End result of such a site is contained within this repository which shows heroes statistics in a table and a cluster diagram.

<img width="1879" height="840" alt="dashboard-statistics" src="https://github.com/user-attachments/assets/80585d48-166b-4a87-8ada-00ab1a107649" />
First tab on navigation bar.

<img width="1898" height="819" alt="dashboard-cluster" src="https://github.com/user-attachments/assets/5cfe158c-d16d-41b7-84dd-664ae46fb362" />
Second tab on navigation bar.

Accommodates different weeks in drop down bar on right.

## System Architecture Diagram
<img width="437" height="494" alt="System Architecure2" src="https://github.com/user-attachments/assets/1da5cfac-f03e-47bd-bf70-c12315008b75" />

## Technology Used
Python/Pandas

PostgreSQL/Neon

Apache airflow

Docker

Streamlit

## Features

### Feature #1: Processed ~3 million match records
Able to obtain ~3 million match records using Python and Pandas to obtain statistics such as, hero appearance, win rates and performance for analytical reporting. Reformatted data for database storage to take as little space as possible while providing enough data for analysis.

### Feature #2: Implemented 3 DAGs for common uses
<img width="942" height="503" alt="DAGs" src="https://github.com/user-attachments/assets/a0f217f4-4523-4664-ab53-e22033f2f295" />

1. DAG: clear_database

This DAG is mostly ran manually to clear out my entire PostgreSQL database. This DAG runs a truncate on the existing table as to prevent the reset of permissions on my readonly and writeonly roles, while giving me a blank table so insert data into.

<img width="580" height="159" alt="DAG_main" src="https://github.com/user-attachments/assets/0979477d-7bae-4f53-b9c0-616190196614" />

2. Dag: main

This DAG directs the main body of code consisting of 3 pythonOperators:
  1. Checks if there is a week's worth of data to process (Project aims to get a weekly round-up type analysis)
  2. Checks database for latest timestamp and changes config file to ready next ETL
  3. Runs ETL python code based on set timestamp in config file, cleans and validates, uploads it to PostgreSQL. (Main_task)

<img width="582" height="148" alt="DAG_start_4_mon" src="https://github.com/user-attachments/assets/fed2fc38-eb8c-4d18-905e-c4ca3062d819" />

3. DAG: start_4_mon

This DAG should be followed after clear_database, contains 2 pythonOperators:
  1. Gets a list of UNIX timestamps of 4 Sundays back, returns the last Sunday and writes it into the config file.
  2. Runs ETL python code based on set timestamp in config file, cleans and validates, uploads it to PostgreSQL. (Main_task)

### Feature #3: Retries on get request failure
<img width="479" height="560" alt="Retry get request" src="https://github.com/user-attachments/assets/6dfd59f6-dd27-45ac-90b4-06ad97df9b11" />

Get requests to the OpenDota API fails on occasion, while get request code stays consistent. 

I have programmed a recursion function that has 2 main features that reduces its overall impact:
  1. Recursion function that retries if get request fails (automatically retries with same code as issue is likely API based)
  2. Able to start loading from last collected batch of data ("save point" introduced, able to continue where for loop left off on error)






