# Homework - Week 2


**01. Within the execution for `Yellow` Taxi data for the `year 2020` and `month 12`: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?**

> 128.3 MB

*Explanation: Look inside "Buckets" in GCS, for the file in question.*

**02. What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?**

> green_tripdata_2020-04.csv

*Explanation: Check in Kestra output files*

**03. How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?**

> 24,648,663

*Explanation: Run the following command in BigQuery:*

````
SELECT COUNT(1)
FROM zoomcamp.yellow_tripdata
WHERE EXTRACT(YEAR FROM tpep_pickup_datetime) = 2020
````

**04. How many rows are there for the Green Taxi data for all CSV files in the year 2020?**

> 1,734,039

*Explantion: Run the following command in Big Query:*

````
SELECT COUNT(1)
FROM zoomcamp.green_tripdata
WHERE EXTRACT(YEAR FROM lpep_pickup_datetime) = 2020
````

**05. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?**
> 1,925,152


**06. How would you configure the timezone to New York in a Schedule trigger?**
>> Add a timezone property set to America/New_York in the Schedule trigger configuration


*Explanation:*

*- Kestra uses the standard IANA t`i`mezone database, which specifies timezones in the format Region/City (e.g., America/New_York)*

*- Kestra uses the standard IANA timezone database, which specifies timezones in the format Region/City (e.g., America/New_York)*

*- `UTC-5` is a fixed offset, which also does not account for DST changes. During DST, New York switches to `UTC-4`.*

````
id: example_schedule
namespace: example
tasks:
  - id: example_task
    type: io.kestra.core.tasks.debugs.Return
    format: "This task runs on a schedule"
triggers:
  - id: example_trigger
    type: io.kestra.core.models.triggers.types.Schedule
    cron: "0 12 * * *"
    timezone: "America/New_York"
````
