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



---


# Homework questions 🏡

**01. What is count of records for the 2024 Yellow Taxi Data?**
>> 20,332,093

*Explanation:*
After you create the table yellow_tripdata_2024 above, you just have to go to `details`and look at `Storage Info`

---

**02. Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.** **What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

>> 0 MB for the External Table and 155.12 MB for the Materialized Table



*Explanation:*
- You don't need to run the query, just create it, and check the on the green mark on the top how much it will cost you (just hover over the checkmark ✅)

This is the query for the Table:

````sql

SELECT COUNT(DISTINCT PULocationID) FROM `your_project_id.your_dataset_name.yellow_tripdata_2024
````


This is the query for the External table:

````sql
SELECT COUNT(DISTINCT PULocationID) FROM `your_project_id.your_dataset_name.yellow_tripdata_external`
````

---


**03. Write a query to retrieve the PULocationID form the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?**

>> BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

*Explanation*: 
***Why is this correct?***
BigQuery stores data in a columnar format, meaning that each column is stored separately. *When you run a query, BigQuery only scans the specific columns you request.*

- If you query only `PULocationID`, BigQuery scans just that column.
- If you query both `PULocationID` and `DOLocationID`, BigQuery has to scan both columns, increasing the amount of data read.

Since BigQuery charges based on the amount of data processed, adding more columns increases the estimated number of bytes scanned.

***Why are the other options incorrect?***
❌ *"BigQuery duplicates data across multiple storage partitions..."* → Incorrect. 
BigQuery does not duplicate entire tables across partitions like that. Partitions store data efficiently, but each column is still stored separately.

❌ *"BigQuery automatically caches the first queried column..."* → Incorrect. 
BigQuery does not cache column data in this way. The estimated bytes scanned is based on the amount of data physically read from storage.

❌ *"BigQuery performs an implicit join operation..."* → Incorrect. 
Selecting multiple columns does not perform a join. A join only happens when you combine data from multiple tables using JOIN.


----
**04. How many records have a fare_amount of 0?**

>> 8,333

```sql
SELECT COUNT(*) FROM `your_project_id.your_dataset_name.yellow_tripdata_external`
WHERE fare_amount = 0;
````


----

**05. What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_timedate and order the results by VendorID (Create a new table with this strategy)**

>> Partition by `tpep_dropoff_timedate` and Cluster on `VendorID`

````sql
CREATE OR REPLACE TABLE `your_project_id.your_dataset_name.optimized_yellow_tripdata_2024`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT * FROM `your_project_id.your_dataset_name.yellow_tripdata_2024`;

````


*Explanation*

- Since queries will always filter on `tpep_dropoff_timedate`, partitioning by this column ensures that only the relevant partitions are scanned, improving query performance and reducing costs.
- Since results need to be ordered by `VendorID`, clustering on this column will optimize the sorting and grouping process within each partition, reducing query time.

***Why are the other options incorrect?***
❌ Cluster on tpep_dropoff_timedate and Cluster on VendorID
BigQuery does not allow multiple clustering columns without partitioning first.
Clustering alone does not provide the storage efficiency of partitioning when filtering on tpep_dropoff_timedate.

❌ Cluster on tpep_dropoff_timedate and Partition by VendorID
Partitioning by VendorID is inefficient because there are usually only a few unique VendorIDs (e.g., 1 or 2 taxi vendors), leading to very large partitions.
Instead, partitioning by a time-based column (like tpep_dropoff_timedate) ensures a better distribution of data.

❌ Partition by tpep_dropoff_timedate and Partition by VendorID
BigQuery does not support multiple partitioned columns in a single table. Only one column can be used for partitioning.

---

**06. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_timedate 03/01/2024 and 03/15/2024 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.**

>> 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

````sql
SELECT DISTINCT VendorID 
FROM `your_project_id.your_dataset_name.optimized_yellow_tripdata_2024` 
WHERE 
  TIMESTAMP_TRUNC(tpep_dropoff_datetime, DAY) BETWEEN TIMESTAMP("2024-03-01") AND TIMESTAMP("2024-03-15")
````

----

**07.Where is the data stored in the External Table you created?**
>> GCP Bucket

---

**08. It is best practice in Big Query to always cluster your data:**
>> False

--

**Bonus: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?**

```SELECT COUNT(*) FROM my_dataset.materialized_table;```

Estimated Bytes Read: Close to 0 Bytes

- BigQuery Materialized Views store precomputed results, meaning that the COUNT(*) query does not need to scan the original dataset. Instead, it retrieves the precomputed row count directly from metadata, which is extremely efficient and incurs almost no additional cost.

- Regular tables scan all rows to compute COUNT(*), leading to high bytes read.
Materialized views store precomputed results, so querying them reads only metadata, reducing query cost and execution time.


