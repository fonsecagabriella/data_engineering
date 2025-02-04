# Homework - Week 03

## INGESTING THE DATA

1. You will need a service account key (retrieved from GCS)
2. Run the script `load_yellow_data.py` (but first change the name of your bucket and location of your key)
    2.1 You run the script by using the terminal `python load_yellow_data.py``
3. Check in your bucket in Google Cloud if the six `parquet`files are there.

## BIG QUERY SETUP

**Create an external table using the Yellow Taxi Trip Records.**

In the BigQuery Console, create a new SQL query and run the following:

```
CREATE OR REPLACE EXTERNAL TABLE `your_project_id.your_dataset_name.yellow_tripdata_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket-name/path/to/parquet_files/*.parquet']
);

```

✅ Now you can query the data from GCS without storing it in BigQuery.

**Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).**
In the BigQuery Console, create a new SQL query and run the following:


*FOR A REGULAR TABLE*
````
CREATE OR REPLACE TABLE `your_project_id.your_dataset_name.yellow_tripdata_2024`
AS
SELECT * FROM `your_project_id.your_dataset_name.yellow_tripdata_external`;

````

*FOR A MATERIALIZED TABLE*
````
CREATE MATERIALIZED VIEW `your_project_id.your_dataset_name.yellow_tripdata_2024_mv`
AS
SELECT * FROM `your_project_id.your_dataset_name.yellow_tripdata_external`;

````

# Notes 📝

## Difference Between Regular and Materialized Tables in BigQuery

| Feature | Regular Table | Materialized Table (View) |
|---|---|---|
| Storage | Stores full data | Stores precomputed query results |
| Performance | Slower, queries scan the table | Faster, queries use precomputed results |
| Refresh | Must be manually updated | Automatically updates when source changes |
| Use Case | Storing raw or cleaned data | Improving query speed for frequent queries |
| Cost | Charges for storage & queries | Charges for storage but **reduces** query costs |

### Regular Table
A **regular table** in BigQuery is a standard table where data is stored in a structured format. It is queried directly from storage, meaning every time you run a query, BigQuery scans the data in the table to generate results.

- Data is stored persistently.
- Queries read from the table every time they are executed.
- No precomputed results; queries can take longer if scanning large datasets.
- Good for frequently updated datasets.

```sql
CREATE OR REPLACE TABLE my_dataset.regular_table AS
SELECT * FROM my_dataset.source_table;
```

## Materialized Table
A **materialized** table is a precomputed table that stores the results of a query. Unlike regular tables, materialized tables improve query performance by reducing the amount of data that needs to be scanned.

- Stores precomputed query results.
- Improves performance for repetitive queries.
- Requires periodic refresh to stay up-to-date.
- Reduces query costs by avoiding frequent full table scans.

```sql
CREATE MATERIALIZED VIEW my_dataset.materialized_table AS
SELECT customer_id, SUM(total_amount) AS total_spent
FROM my_dataset.transactions
GROUP BY customer_id;

````



# Homework questions 🏡

**1: What is count of records for the 2024 Yellow Taxi Data?**
>> 20,332,093

*Explanation:*
After you create the table yellow_tripdata_2024 above, you just have to go to `details`and look at `Storage Info`

**2. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.**
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

>> 0 MB for the External Table and 155.12 MB for the Materialized Table



*Explanation:*
- You don't need to run the query, just create it, and check the on the green mark on the top how much it will cost you (just hover over the checkmark ✅)

This is the query for the Table:

```sql

SELECT DISTINCT COUNT(PULocationID) FROM `your_project_id.your_dataset_name.yellow_tripdata_2024``

```

This is the query for the External table:
````sql
SELECT DISTINCT COUNT(PULocationID) FROM `your_project_id.your_dataset_name.yellow_tripdata_external`
````

**3 Write a query to retrieve the PULocationID form the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?**






