# Introduction to Data Loading Tool (DLT)

## What is DLT?

[Data Loading Tool (DLT)](https://github.com/dlt-hub/dlt) is an open-source Python library designed to streamline the process of loading data from various sources into well-structured, live datasets. It offers a lightweight interface for extracting data from REST APIs, SQL databases, cloud storage, and Python data structures. DLT is designed to be easy to use, flexible, and scalable. 

## Key Features of DLT

- **Ease of Use**: DLT provides a simple interface for data extraction, making it accessible for both beginners and experienced data engineers.
- **Flexibility**: Supports a wide range of data sources, including REST APIs, SQL databases, and cloud storage.
- **Scalability**: Designed to handle large volumes of data efficiently.

# Setting Up Your First DLT Project

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.9 or later**
- **Virtual Environment (Recommended)**: It's advisable to use a virtual environment to manage dependencies.

## Step 01: Install DLT with support for DuckDB (a lightweight db)

Install DLT using pip:

```bash
pip install dlt[duckdb]
```

*Ps: you need to use ""  to pip install via shell zhs*

## Step 02:  Initialize a New DLT Project
````
dlt init <project_name> <destination>
````

## Step 03: Define Your Data Pipeline
Within your project directory, create a Python script (e.g., pipeline.py) to define your data pipeline. Here's an example:

````python
import dlt
from dlt.sources import source
from dlt.destinations import destination

@dlt.source
def my_source():
    # Define your data extraction logic here
    pass

@dlt.destination
def my_destination():
    # Define your data loading logic here
    pass

@dlt.pipeline
def my_pipeline():
    data = my_source()
    my_destination(data)
````

## Step 04: Run the pipeline

`dlt run pipeline.py`

