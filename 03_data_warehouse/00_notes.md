# Data Warehouse and BigQuery 👩🏽‍💻

1. [OLTP x OLAP x Data Warehouse](#oltp-x-olap-x-data-warehouse)
   - [In Summary](#in-summary)
   - [Data Flow](#data-flow)
   - [Purpose and Use](#purpose-and-use)
   - [Schema Design](#schema-design)
   - [OLTP (Online Transaction Processing)](#oltp-online-transaction-processing)
   - [OLAP (Online Analytical Processing)](#olap-online-analytical-processing)
   - [Data Warehouse](#data-warehouse)

2. [BigQuery](#bigquery)
   - [Best Practices](#best-practices)
     - [Cost Reduction](#cost-reduction)
     - [Improve Query Performance](#improve-query-performance)

3. [Partitioning vs Clustering](#partitioning-vs-clustering)
   - [Partitioning](#partitioning)
   - [Clustering](#clustering)
   - [Comparison Table](#comparison-table)
   - [When to Use Partitioning & Clustering Together](#when-to-use-partitioning--clustering-together)

4. [Difference Between Regular, Materialized, and External Tables in BigQuery](#difference-between-regular-materialized-and-external-tables-in-bigquery)
   - [Regular Table](#regular-table)
   - [Materialized Table](#materialized-table)
   - [External Tables in BigQuery](#external-tables-in-bigquery)
   - [Pros & Cons of External Tables](#pros--cons-of-external-tables)


----



## 1. OLTP x OLAP x Data Warehouse
**In Summary:**
- OLTP is like a cashier recording every sale in a store.
- Data Warehouse is like the store manager's database that combines all sales records from multiple branches for a full overview.
- OLAP is like an analyst reviewing and slicing these sales data to uncover patterns, trends, and insights for decision-making.

-------------

<img src="../images/data-management.png" width="80%">


**Data Flow:**
- Data originates in OLTP systems, where business transactions are recorded. 
- This raw transactional data is extracted, transformed, and loaded (ETL/ELT process) into the Data Warehouse.


**Purpose and Use:**
- OLTP focuses on operational efficiency and quick transactional processes.
- Data Warehouse stores historical, cleaned, and consolidated data for analytical purposes.
- OLAP provides tools and technologies to analyze the data in the Data Warehouse, supporting business intelligence and strategic decisions.


**Schema Design:**
- OLTP systems use normalized schemas to reduce redundancy and improve transactional performance.
- Data Warehouses use denormalized schemas (e.g., star schema) to optimize analytical queries.

------



| Feature                 | OLTP                          | OLAP                         |
|-------------------------|-------------------------------|------------------------------|
| **Main Use**            | Day-to-day operations         | Data analysis and reporting  |
| **Data Volume**         | Small and current             | Large and historical         |
| **Query Type**          | Simple, fast transactions     | Complex, analytical queries  |
| **Data Structure**      | Normalized                    | Denormalized                 |
| **Users**               | Operational staff/customers   | Analysts/decision-makers     |
| **Backup and recovery**| Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| **Space requirements** | Generally small if historical data is archived                        | Generally large due to aggregating large datasets                        |



### **OLTP (Online Transaction Processing)**
Designed to handle day-to-day operations like sales, banking transactions, or customer orders.

- Fast and frequent transactions: Handles many small, quick tasks like adding a new order or updating an account balance.
- Real-time updates: Ensures data is always up-to-date for operational needs.
- Data structure: Highly normalized (organized into many tables to avoid redundancy).
- Users: Typically used by front-line employees or customers interacting with systems like apps or websites.
- Example: When you buy something online, OLTP systems handle the order, update the stock, and process the payment—all quickly and accurately.

### **OLAP (Online Analytical Processing)**
Designed for analyzing large amounts of data to identify trends, patterns, or insights.

- Complex queries: Processes heavy, analytical queries like "What were our total sales by region over the past year?"
- Historical data: Often works with aggregated data to look at trends over time.
- Data structure: Denormalized for faster reading (data may be stored in fewer, broader tables).
- Users: Typically used by analysts, decision-makers, or business intelligence tools.
- Example: A company might use OLAP to analyze last year's sales to decide which products to promote this year.

### **Data Warehouse**
Central repository that aggregates, organizes, and stores historical data for analysis.

<img src="../images/data_warehouse.png" width="70%">

- Role in the ecosystem: Pulls and integrates data from multiple OLTP systems (and other sources like APIs, logs, or flat files).
- Uses ETL/ELT processes to transform transactional data into a structured format suitable for analysis.
- Serves as the foundation for OLAP activities.
- Optimized for read-heavy operations and large-scale aggregations.
- Stores denormalized data in formats like star or snowflake schemas for performance and usability.


-----------

## 4. BigQuery
- Serverless datawarehouse
- Software as well as infrastructure including scalability and high-availability 
- Uses column oriented structured
<img src="../images/column-oriented.png" width="80%">

- You can used BigQuery to run ML models

````
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata``
OPTIONS(
    format = 'CSV',
    -- you can get all files stored in the bucket with *
    uris=['gs://nyc-tl-data/tripdata/yellow_tripdata_2019-*.csv'] 
)
````

### **Best practices**
**COST REDUCTION**
- Avoid `SELECT *` 
- Price queries before running them
- Use clustered or partioned tables

**IMPROVE QUERY PERFORMANCE**
- Filter on partitioned columns
- Denormalise data
- Use nested or repeated columns
- Reduce data before using `JOIN`
- Place the table with the largest number of rows first followed by the tables with the fewest rows, and then place the remaning tables by decreasing size.



----



## 3. Partioning vs Clustering

| **Feature**       | **Partitioning**                                 | **Clustering**                                    |
|--------------------|--------------------------------------------------|--------------------------------------------------|
| **How it works**   | Divides the table into independent partitions.   | Organizes data within the table (or partition).  |
| **Key Columns**    | Focuses on one partitioning column (or criteria).| Focuses on one or more clustering columns.       |
| **Best for**       | Date-based queries                               | Filtering, sorting, or grouping on specific columns |
| **Column types**   | Date or Timestamp columns                        | Low-cardinality columns (e.g., region, category) |
| **Storage**        | Creates separate physical storage for partitions.| No separate storage; organizes data internally.  |
| **Use Case**       | Filters on partitioning column (e.g., date).     | Filters or aggregates on clustering columns.     |
| **Benefit**        | Reduces query cost by skipping entire partitions.| Reduces data scanned within partitions or table. |
| **Improves performance?** | ✅ Yes, by scanning only relevant partitions | ✅ Yes, by reducing scanned bytes within partitions |
| **Reduces cost?**  | ✅ Yes, fewer scanned bytes                      | ✅ Yes, especially for frequent filters        |
| **Can be combined?** | ✅ Yes                                        | ✅ Yes                                         |




### **Partition**
Partitioning divides a table into smaller, manageable segments (called partitions) based on the values in one or more columns. It allows queries to scan only relevant partitions, improving performance for queries that filter on the partitioned column(s).


- The icone for partitioned and non-partitioned data is different (the one for partitioned has a little bar)
<img src="../images/partioned-non.png" width="90%">

### **Clustering**
Clustering organizes data within a table (or partition) based on the values in one or more columns. It stores similar rows together physically, reducing the amount of data scanned during queries.


- The order of the columns matter for performance
- Clustering improves filter and aggrehgate queries
- You can specify up to for
- Useful for big tables (> 1GB)

**When Clustering is NOT Necessary or Useful:**
❌ Small tables (<1GB)
The overhead of maintaining clustering is not worth it for small tables.

❌ High-cardinality columns (too many unique values)
Clustering on a column like user_id with millions of unique values may not provide significant performance gains.

❌ Queries do not filter, sort, or aggregate on the clustering column
If queries rarely use WHERE, ORDER BY, or GROUP BY on the clustering column, the benefits of clustering will not be realized.


### When to Use Partitioning & Clustering Together?
If queries filter by date and another column, use both.

Example:
- Partition by `event_date`
- Cluster by `customer_id`

This speeds up queries that filter by date AND customer ID.

**If unsure, start with partitioning (it's more impactful on query performance and cost). Add clustering later if additional optimization is needed.**

---------------



## 4. Difference Between Regular, Materialized and External Tables in BigQuery

| Feature | Regular Table | Materialized Table (View) |
|---|---|---|
| Storage | Stores full data | Stores precomputed query results |
| Performance | Slower, queries scan the table | Faster, queries use precomputed results |
| Refresh | Must be manually updated | Automatically updates when source changes |
| Use Case | Storing raw or cleaned data | Improving query speed for frequent queries |
| Cost | Charges for storage & queries | Charges for storage but **reduces** query costs |

### 4.1 Regular Table
A **regular table** in BigQuery is a standard table where data is stored in a structured format. It is queried directly from storage, meaning every time you run a query, BigQuery scans the data in the table to generate results.

- Data is stored persistently.
- Queries read from the table every time they are executed.
- No precomputed results; queries can take longer if scanning large datasets.
- Good for frequently updated datasets.

```sql
CREATE OR REPLACE TABLE my_dataset.regular_table AS
SELECT * FROM my_dataset.source_table;
```

### 4.2 Materialized Table
A **materialized** table is a precomputed table that stores the results of a query. Unlike regular tables, materialized tables improve query performance by reducing the amount of data that needs to be scanned.

- Stores precomputed query results.
- Improves performance for repetitive queries.
- Requires periodic refresh to stay up-to-date.
- Reduces query costs by avoiding frequent full table scans.

````sql
CREATE MATERIALIZED VIEW my_dataset.materialized_table AS
SELECT customer_id, SUM(total_amount) AS total_spent
FROM my_dataset.transactions
GROUP BY customer_id;

````

### 4.3 External Tables in BigQuery

✅ **No Data Duplication** → Data remains in GCS; BigQuery does not copy it.
✅ **Cost-Efficient** → You don’t pay for storage in BigQuery, only for the query processing.
✅ **Schema Definition** → You must define the schema, or BigQuery can auto-detect it.
✅ **Supports Various Formats** → CSV, JSON, Parquet, ORC, and Avro files.


**When Should You Use an External Table?**
- When you don’t want to store large datasets inside BigQuery.
- When data frequently updates in GCS and you don’t want to reload it into BigQuery.
- When you only need to run occasional queries on the data.

| Pros ✅ | Cons ❌ |
|---------|---------|
| No need to move data into BigQuery | Query performance is slower than internal tables |
| Saves on storage costs | Cannot be used for clustering or partitioning |
| Supports various file formats (CSV, JSON, Parquet) | Limited support for certain operations (e.g., updates) |
