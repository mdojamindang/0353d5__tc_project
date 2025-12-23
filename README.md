# Restaurant Project  

This is an lightweight analytics dashboard that uses **DuckDB** as the backing database and **Streamlit** for interactive visualization.

## Overview
The purpose of this exercise is to use a randomly generated restaurant information and create an analytics dashboard the focuses on a few key components. 

## Project Structure
The project is stores in a repository labeled using `<hex_code>__<company_initials>_project` format. It is separated into multiple subfolders to show clear boundaries between different parts of the components. 

0353d5__tc_project/
├── code/
│ └── app.py 
├── config/
│ └── ingest_data.py 
├── data/
│ └── data.csv 
├── database/
│ └── data.duckdb 
├── dev/
├── requirements.txt
└── README.md

 - **`code/`**  
  Contains the application code and other future codes.

- **`config/`**  
  Contains the python script to ingest data into **DuckDB** database

- **`data/`**  
  Contains the one time csv file of the restaurant data. Replacing the csv file and running the script inside config will update the data inside the **DuckDB** database

- **`database/`**  
  Contains the output database after running the script inside the config subfolder

- **`dev/`**  
  Contains the jupyter notebook used for testing the output of the analytics dashboard

- **`READ.md`**  
  Provides the project documentation

- **`requirement.txt`**  
  Provides the packages needed to make the project work



 ## Tech Stack

- **Python** – primary programming language
- **Jupyter Notebook** – exploratory analysis and query validation during development
- **DuckDB** – embedded analytical database for SQL-based querying
- **Streamlit** – interactive dashboard framework
- **Pandas** – lightweight data manipulation

## Database Design

The project uses DuckDB as a local analytical database to store and query the dataset.
Data is ingested once into a DuckDB database file and accessed using SQL queries. Data can be reingested using the ingest_data.py file inside the config folder. The dashboard performs multiple targeted aggregation queries rather than loading entire tables into memory.
DuckDB was chosen for its fast analytical performance, simple setup, and strong SQL support.
	
### Future Improvements
- Migrate from a local, file-based database to a centrally hosted database to support multi-user access and larger data volumes.
- Introduce incremental data ingestion for streaming sources (e.g. Kafka), including:
  - Historical backfills
  - Deduplication logic
  - Overwrite or upsert strategies for categorical and slowly changing data
- Organize data into well-defined schemas and analytical marts to separate raw data, transformed data, and reporting-ready tables.


## Dashboard Design 

The project uses Streamlit to present metrics and visualizations derived from the database.
Instead of loading the entire dataset into memory, the dashboard relies on multiple focused SQL aggregation queries executed directly in the database. This approach would leverage the database’s strengths for analytical workloads. Python is used to perform additional data processing when needed. In this project, Python and Pandas was used for remapping the dataframe columns to human readable names.

### Future Improvements
- Improve UI and layout for better usability and readability as the number of views grows.
- Enhance deployment by containerizing the application and deploying it to a managed environment to support consistent builds and easier scaling.

## Setup & Usage

### Prerequisites
- Python 3.9+
- pip
- git

### Installation
1. Clone the repository and install dependencies:
2. Run this script in the root folder to install 

```bash
pip install -r requirements.txt
```

### Reingestion of Data
1. Update the data in the `Data.csv` file located in the `data/` folder
   Schema:
	restaurant_names - string
	food_names - string
	first_name - string
	food_cost - float

2. Run this script to update the local database
```bash
python3 config/ingest_data.py
```

### Run Locally
1. Run this script to see the locally hosted dashboard
```bash
streamlit run code/app.py
```
