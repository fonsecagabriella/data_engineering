FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

# create a directory called app
WORKDIR /app
# from current to destination
COPY ingest_data.py ingest_data.py


#ENTRYPOINT [ "bash" ] # run bash

# run python script
ENTRYPOINT [ "python", "ingest_data.py" ]