# alternative load code for the homework
# by dilipkumar
 

@dlt.source(name="fhv_tripdata")
def download_parquet():
       for month in range(1, 13):
           file_name = f"fhv_tripdata_2019-{month:02d}.parquet"
           url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
           response = requests.get(url)
           df = pd.read_parquet(BytesIO(response.content))
           yield dlt.resource(df, name=file_name)

pipeline_fs = dlt.pipeline(
            pipeline_name='fs_pipeline',
            destination='filesystem',
            dataset_name='fhv',)

load_info_fs = pipeline_fs.run(download_parquet(), loader_file_format="parquet")
print(load_info_fs)

pipeline = dlt.pipeline(
       pipeline_name="fhv_pipeline",
       destination='bigquery',
       dataset_name=DATASET_NAME,
   )
load_info = pipeline.run(
       download_parquet(),
       loader_file_format="parquet",
       table_name="fhv_tripdata", 
       write_disposition="append"
   )
print(load_info)