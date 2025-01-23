## 01. Understanding docker first run


Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.
What's the version of Pip?
>> Version  24.3.1

`docker run -it --entrypoint bash python:3.12.8`

`pip list`



## 02. Understanding Docker networking and docker-compose

Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

>> db:5432

```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data 
```

**EXPLANATION**
**Docker Compose automatically creates a network for the services defined in the docker-compose.yaml.
The containers can communicate with each other using their service names as hostnames.**

- The hostname for pgAdmin to connect to the PostgreSQL database is the service name of the db container, which is db. Docker sets up internal DNS so containers can resolve each other's service names.
- The internal port of the PostgreSQL service (5432) is what pgAdmin should use to connect. The 5433 port specified in the ports section is only for external access to PostgreSQL from your host machine.


## 03. Trip Segmentation Count

>> 104,802; 198,924; 109,603; 27,678; 35,189


````
SELECT 
	COUNT(1)
FROM 
	green_taxi_trips t
WHERE
	CAST(t.lpep_pickup_datetime AS DATE) >= '2019-10-01' AND 
    CAST(t.lpep_pickup_datetime AS DATE) <= '2019-10-31' AND
	CAST(t.lpep_dropoff_datetime AS DATE) >= '2019-10-01' AND
	CAST(t.lpep_dropoff_datetime AS DATE) <= '2019-10-31' AND
	t.trip_distance 
````


## 04. Longest trip for each day

>> 2019-10-31

````
SELECT 
    CAST(t.lpep_pickup_datetime AS DATE) AS pick_up,
    MAX(trip_distance) AS max_trip_distance
FROM 
    green_taxi_trips t
GROUP BY 
    CAST(t.lpep_pickup_datetime AS DATE)
ORDER BY 
    max_trip_distance DESC;
````

### 05. Three biggest pickup zones

>> East Harlem North, East Harlem South, Morningside Heights


````
SELECT 
    SUM(total_amount) AS total_amount,
	z_pickup."Zone" AS zone
FROM 
    green_taxi_trips t
	JOIN taxi_zone_lookup z_pickup 
        ON t."PULocationID" = z_pickup."LocationID"
WHERE
	CAST(t.lpep_pickup_datetime AS DATE) = '2019-10-18'
GROUP BY 
    zone
HAVING SUM(total_amount)>13000
ORDER BY total_amount DESC

````

## 06. Largest tip

>> JFK Airport


````
SELECT 
    MAX(tip_amount) AS tip_amount,
	z_dropoff."Zone" AS zone
FROM 
    green_taxi_trips t
	JOIN taxi_zone_lookup z_pickup 
        ON t."PULocationID" = z_pickup."LocationID"
	JOIN taxi_zone_lookup z_dropoff 
        ON t."DOLocationID" = z_dropoff."LocationID"
WHERE
	CAST(t.lpep_pickup_datetime AS DATE) >= '2019-10-01' AND
	CAST(t.lpep_pickup_datetime AS DATE) <= '2019-10-31' AND
	z_pickup."Zone" = 'East Harlem North'
GROUP BY 
    z_dropoff."Zone"	
ORDER BY tip_amount DESC
````

## 07. Terraform Workflow

>> terraform init, terraform apply -auto-approve, terraform destroy


