# data-engineering

## Postgress command line for Docker

-e for environment variable
-v for mount
-p to map port (local:cloud)

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/gabi/codes/data_engineering/ny_taxi_post_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

docker run

## Command to use pgAdmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4


## Postgres Network

docker network create pg-network


### This command will create a container 
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /Users/gabi/codes/data_engineering/ny_taxi_post_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg_database \
  postgres:13

## Postgress and pgAdmin

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin2 \
  dpage/pgadmin4


## Python Script to ingest data to db locally

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz


## Python Script to ingest data to container
Ps: in real life you would nont use pg-network as parameter for the container, but in the host you would have an URL of where your db is located

docker build -it taxi_ingest:v001

docker run -it \
--network=pg-network \
taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg_database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz

