# Using Kestra, dbt, and dlt in a Data Engineering Project

## 1. Overview of the Tools

| Tool  | Purpose  | Key Features | Similarities |
|--------|-------------|--------------|----------------|
| **Kestra** | **Workflow Orchestration** | Schedules and runs tasks (ETL, API calls, data movement, dbt runs) | Automates workflows like Airflow |
| **dlt (Data Load Tool)** | **Extract & Load (EL)** | Simplifies data ingestion from APIs, databases, and files into cloud data warehouses | Like Airbyte but code-first |
| **dbt (Data Build Tool)** | **Transform & Model (T)** | Manages SQL-based transformations, tests data, creates tables/views | Works with SQL-based transformations |

## 2. How They Work Together

A complete **Extract, Load, Transform (ELT) workflow** might look like this:

1. **dlt extracts and loads data** → Pulls data from APIs, databases, or files and loads it into a cloud warehouse (e.g., BigQuery).
2. **dbt transforms data** → Cleans, models, and enriches the raw data into useful tables/views.
3. **Kestra orchestrates everything** → Automates and schedules dlt and dbt tasks, ensuring the pipeline runs smoothly.

---

## 3. Example Use Case: Analyzing Taxi Ride Data

Imagine you need to analyze taxi ride data from an API and store the results in BigQuery.

### **Step 1: Extract and Load Data with dlt**
- Use **dlt** to pull raw taxi ride data from an API (`taxi_ride_api`).
- Load this raw data into **BigQuery** (`raw_taxi_rides` table).

```python
import dlt
from dlt.sources import api

pipeline = dlt.pipeline(destination="bigquery", dataset_name="raw_data")

data = api.get("https://taxi-data.com/api/rides")  # Example API
pipeline.run(data, table_name="raw_taxi_rides") 

```


---

# Step 2: Transform Data with dbt

Use dbt to clean and transform the raw data.  
Create models for ride durations, payment methods, and revenue.  

### Example: `stg_taxi_rides.sql` (staging model)
```sql
WITH trips AS (
    SELECT *, 
           TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, SECOND) AS ride_duration
    FROM `raw_data.raw_taxi_rides`
)
SELECT
    ride_id,
    vendor_id,
    pickup_location,
    dropoff_location,
    ride_duration,
    fare_amount,
    CASE 
        WHEN payment_type = 1 THEN 'Credit Card'
        WHEN payment_type = 2 THEN 'Cash'
        ELSE 'Other'
    END AS payment_method
FROM trips;
````

---

### Step 3: Automate with Kestra

Example: kestra.yaml (workflow definition)


```yml
id: taxi_data_pipeline
namespace: data_engineering

tasks:
  - id: extract_load_dlt
    type: io.kestra.plugin.scripts.python.Script
    script: |
      import dlt
      from dlt.sources import api
      pipeline = dlt.pipeline(destination="bigquery", dataset_name="raw_data")
      data = api.get("https://taxi-data.com/api/rides")
      pipeline.run(data, table_name="raw_taxi_rides")

  - id: transform_dbt
    type: io.kestra.plugin.dbt.CloudRun
    accountId: "{{ dbt_account_id }}"
    environmentId: "{{ dbt_env_id }}"
    commands:
      - dbt run
```