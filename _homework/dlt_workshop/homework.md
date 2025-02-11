# Homework - DLT Workshop

**01. dlt Version**

>> dlt 1.6.1

*Explanation*

First you install dlt:

`pip install 'dlt[duckdb]'`

Then check the version:

`dlt --version`


**02. How many tables were created?**

>> 04

*Explanation: Code at [taxi_dlt_pipeline](taxi_dlt_pipeline.ipynb)*

Output of `SQL >> DESC `:

```
           database        schema                 name  \
0  ny_taxi_pipeline  ny_taxi_data           _dlt_loads   
1  ny_taxi_pipeline  ny_taxi_data  _dlt_pipeline_state   
2  ny_taxi_pipeline  ny_taxi_data         _dlt_version   
3  ny_taxi_pipeline  ny_taxi_data                rides   

                                        column_names  \
0  [load_id, schema_name, status, inserted_at, sc...   
1  [version, engine_version, pipeline_name, state...   
2  [version, engine_version, inserted_at, schema_...   
3  [end_lat, end_lon, fare_amt, passenger_count, ...   

                                        column_types  temporary  
0  [VARCHAR, VARCHAR, BIGINT, TIMESTAMP WITH TIME...      False  
1  [BIGINT, BIGINT, VARCHAR, VARCHAR, TIMESTAMP W...      False  
2  [BIGINT, BIGINT, TIMESTAMP WITH TIME ZONE, VAR...      False  
3  [DOUBLE, DOUBLE, DOUBLE, BIGINT, VARCHAR, DOUB...      False  
```

**03. Explore the loaded data**
>> 10000

*Explanation: Code at [taxi_dlt_pipeline](taxi_dlt_pipeline.ipynb)*

**04. Trip Duration Analysis**
>> 12.3049


*Explanation: Code at [taxi_dlt_pipeline](taxi_dlt_pipeline.ipynb)*