import duckdb
import pandas as pd 

conn = duckdb.connect("database/data.duckdb")
df = pd.read_csv("data/data.csv")

conn.execute("CREATE OR REPLACE TABLE TABLE_CHECK_DATA AS SELECT * FROM df")

conn.close()