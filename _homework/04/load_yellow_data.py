import dlt
import requests
import pandas as pd
import os
from io import BytesIO
from google.cloud import storage

# Set Google Cloud credentials
CREDENTIALS_FILE = "peppy.json"  
client = storage.Client.from_service_account_json(CREDENTIALS_FILE)

# Define dataset and bucket
DATASET_NAME = "zoomcamp_dbt_4"  # Change to your BigQuery dataset
BUCKET_NAME = "imgabi-zoomcamp-kestra"  

# Define base URL for yellow datasets
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
FILES = [f'yellow_tripdata_{year}-{str(month).zfill(2)}.csv.gz' for year in (2019, 2020) for month in range(1, 13)]

def upload_to_gcs(dataframe, file_name):
    """Uploads a Pandas DataFrame to GCS as a CSV file."""
    print(f"💻 Uploading {file_name} to GCS...")
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"yellow/{file_name}")
    csv_data = dataframe.to_csv(index=False)
    blob.upload_from_string(csv_data, content_type="text/csv")
    print(f"📤 Uploaded {file_name} to GCS.")

def download_yellow_data(file_name):
    """Downloads a given yellow CSV file from GitHub, saves to GCS, and returns a DataFrame."""
    print(f"⏳ Downloading {file_name}...")
    url = BASE_URL + file_name
    response = requests.get(url)
    if response.status_code == 200:
        print(f"✅ Downloaded: {file_name}")
        df = pd.read_csv(BytesIO(response.content), compression='gzip', dtype={
            'VendorID': 'Int64',
            'tpep_pickup_datetime': 'str',
            'tpep_dropoff_datetime': 'str',
            'store_and_fwd_flag': 'str',
            'RatecodeID': 'Int64',
            'PULocationID': 'Int64',
            'DOLocationID': 'Int64',
            'passenger_count': 'Int64',
            'trip_distance': 'float64',
            'fare_amount': 'float64',
            'extra': 'float64',
            'mta_tax': 'float64',
            'tip_amount': 'float64',
            'tolls_amount': 'float64',
            'ehail_fee': 'float64',
            'improvement_surcharge': 'float64',
            'total_amount': 'float64',
            'payment_type': 'Int64',
            'trip_type': 'Int64',
            'congestion_surcharge': 'float64'
        })
        print(f"Columns in {file_name}: {df.columns.tolist()}")
        upload_to_gcs(df, file_name)
        return df
    else:
        print(f"❌ Failed to download: {file_name}")
        return None

def load_data_into_bigquery():
    """Loads the downloaded yellow data into BigQuery using dlt."""
    print("🚀 Starting to load data into BigQuery...")
    pipeline = dlt.pipeline(
        pipeline_name="yellow_pipeline",
        destination="bigquery",
        dataset_name=DATASET_NAME
    )

    for file in FILES:
        df = download_yellow_data(file)
        if df is not None:
            print(f"🚀 Running dlt pipeline for {file}...")
            try:
                load_info = pipeline.run(
                    [df],  # Process one file at a time
                    table_name="yellow_tripdata", 
                    write_disposition="append"
                )
                print(f"📈 Data loaded successfully into BigQuery for {file}.")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")

if __name__ == "__main__":
    load_data_into_bigquery()
