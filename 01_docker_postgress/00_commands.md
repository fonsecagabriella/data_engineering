# Commands Docker + Postgres 🐟 👩🏽‍💻

## Creating and Running a Container for Postgres

This code will create a container with Postgres.
These are the details of the db we will be using in the project.

In the shell, run to create:

```docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/gabi/codes/data_engineering/ny_taxi_post_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

`docker run`

**Explanation:** 
    `-e` for environment variable
    `-v` for mount
    `-p` to map port (local:cloud)


## Create a container for pgAdmin
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

## Create a Network
We will create a network to connect the database and pgAdmin.

To create the network run in the shell.

`docker network create pg-network`


### Create a container with Postgres inside the network

The command below creates a container with Postgres using the network we created above.

```docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/gabi/codes/data_engineering/ny_taxi_post_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg_database \
  postgres:13

```

### Postgress and pgAdmin

Here we connect Postgres and pgAdmin so we can manipulate the db in pgAdmin instead of via command line.

```docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin2 \
  dpage/pgadmin4
```


## Python Script to ingest data to db locally

```
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
```


## Python Script to ingest data to container
Ps: in real life you would nont use pg-network as parameter for the container, but in the host you would have an URL of where your db is located

```docker build -it taxi_ingest:v001```

```docker run -it \
--network=pg-network \
taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg_database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
    
```