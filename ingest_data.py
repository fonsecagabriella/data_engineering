import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = "output.csv"


    # download the csv
    # this command get the file from the url and save it as csv_name, or output.csv
    os.system(f"wget {url} -O {csv_name}")

    # engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi") #values from the docker file (for postgres)
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}") #values from the docker file (for postgres)

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip') 

    df = next(df_iter)


    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime) # fix issue where TEXT should be something else, such as DATETIME
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime) 

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df.to_sql(name=table_name, con=engine, if_exists="append")

    while True:
        t_start = time()
        df = next(df_iter)

        # these steps need to be done everytime: convert datetime and append the new row
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime) 
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists="append")

        t_end = time()

        print("another row inserted, took %.3f seconds" % (t_end - t_start))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert data into a PostgreSQL database")

    parser.add_argument("--user", help="username for postgres")
    parser.add_argument("--password", help="password for postgres")
    parser.add_argument("--host", help="host for postgres")
    parser.add_argument("--port", help="port for postgres")
    parser.add_argument("--db", help="database for postgres")
    parser.add_argument("--table_name", help="name of the table we will write the records to")
    parser.add_argument("--url", help="url of the csv")

    args = parser.parse_args()

    main(args)
