#!/usr/bin/env python3

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    # Create table environment
    settings = EnvironmentSettings.new_instance() \
                      .in_streaming_mode() \
                      .build()
    
    tbl_env = StreamTableEnvironment.create(env, environment_settings=settings)
    
    # Configure kafka connector
    kafka_jar = "file:///opt/flink/lib/flink-sql-connector-kafka-1.16.0.jar"
    tbl_env.get_config().get_configuration().set_string(
        "pipeline.jars", kafka_jar
    )
    
    # Set configuration to ignore parse errors for JSON with NaN values
    tbl_env.get_config().get_configuration().set_string(
        "table.exec.source.cdc-events-duplicate", "true"
    )
    tbl_env.get_config().get_configuration().set_string(
        "table.exec.sink.not-null-enforcer", "drop"
    )
    
    # Create source table - Green Taxi trips from Kafka with proper handling of NaN values
    source_ddl = """
        CREATE TABLE green_trips (
            lpep_pickup_datetime TIMESTAMP(3),
            lpep_dropoff_datetime TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            WATERMARK FOR lpep_dropoff_datetime AS lpep_dropoff_datetime - INTERVAL '5' SECONDS
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'green-trips',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'properties.group.id' = 'taxi-session-consumer',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json',
            'json.fail-on-missing-field' = 'false',
            'json.ignore-parse-errors' = 'true'
        )
    """
    
    # Create sink table for results with primary key
    sink_ddl = """
        CREATE TABLE taxi_sessions (
            PULocationID INT,
            DOLocationID INT,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            trip_count BIGINT,
            session_duration_minutes DOUBLE,
            PRIMARY KEY (PULocationID, DOLocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = 'taxi_sessions',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        )
    """
    
    # Execute DDL statements
    print("Creating source table...")
    tbl_env.execute_sql(source_ddl)
    
    print("Creating sink table...")
    tbl_env.execute_sql(sink_ddl)
    
    # Create a SQL query that processes the data with session window
    # To find the longest unbroken streak of taxi trips between pickup and dropoff locations
    session_query = """
        INSERT INTO taxi_sessions
        SELECT 
            PULocationID,
            DOLocationID,
            MIN(window_start) AS session_start,
            MAX(window_end) AS session_end,
            COUNT(*) AS trip_count,
            TIMESTAMPDIFF(MINUTE, MIN(window_start), MAX(window_end)) AS session_duration_minutes
        FROM (
            SELECT 
                PULocationID,
                DOLocationID,
                window_start,
                window_end
            FROM TABLE(
                TUMBLE(TABLE green_trips, DESCRIPTOR(lpep_dropoff_datetime), INTERVAL '1' MINUTE)
            )
            GROUP BY PULocationID, DOLocationID, window_start, window_end
        ) 
        GROUP BY PULocationID, DOLocationID
    """
    
    print("Executing session query...")
    
    # Execute the query with a detached job
    tbl_env.execute_sql(session_query)
    
    print("Job submitted successfully!")

if __name__ == "__main__":
    main()