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

# Define base URL for FHV datasets
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/"
FILES = [f'fhv_tripdata_2019-{str(month).zfill(2)}.csv.gz' for month in range(1, 13)]

def upload_to_gcs(dataframe, file_name):
    """Uploads a Pandas DataFrame to GCS as a CSV file."""
    print(f"💻 Uploading {file_name} to GCS...")  # Signal before upload
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"fhv_data/{file_name}")

    csv_data = dataframe.to_csv(index=False)
    blob.upload_from_string(csv_data, content_type="text/csv")

    print(f"📤 Uploaded {file_name} to GCS.")

def download_fhv_data(file_name):
    """Downloads a given FHV CSV file from GitHub, saves to GCS, and returns a DataFrame."""
    print(f"⏳ Downloading {file_name}...")  # Signal before download
    url = BASE_URL + file_name
    response = requests.get(url)
    if response.status_code == 200:
        print(f"✅ Downloaded: {file_name}")
        df = pd.read_csv(BytesIO(response.content), compression='gzip')

        # Print column names to debug
        print(f"Columns in {file_name}: {df.columns.tolist()}")

        # Rename columns if necessary
        if "PUlocationID" in df.columns:
            df.rename(columns={"PUlocationID": "pu_location_id"}, inplace=True)
        if "DOlocationID" in df.columns:
            df.rename(columns={"DOlocationID": "do_location_id"}, inplace=True)

        # Ensure columns exist before modifying
        if "pu_location_id" in df.columns:
            df["pu_location_id"] = df["pu_location_id"].fillna(0).astype(int)
        if "do_location_id" in df.columns:
            df["do_location_id"] = df["do_location_id"].fillna(0).astype(int)

        # Upload to GCS
        upload_to_gcs(df, file_name)

        return df
    else:
        print(f"❌ Failed to download: {file_name}")
        return None

def load_data_into_bigquery():
    """Loads the downloaded FHV data into BigQuery using dlt."""
    print("🚀 Starting to load data into BigQuery...")  # Signal before loading data
    
    pipeline = dlt.pipeline(
        pipeline_name="fhv_pipeline_n",
        destination="bigquery",
        dataset_name=DATASET_NAME
    )

    # Download & load all FHV files
    all_data = [download_fhv_data(file) for file in FILES]
    all_data = [df for df in all_data if df is not None]  # Remove failed downloads

    if all_data:  # Only proceed if we have data
        print(f"📈 Data loaded successfully into BigQuery.")
        load_info = pipeline.run(all_data, table_name="fhv_trips", write_disposition="append")
        print(f"🚀 Data loaded successfully: {load_info}")
    else:
        print("❌ No data to load into BigQuery. Check if all files were downloaded successfully.")

if __name__ == "__main__":
    load_data_into_bigquery()
