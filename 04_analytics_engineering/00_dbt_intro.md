
# Analytics Engineering

### Table of contents

- [Introduction to analytics engineering](#Introduction-to-analytics-engineering)
- [Introduction to dbt](#Introduction-to-dbt)
- [Setting up dbt with bigquery](#setting-up-dbt-with-bigquery)
- [Development of dbt Models](#development-of-dbt-models)
    - [Anatomy of a dbt model](#Anatomy-of-a-dbt-model)
    - [FROM clause of a dbt model](#from-clause-of-a-dbt-model)
    - [Developing the first staging model](#developing-the-first-staging-model)
    - [Macros](#macros)
    - [Packages](#packages)
    - [Variables](#variables)
    - [Developing the second staging model](#developing-the-second-staging-model)
- [Core Models](#core-models)    
    - [Dim zones](#dim-zones)
    - [Fact trips](#fact-trips)
    - [Monthly zone revenue](#monthly-zone-revenue)
- [Building the model](#building-the-model)
- [Testing](#testing)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Visualising the transformed data](#visualising-the-transformed-data)




## Introduction to analytics engineering

_[Video source](https://www.youtube.com/watch?v=uF76d5EmdtU)_

In a traditional data team, we recognize the data engineer, the data analyst, and sometimes the data scientist. The data engineer prepares and maintains the infrastructure the data team needs. The data analyst uses the data hosted in that infrastructure to answer questions and solve problems.

With recent developments, data scientists and analysts are writing more code, but they are not trained as software engineers, and this is not their primary focus. Similarly, data engineers, while excellent software engineers, lack training in how the data is used by business users.

This gap is where the analytics engineer comes in. The role combines elements of the data engineer and the data analyst. It introduces good software engineering practices from the data engineer to the efforts of data analysts and scientists.

![ae1](images/ae1.jpg)

<br><br>

The analytics engineer may be exposed to the following tools:

- Data Loading (Stitch, Apache NiFi, Airbyte)
- Data Storing (Google BigQuery, Snowflake, Amazon Redshift)
- Data Modeling (dbt, Dataform, Apache Spark SQL)
- Data Presentation (Looker, Tableau, Google Data Studio, Power BI, Metabase)


This week, we’ll focus on the last two areas: data modeling and presentation.

### Data modeling concepts

**ETL vs. ELT**

In ETL, we extract the sources, transform the data, and then load it into a data warehouse. In ELT, we load the data into the data warehouse first and then transform it.

The first approach takes longer to implement because we must transform the data upfront. However, this results in more stable and compliant data because it is clean. On the other hand, ELT is faster and more flexible because the data is already loaded.

This approach leverages cloud data warehousing, which has lowered the cost of storage and compute. Without those restrictions, we can afford to load all our data first and transform it within the data warehouse.

![ae2](images/ae2.jpg)

<br><br>

We will now dive deeper into the transformation step.

**Kimball's Dimensional Modeling**

Kimball's Dimensional Modeling is a methodology for designing data warehouses. It was introduced by Ralph Kimball
and is an approach to Data Warehouse design which focuses on 2 main points:

- Deliver data that is understandable to the business
- Deliver fast query performance

Other goals such as reducing redundant data (prioritized by other approaches) are secondary. We are not going to
focus heavily on making sure that data is not redundant; instead, we prioritize user understandability of this
data and query performance.

Kimball's Dimensional Modeling uses Star Schema Design as its primary approach for organizing data in a data 
warehouse. This design ensures the data is easy to query, supports high performance, and aligns with the analytical
needs of businesses.

**Elements of Dimensional Modeling**

We are going to be talking mainly about two types of tables. Fact tables and dimensional tables. This is also 
known as the star schema.

- Fact tables: The central table in the schema. Contains quantitative data, metrics, or measurements that 
represent business processes (e.g., sales, revenue, or inventory counts). Includes foreign keys that link to the dimension tables.

- Dimensions tables: provide context to these fact tables. Contain attributes (details) about dimensions such as 
time, product, customer, or location.

The star schema is a type of database schema that is widely used in data warehousing and business intelligence 
for organizing and querying data. It is called "star schema" because its structure resembles a star shape when 
visualized: a central fact table is surrounded by multiple dimension tables.

![ae3](images/ae3.jpg)

<br><br>

The star schema simplifies data organization for analytics and reporting while prioritizing performance and ease
of use over strict normalization. Dimension tables can store repeated data, which consumes more storage compared
to normalized schemas.

**Architecture of Dimensional Modeling**

An analogy that is presented in Kimball's dimensional modeling is the kitchen analogy. The book compares
how the data warehouse and the ETL process could be compared with a restaurant:

- Staging Area: Here, we have the raw data. This is not meant to be exposed to everyone but only to those who 
 know how to use that raw data. In the case of a restaurant, this would be the food in its raw state before being 
 processed.

- Processing Area: This is the kitchen in a restaurant. Here, raw data is processed and turned into data models.
 Again, this is limited to those who know how to do this, such as the cooks. The focus is on efficiency and 
 ensuring standards are followed.

- Presentation Area: This is the dining hall and represents the final presentation of the data. Here, the data 
 is exposed to business stakeholders.


 ## Introduction to dbt

 _[Video source](https://www.youtube.com/watch?v=gsKuETFJr54)_

**What is dbt?** 

dbt is a transformation workflow that allows us to use SQL, or Python as well, to deploy analytical code. This code enables us to process all the data loaded from different sources. For example, in our case, we're using taxi data, but in a company setting, as a data engineer, you might work with data from backend systems, apps, frontend systems, or even third-party providers.

All this data is loaded into a data warehouse. We're referencing BigQuery, but it could also be other platforms. dbt sits on top of the data warehouse and helps transform raw data into something meaningful and useful for the business or stakeholders. This transformed data could be consumed by BI tools or integrated into other workflows, such as machine learning pipelines.

![ae4](images/ae4.jpg)

<br><br>

dbt helps turn raw data into actionable data by applying data modeling techniques. Additionally, it incorporates software engineering practices, like version control and modularity, into the analytics workflow. dbt allows developers to write SQL or Python in a sandboxed environment, introducing layers like testing, documentation, and CI/CD pipelines. 

**How does dbt work?**

In dbt, a model is essentially a SQL file where you write the logic to transform your data. For instance, if you have raw data in your data warehouse, you can create a model to apply transformations, clean it, and make it more structured and useful for analysis. A dbt model typically contains a SQL statement, such as a SELECT query, that defines how the data should be transformed.

A dbt model looks like this:

```sql

WITH
    orders as (select * from {{ref('orders')}}),
    line_items as (select * from {{ref('line_items')}})

SELECT
    id,
    sum(line_items.purchase_price)    

FROM orders
LEFT JOIN line_items ON orders.id = line_items.order_id

GROUP BY 1;
```

dbt simplifies many of the complexities traditionally associated with data transformation. It abstracts away the details of where the transformed data will be stored (e.g., in which schema or environment in your data warehouse). It also automates the generation of necessary SQL commands, such as Data Definition Language (DDL) for creating tables or views and Data Manipulation Language (DML) for inserting or updating data. This means you don't need to manually write the boilerplate SQL to manage these aspects.

When you execute a dbt command, such as dbt run, the tool compiles all the SQL files in your project. During this process, it resolves references between models, applies configuration settings (like whether a model should be a table or a view), and optimizes the SQL queries. Then, it runs the compiled SQL against your data warehouse.

![ae5](images/ae5.jpg)

<br><br>

Here’s how it works step by step:

1. Selection of Raw Data: The SQL statement in your model pulls raw data from the source tables or external datasets in the data warehouse.

2. Transformation: The model applies transformations, such as filtering, aggregations, joins, or calculations, to clean and organize the raw data

3. Persistence: Once the data is transformed, dbt persists the results back into the data warehouse as a table or a view. A table is a physical dataset stored in the warehouse. A view is a virtual dataset that dynamically runs the transformation logic whenever queried.

**How to use dbt?**

dbt has 2 main components: dbt Core and dbt Cloud:

* ***dbt Core***: open-source project that allows the data transformation.
    * Builds and runs a dbt project (.sql and .yaml files).
    * Includes SQL compilation logic, macros and database adapters.
    * Includes a CLI interface to run dbt commands locally.
    * Open-source and free to use.

* ***dbt Cloud***: SaaS application to develop and manage dbt projects.
    * Web-based IDE to develop, run and test a dbt project.
    * Jobs orchestration.
    * Logging and alerting.
    * Intregrated documentation.
    * Free for individuals (one developer seat).


**How are we going to use dbt?**

There are two ways to use dbt, and throughout the project, you'll see videos illustrating these approaches: version A and version B.

- Version A primarily uses BigQuery as the data warehouse. This method involves using the dbt Cloud Developer plan, which is free. You can create an account at no cost, and since this is cloud-based, there’s no need to install dbtcore locally.

- Version B uses PostgreSQL. In this approach, you'll perform development using your own IDE, such as VS Code, and install dbt Core locally connecting to the postgresql database. You will be running  dbt models through the CLI

During the project you might already have data loaded into GCP buckets. This raw data will be loaded into tables in BigQuery. dbt will be used to transform the data, and finally, dashboards will be created to present the results.

![ae6](images/ae6.jpg)

<br><br>

## Setting up dbt with bigquery

_[Video source](https://www.youtube.com/watch?v=J0XCDyKiU64)_


**1: Create a BigQuery service account**

In order to connect we need the service account JSON file generated from bigquery. Open the [BigQuery credential wizard](https://console.cloud.google.com/apis/credentials/wizard) to create a service account

Select BigQuery API and Application data
<br>

![ae7](images/ae7.jpg)
<br><br>

Next --> Continue --> Complete Service account name and description
<br>

![ae8](images/ae8.jpg)
<br><br>

Click on Create and continue

Select role --> BigQuery Admin

You can either grant the specific roles the account will need or simply use BigQuery admin, as you'll be the sole user of both accounts and data.
<br>

![ae9](images/ae9.jpg)
<br><br>

Click on continue --> Click on Done


**2: Download JSON key**

Now that the service account has been created we need to add and download a JSON key, go to the keys section, select "create new key". Select key type JSON and once you click on create it will get inmediately downloaded for you to use.

In the navigation menu (the three horizontal lines in the top-left corner), go to IAM & Admin > Service Accounts.

Find the dbt service account:
<br>

![ae10](images/ae10.jpg)
<br><br>

Navigate to the Keys tab. Click on Add Key > Create New Key
<br>

![ae11](images/ae11.jpg)
<br><br>

select JSON as the key type --> Create


**3: Copy taxi_rides_ny folder**

Copy taxi_rides_ny folder from https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering in your 04-analytics-engineering folder

This taxi_rides_ny folder contains macros, models, seeds. Cloning these elements gives you a strong foundation
for your DBT project, enabling you to focus on building and improving your data pipeline rather than starting
from scratch. Also saves time by reducing the need to recreate common logic or datasets.

```
git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git
```

Then copy the taxi_rides_ny folder in your own 04-analytics-engineering folder

 

**4: Create a dbt cloud project**

Create a dbt cloud account from [their website](https://www.getdbt.com/pricing/) (free for solo developers)
Once you have logged in into dbt cloud you will be prompt to create a new project.

You are going to need: 

 - access to your data warehouse (bigquery)
 - admin access to your repo, where you will have the dbt project. 

 <br>

![ae12](images/ae12.jpg)
<br><br>

Add new connection --> Select BigQuery
 <br>

![ae13](images/ae13.jpg)
<br><br>

Click on Upload a Service Account JSON file --> upload the json from step 2

Click on Save

Back on your project setup, select BigQuery:

 <br>

![ae14](images/ae14.jpg)
<br><br>

Click on save

Test the connection and click on save the Development credentials, not necessary to change those values:

 <br>

![ae14](images/ae36.jpg)
<br><br>


Now its time to setup a repository:
 <br>

![ae15](images/ae15.jpg)
<br><br>

Select git clone and paste the SSH key from your repo:

![ae16](images/ae16.jpg)
<br><br>

Click on import --> Click on next

You will get a deploy key:

 <br>

![ae17](images/ae37.jpg)
<br><br>

Head to your GH repo and go to the settings tab. You'll find the menu deploy keys. Click on add key and paste the deploy key provided by dbt cloud. Make sure to click on "write access":

 <br>

![ae17](images/ae38.jpg)
<br><br>

Back on dbt cloud, click on next, you should look this:


 <br>

![ae17](images/ae17.jpg)
<br><br>



Also make sure you informed taxi_rides_ny as the project subdirectory:

On the left sidebar, click on dashboard --> settings --> Edit

 <br>

![ae17](images/ae18.jpg)
<br><br>



**5: Create new branch**

On the left sidebar, click on Develop --> Cloud IDE


Create a new branch:

 <br>

![ae39](images/ae39.jpg)
<br><br>

I will use "dbt" branch. After creating the new branch, you can go to your repo on github and see the new branch created.

Note: it is important to create a new branch, because if we had chosen to work on the master branch we would get stuck in read-only mode.



## Development of dbt Models

_[Video source](https://www.youtube.com/watch?v=ueVy2N54lyc)_

Let's start now with the development of those DBT models. If we go back to the initial lessons, DBT sits on top of our platform, either BigQuery or Postgres.

We already loaded the raw data as the trips data. Now we're going to work on development, testing, and documentation. We'll start with development and by the end of these lessons, we'll deploy this into production to use those transformations in our BI tools.
 <br>

![ae21](images/ae21.jpg)
<br><br>

### Modular data modelling

To get started, we're going to use a modular data modeling approach. As we discussed in earlier lessons, we'll create fact tables and dimensional tables. The structure of our DBT project will look something like this:

- First, we have the tables we loaded (trips data). These are our sources.

- Then, we'll start building SQL scripts called "models" in DBT to perform transformations.

For example, we'll pick up the source data, clean it, deduplicate it, recast and rename columns, and typecast data. Afterward, we'll apply business logic to create fact and dimension tables. Finally, we'll create data marts to aggregate the data for our stakeholders.

We initially have tables that already exist outside our DBT project. These contain the data we will use, and we define them as sources. Additionally, we will use a file (e.g., taxi_zone_lookup) to create a table that will be incorporated into our transformations.

 <br>

![ae22](images/ae22.jpg)
<br><br>


### Anatomy of a dbt model

How does this look in each SQL file? Let's examine the anatomy of a DBT model:

 <br>

![ae25](images/ae25.jpg)
<br><br>

DBT models are SQL scripts. We'll always work with files named after the model, saved as .sql. Inside these files, we write SQL statements, primarily SELECT statements, because DBT handles the DDL (Data Definition Language) and DML (Data Manipulation Language) for us.

To tell DBT how to create the DDL and DML, we use configurations like this:

 <br>

![ae23](images/ae23.jpg)
<br><br>

This tells DBT to materialize the model as a table in the database. When you run dbt run, it compiles all the SQL files in your project. For example, the result might look like this:

 <br>

![ae24](images/ae24.jpg)
<br><br>

### Materializations in dbt cloud

There are mainly four types of materializations in DBT:

- Ephemeral: These are models that do not materialize in physical storage. They only exist within other models, similar to a Common Table Expression (CTE) if you're familiar with writing SQL.

- View: A view materializes in the database as a view. Every time you run dbt run, it creates or alters the view based on the SELECT statement in your file.

- Table: This materializes as a table in the physical database. Each time you run the model, DBT drops the existing table and recreates it with the CREATE TABLE AS SELECT statement, as shown earlier.

- Incremental: This is a more advanced materialization type. It also materializes as a table in the physical database, but instead of recreating the table entirely, it can work in two ways: Drop the table and recreate it with the SELECT statement or Insert only the new data into the table, allowing you to update the table incrementally.

### FROM clause of a dbt model

**1: sources**

We first select data from sources. This is the data we have already loaded, and we define it in a YAML file. In this file, we specify where to find the source, allowing us to define the data location only once. After that, we can reference all tables within that location using the definition.

This approach abstracts the complexity of where the source is physically stored, as we only define it once. When referencing it in the project, we use the source() function, providing the source name and the table name. DBT then compiles this reference into the appropriate database and schema location defined in the YAML file.

 <br>

![ae26](images/ae26.jpg)
<br><br>

Another benefit of defining sources in DBT is the ability to perform extensive testing on them. A key example is freshness testing. We can define a threshold for the freshness of our data, which is particularly useful in production pipelines. This helps identify outdated data before stakeholders notice it. The freshness threshold ensures we’re alerted if the data exceeds the defined acceptable age.

Additionally, we can use selection to run specific DBT models dependent on fresh data. Testing and validation of sources significantly improve data quality in our models, as we verify the integrity of the input data.

**2: seeds**

The second source of data we select from is **seeds**. Seeds are CSV files stored within our repository. When running dbt run on a seed, DBT executes an operation similar to a COPY INTO command in SQL.

The advantage of using seeds in DBT is that they are version-controlled and stored in the same repository as the rest of the DBT project. This ensures:

- Consistency and centralization of all project files.
- Integration with version control for better collaboration.
- Documentation and testing capabilities for the seed data.

Seeds are ideal for data that does not change frequently. For example, we can use a seed for a master data table, like taxi_zone_lookup, which is relatively small and benefits from version control.

**3: refs**

The other thing we can select from, continuing with the modular approach, is the DBT models themselves. For example, after working with sources and creating transformations to clean the green trip data and yellow trip data, we can move on to building fact or dimensional models.

 <br>

![ae27](images/ae27.jpg)
<br><br>

In these cases, we use the ref() function to reference the underlying tables. By specifying the name of the model within the ref() function, DBT compiles the code and determines the correct location for the referenced model.

This approach allows us to run the same code in any environment. For instance, when working locally, the model may go to a development schema like my_name_schema. In production, the same code will automatically point to a production schema. DBT abstracts the complexity of environment-specific configurations, enabling seamless execution across different environments.

Another benefit of using ref() is that it automatically builds dependencies between models. For example, if a new DBT model depends on the stg_green_tripdata model, DBT recognizes this relationship. This ensures that models are executed in the correct order during development and deployment, simplifying the process significantly.

 <br>

![ae28](images/ae28.jpg)
<br><br>


### Developing the first staging model

**schema.yml**

Under the models directory, there is a folder named staging. This will represent the initial layer of models responsible for cleaning the source data. Inside the staging folder, there is a schema.yml file for defining the sources:

```yaml

version: 2

sources:
  - name: staging
    database: zoomcamp-airflow-444903 
    schema: zoomcamp
      
    tables:
      - name: green_tripdata
      - name: yellow_tripdata

models:
    - name: stg_green_tripdata
    ...  
    - name: stg_yellow_tripdata
    ...
```      

> [!NOTE]  
> Make sure the values ​​in the YAML match the values ​​in your BigQuery!

Full code: [`schema.yml`](taxi_rides_ny/models/staging/schema.yml)


In this file, we'll define the sources and we'll define the database and schema where the data resides.
Next, we'll define the tables we want to use, such as green_tripdata and yellow_tripdata. Once defined, these sources can be referenced in our models. For example, we'll start by working with the green_tripdata.

One advantage of using DBT's approach is that it adheres to the DRY (Don't Repeat Yourself) principle. If we change the schema or table name in the YAML file, all dependent models will automatically update without requiring code changes in multiple places.

**model: stg_green_tripdata.sql**

Inside the staging folder, there is a stg_green_tripdata.sql file. This dbt model defines a SQL query that transforms and materializes data from a source table (green_tripdata) into a view in the database.

stg_green_tripdata.sql looks like this:

```sql

{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, lpep_pickup_datetime) as rn
  from {{ source('staging','green_tripdata') }}
  where vendorid is not null 
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} as tripid,
    {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,
    {{ dbt.safe_cast("ratecodeid", api.Column.translate_type("integer")) }} as ratecodeid,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,
    
    -- timestamps
    cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    {{ dbt.safe_cast("trip_type", api.Column.translate_type("integer")) }} as trip_type,

    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(ehail_fee as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
    {{ get_payment_type_description("payment_type") }} as payment_type_description
from tripdata
where rn = 1


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
```



**Step by step explanation of the model:**

```sql
{{
    config(
        materialized='view'
    )
}}
```

This sets the model to be materialized as a view. A view is a virtual table created dynamically by running the query each time it is accessed, rather than persisting data as a physical table.


```sql

with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, lpep_pickup_datetime) as rn
  from {{ source('staging','green_tripdata') }}
  where vendorid is not null 
)

```

- Data Source: Fetches data from the green_tripdata table in the staging schema using the {{ source() }} function, which references an external table defined in dbt's sources.

- Filtering: Excludes rows where vendorid is NULL.

- Deduplication: Uses the row_number() function to assign a unique row number (rn) within each group of records partitioned by vendorid and lpep_pickup_datetime. This helps to remove duplicates later.

The main SELECT statement transforms the cleaned data (tripdata) into a more structured and enriched dataset:

```sql
{{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} as tripid,
{{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,

```

- Generates a unique surrogate key (tripid) by combining vendorid and lpep_pickup_datetime using dbt's generate_surrogate_key utility.

- Safely casts vendorid to an integer using dbt's safe_cast() function.

```sql

cast(lpep_pickup_datetime as timestamp) as pickup_datetime,
cast(lpep_dropoff_datetime as timestamp) as dropoff_datetime,

```

- Converts datetime fields (lpep_pickup_datetime, lpep_dropoff_datetime) to timestamp format for consistent handling.

```sql

{{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
cast(trip_distance as numeric) as trip_distance,
```

- Casts fields like passenger_count and trip_distance to appropriate types (integer and numeric).

```sql

cast(fare_amount as numeric) as fare_amount,
coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
{{ get_payment_type_description("payment_type") }} as payment_type_description

```

- Handles financial data like fare_amount and tip_amount, casting them to numeric

- Uses coalesce() to ensure payment_type is never NULL, defaulting to 0

- Maps payment_type to a human-readable description using a custom function (get_payment_type_description).

Deduplication:

```sql

from tripdata
where rn = 1

```

- Ensures only the first record for each vendorid and lpep_pickup_datetime combination is included by filtering for rows where rn = 1.


### Macros

You may have noticed that I've been using elements enclosed in double curly brackets, such as {{ source() }} and {{ ref() }}. These are macros, and they allow us to dynamically generate SQL code. In DBT, the content inside double curly brackets is written in a templating language called Jinja. This language is similar to Python in its structure and enables us to define how DBT should compile the code.

Macros in DBT are essentially functions that generate code. Unlike functions in Python, the input and output of a macro result in dynamically generated SQL code. Macros are very useful for simplifying repetitive code, adhering to the DRY (Don't Repeat Yourself) principle, and enabling dynamic code generation. For example, you can use loops within a macro to generate complex SQL constructs like case statements.

Let’s create a macro called get_payment_type_description. It will take a parameter, such as payment_type, and generate a SQL case statement. The syntax for defining macros is similar to Python functions:

- Use macro to define the macro.
- Provide the macro's name.
- Specify its parameters.
- Include the SQL code to be dynamically generated


Here’s an example of get_payment_type_description.sql macro:

```sql

{#
    This macro returns the description of the payment_type 
#}

{% macro get_payment_type_description(payment_type) -%}

    case {{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }}  
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
        else 'EMPTY'
    end

{%- endmacro %}
```

This macro is designed to return the description of a given payment_type in a SQL context. It uses a CASE statement to map integer values of payment_type to their corresponding descriptions. 

- The macro uses dbt.safe_cast to ensure payment_type is safely converted to an integer (or a compatible type). This is useful for ensuring type compatibility in SQL.

- api.Column.translate_type("integer") helps translate the type definition for the database being used.

The macro outputs the resulting SQL CASE statement, which can then be embedded in a query to dynamically resolve the description of the payment type.

Example Usage:

 <br>

![ae30](images/ae30.jpg)
<br><br>


We can observe the macro in the stg_green_tripdata.sql file, line 42:

```sql

{{ get_payment_type_description("payment_type") }} as payment_type_description

```

The output of the macro is included in the query as a new column named payment_type_description. For instance:

 <br>

![ae31](images/ae31.jpg)
<br><br>


When compiled, DBT will replace the macro call with the actual SQL case statement. This approach saves time and effort when dealing with large-scale projects.

Macros can also be reused across projects by creating packages. A DBT package is similar to a library in other programming languages. It can contain models, macros, and other reusable components. By adding a package to your project, you can leverage its functionality anywhere in your codebase.

For example, if you find yourself frequently using a macro like get_payment_type_description across multiple projects, you can bundle it into a package and include it in your DBT projects using the packages.yml file.


### Packages

To start using DBT packages, you need to create a packages.yml file in your project. In this file, you define the packages you want to use. For example, you can include the GitHub or Git URL of a package. Fortunately, there are many pre-built packages available in the DBT Package Hub.

To use a package, you simply define it in your packages.yml. For example, you could import a package like this:


```yml

packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: dbt-labs/codegen
    version: 0.12.1
```

Once imported, you can use the macros from that package by calling them with a prefix. For instance, if you're using the dbt_utils package, you can call a macro like this:

```sql

{{ dbt_utils.surrogate_key(['field1', 'field2']) }}

```

Packages save you a lot of time by providing pre-built macros, tests, and utilities. They also allow for the reuse of common logic across projects. If your organization frequently uses specific macros (e.g., a macro for handling payment types), you can bundle them into an internal package and share it with other teams.

After defining the packages in packages.yml, you need to run the following command to install them:

```

dbt deps

```

This will download and install the packages into your project. You can find the installed packages and their macros under the dbt_packages directory.

Let’s use the generate_surrogate_key macro from the dbt_utils package. This macro creates a hashed surrogate key based on the specified fields. For example in the stg_green_tripdata.sql file:

```sql

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} as tripid,

from tripdata
```

This macro generates a hash of the vendor_id and pickup_datetime fields to create a unique identifier for each row. A good practice is to include this surrogate key at the beginning of your table, as it helps define the granularity of the data.

You can compile this code to see how it looks. The macro is applying an MD5 hash to the specified fields. If you're using a different database platform, the resulting code will adapt accordingly. For instance, the syntax might differ slightly in Postgres compared to BigQuery, but DBT's macros and adapters handle this automatically, abstracting the complexity for you.

Once compiled, you can view the resulting SQL code under the target/compiled folder in your project:

 <br>

![ae31](images/ae35.jpg)
<br><br>

This folder contains the exact SQL generated for your database, which is useful for debugging or understanding how the macros work.

### Variables

Now, let’s learn about variables. The concept of variables in DBT is similar to variables in any programming language. A variable acts like a container where you store a value that you want to use later, and you can access it whenever needed.

In DBT, variables can be defined at the project level within the dbt_project.yml file, allowing you to use them across various models or macros. For example, you might define a variable payment_type_values as a list of numbers:

```yaml

vars:
  payment_type_values: [1, 2, 3, 4, 5, 6]
```  

This list could be used in different scenarios, such as building a CASE statement by looping through the list. Running a test to check if the actual values in the table are part of the list or dynamically setting a variable's value within a macro using the var marker.

Additionally, you can pass a value for a variable during execution. This allows you to customize behavior dynamically at runtime. To access a variable, use the var() marker.

Here’s an example in stg_green_tripdata:

```sql

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
```


A conditional execution checks if a variable is_test_run is True. If it’s True, it adds LIMIT 100 to the query. If it’s False, the query proceeds without the limit. The code also defines a default value for is_test_run, which is True. This means that unless specified otherwise, LIMIT 100 will always be added by default.

To test this, you can run the code as it is and confirm that the LIMIT 100 is applied. If you don’t want the limit, you can override the variable during execution by passing a dictionary of variables. For example:

```
dbt run --vars '{"is_test_run": false}'
```

When this command is executed, the code no longer adds the LIMIT 100. This is a useful technique for development, as it allows you to test with smaller datasets (faster and cheaper queries) while ensuring full production data is used during deployment by setting is_test_run to False.

This method, often referred to as a "dev limit," is highly recommended for optimizing development workflows. By default, you’ll have faster and cheaper queries during development, but the limit can easily be removed when working with the full production data.


### Developing the second staging model

The next task is to create the staging file for yellow_trip_data. This is very similar to the previous file, so we won't go into detail about its structure. The code is almost identical, using the same macro.

There are a few differences: the staging file typically includes a straightforward CTE and doesn't use the same variables as before. However, the core SQL logic remains largely the same.

stg_yellow_tripdata.sql looks like this:

```sql

{{ config(materialized='view') }}
 
with tripdata as 
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('staging','yellow_tripdata') }}
  where vendorid is not null 
)
select
   -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'tpep_pickup_datetime']) }} as tripid,    
    {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,
    {{ dbt.safe_cast("ratecodeid", api.Column.translate_type("integer")) }} as ratecodeid,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,

    -- timestamps
    cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    -- yellow cabs are always street-hail
    1 as trip_type,
    
    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(0 as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    coalesce({{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }},0) as payment_type,
    {{ get_payment_type_description('payment_type') }} as payment_type_description
from tripdata
where rn = 1

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
```

## Core Models

So far, our project looks like this: we have our two sources and a set of models. Now, we need to create our fact and dimensional tables

 <br>

![ae40](images/ae40.jpg)
<br><br>

### Dim zones

The goal for dim_zones is to act as a master data table containing all the zone information where the taxis operate. These taxis move within specific zones, and we want to ensure we have accurate information about them.

Since we don’t have source data for this, we’ll use the seeds mentioned earlier. For this, we'll leverage the taxi_zone_lookup file. It’s unlikely that this data will change frequently.

We’ll copy this data, save it as a CSV file, and include it in our project under the seeds folder. The file is named taxi_zone_lookup.csv, and it can be downloaded directly from GitHub if needed. Once saved, the seed file will have a distinct icon in the project, and we can preview the data.

The seed contains fields like location_id, which is also present in both the green and yellow trip data. This will allow us to connect the data with the taxi_zone_lookup table for additional context. The dim_zones model is under the core folder.

dim_zones.dql looks like this:

```sql

{{ config(materialized='table') }}

select 
    locationid, 
    borough, 
    zone, 
    replace(service_zone,'Boro','Green') as service_zone 
from {{ ref('taxi_zone_lookup') }}
```

The dim_zones model will use data from taxi_zone_lookup. It will define fields like location, borough, and service_zone. Additionally, we’ll address an issue where all entries labeled as "Borough" were actually "Green Zones," which only green taxis operate in. We'll clean up the data by renaming those values for easier analytics.

So far, our project looks like this:

 <br>

![ae31](images/ae42.jpg)
<br><br>


### Fact trips

With dim_zones, we are ready to create the next step: a fact table for trips (fact_trips). We will combine the green and yellow trip data, encase it with dimensional data, and materialize it as a table. Materializing it as a table ensures better performance for analytics since this table will be large due to unions and joins.

fact_trips.sql model goal is to:

- Combine both green and yellow trip data.
- Add a field to identify whether a record is from the green or yellow dataset for easier analysis.
- Join this data with the dim_zones model to enrich it with pickup and drop-off zone details.


fact_trips.sql looks like:

```sql

{{
    config(
        materialized='table'
    )
}}

with green_tripdata as (
    select *, 
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
), 
yellow_tripdata as (
    select *, 
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
), 
trips_unioned as (
    select * from green_tripdata
    union all 
    select * from yellow_tripdata
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select trips_unioned.tripid, 
    trips_unioned.vendorid, 
    trips_unioned.service_type,
    trips_unioned.ratecodeid, 
    trips_unioned.pickup_locationid, 
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    trips_unioned.dropoff_locationid,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    trips_unioned.pickup_datetime, 
    trips_unioned.dropoff_datetime, 
    trips_unioned.store_and_fwd_flag, 
    trips_unioned.passenger_count, 
    trips_unioned.trip_distance, 
    trips_unioned.trip_type, 
    trips_unioned.fare_amount, 
    trips_unioned.extra, 
    trips_unioned.mta_tax, 
    trips_unioned.tip_amount, 
    trips_unioned.tolls_amount, 
    trips_unioned.ehail_fee, 
    trips_unioned.improvement_surcharge, 
    trips_unioned.total_amount, 
    trips_unioned.payment_type, 
    trips_unioned.payment_type_description
from trips_unioned
inner join dim_zones as pickup_zone
on trips_unioned.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on trips_unioned.dropoff_locationid = dropoff_zone.locationid
```

- Select all fields from both the green and yellow trip data using ref() for references and add a service_type column to distinguish the datasets.

- Union the data to create a combined dataset (trips_union).

- Join trips_union with dim_zones for both pickup and drop-off zones to associate zone names and other details. Only valid zones will be included (e.g., exclude unknown zones).

When we run the model with the full production dataset, the resulting table will contain millions of rows, representing a comprehensive and enriched fact table. This table is now ready for use in analysis or as a source for BI tools.

With all of this, the fact_trips table is complete, and we can proceed to testing and further analysis.

So far, our project looks like this:

 <br>

![ae31](images/ae43.jpg)
<br><br>

We can check the lineage to see how the modular data modeling looks. Now, we can observe that fact_trips depends
on all the required models. One of the great features of dbt is that it identifies all these connections. This
means we can run fact_trips, but first, dbt will execute all its parent models. dbt will test the sources for 
freshness or other requirements, run any missing or outdated models, and only then build fact_trips.

The final step is to test these models to ensure that all rows and calculations—totaling 62.7 million—are correct 
before delivering the results.

### Monthly zone revenue

This is a dbt model that creates a table summarizing revenue-related metrics for trips data as a table selecting data from our previous dbt model called fact_trips.

This model creates a table with monthly revenue metrics per pickup zone and service type, including various fare components, trip counts, and averages.

It enables analysis of revenue trends, passenger patterns, and trip details across zones and services, giving a clear breakdown of monthly performance.

dm_monthly_zone_revenue.sql looks like:

```sql

{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fact_trips') }}
)
    select 
    -- Reveneue grouping 
    pickup_zone as revenue_zone,
    {{ dbt.date_trunc("month", "pickup_datetime") }} as revenue_month, 

    service_type, 

    -- Revenue calculation 
    sum(fare_amount) as revenue_monthly_fare,
    sum(extra) as revenue_monthly_extra,
    sum(mta_tax) as revenue_monthly_mta_tax,
    sum(tip_amount) as revenue_monthly_tip_amount,
    sum(tolls_amount) as revenue_monthly_tolls_amount,
    sum(ehail_fee) as revenue_monthly_ehail_fee,
    sum(improvement_surcharge) as revenue_monthly_improvement_surcharge,
    sum(total_amount) as revenue_monthly_total_amount,

    -- Additional calculations
    count(tripid) as total_monthly_trips,
    avg(passenger_count) as avg_monthly_passenger_count,
    avg(trip_distance) as avg_monthly_trip_distance

    from trips_data
    group by 1,2,3
```    

The main query groups the data by:

- Pickup zone (pickup_zone) → Labeled as revenue_zone.
- Month of the pickup date (pickup_datetime) → Labeled as revenue_month 
- Service type (service_type) → Such as economy, premium, etc.

For each group, the query calculates revenue-related metrics like revenue_monthly_fare (Sum of fare_amount), revenue_monthly_extra (Sum of additional fees), etc and other metrics like total_monthly_trips (Count of trips), avg_monthly_passenger_count (Average number of passengers per trip) and avg_monthly_trip_distance (Average distance per trip).

Finally, The GROUP BY 1, 2, 3 clause organizes the results by the specified dimensions (pickup zone, revenue month, and service type). Each calculation is applied within these groups. 1 refers to pickup_zone, 2 refers to the truncated month of pickup_datetime, 3 refers to service_type.

So far, our project looks like this:

 <br>

![ae31](images/ae47.jpg)
<br><br>


## Building the model

**1: schema.yml values**

Open VS Code, go to taxi_rides_ny --> models --> staging --> schema.yml

Make sure that project id, dataset name and tables matches your project id, dataset and tables name in BigQuery!

```yaml

sources:
  - name: staging
    database: zoomcamp-airflow-444903 # project id
    schema: zoomcamp # dataset name
     
    tables:
      - name: green_tripdata #table name
      - name: yellow_tripdata #table name
```

Values check:

 <br>

![ae22](images/ae29.jpg)
<br><br>

**2: dbt build**

In the dbt cloud console, run:

```
dbt build
```

You should look something like this:
 <br>

![ae31](images/ae20.jpg)
<br><br>

 <br>

After running the model (dbt build), the process should complete successfully, creating a view. You can check the view details to confirm the output, including the trip_id and other data fields. You can also examine the compiled SQL in the target/compiled folder for additional troubleshooting.

When you run dbt build in dbt Cloud, it does the following:

- Builds Models: Executes the SQL transformations defined in your project to create or update tables and views in your target data warehouse.

- Runs Tests: Validates data quality by executing both custom tests (defined in .yml files) and standard tests (like unique or not null constraints).

- Updates Snapshots: Captures historical changes in your source data for versioning and time-based analytics.

- Loads Seeds: Loads any seed files (like .csv files) defined in your project into the target data warehouse.


By default, only 100 rows are processed in the query for testing purposes. This is controlled by the is_test_run variable, which defaults to true in stg_green_tripdata.sql and stg_yellow_tripdata models:

```python

{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
```


To run the query without this limit and process the full dataset in production, you need to explicitly set the variable to false by using the following command:

```
dbt build --select +fact_trips.sql+ --vars '{is_test_run: false}'
```

This ensures that the model processes the entire dataset

**3: Check BigQuery**

Head over to BigQuery and check the views that dbt generated:

 <br>

![ae31](images/ae32.jpg)
<br><br>

 <br>

![ae31](images/ae33.jpg)
<br><br>

 <br>

![ae31](images/ae34.jpg)
<br><br>

Dim_zones:

 <br>

![ae31](images/ae41.jpg)
<br><br>

Fact_trips:

 <br>

![ae31](images/ae44.jpg)
<br><br>

dm_monthly_zone_revenue:

 <br>

![ae31](images/ae48.jpg)
<br><br>


## Testing

_[Video source](https://www.youtube.com/watch?v=2dNJXHFCHaY)_

We have many models now, but how do we ensure that the data we deliver to the end user is correct? More importantly, how do we make sure that we don't build models on top of incorrect data? We need to identify errors quickly. For this reason, we can use DBT tests.

DBT tests are assumptions we make about our data. They're essentially statements that select data we don’t want to have. If the query produces results, the test fails and stops execution immediately, preventing the building of dependent models. For example, when building a project, if the query returns no results, the test passes, the data is good, and no alerts are triggered.

These assumptions are primarily defined in YAML files like our schema.yml and are compiled into SQL code. DBT comes with four out-of-the-box tests:

- Unique Test - Ensures the uniqueness of a field in the data model.
- Not Null Test - Verifies that a field does not contain null values.
- Accepted Values Test - Checks if a field contains only predefined valid values.
- Foreign Key Test - Ensures relationships between fields in different tables are valid.

For example, the "Accepted Values" test might ensure that a field like payment_type only contains values 1, 2, 3, 4, or 5. If it’s outside this range, the test will fail:

```yaml

          - name: payment_type
            description: A numeric code signifying how the passenger paid for the trip.
            tests:
              - accepted_values:
                  values: [1,2,3,4,5]
                  severity: warn

```            


Another test ensures that pickup_location has a valid relationship to the ref_taxi_lookup table, verifying it corresponds to a valid taxi zone:

```yaml

          - name: Pickup_locationid
            description: locationid where the meter was engaged.
            tests:
              - relationships:
                  to: ref('taxi_zone_lookup')
                  field: locationid
                  severity: warn
```                  

Similarly, trip_id must be unique and not null, as it’s the primary key:

```yaml

          - name: tripid
            description: Primary key for this table, generated with a concatenation of vendorid+pickup_datetime
            tests:
                - unique:
                    severity: warn
                - not_null:
                    severity: warn
```                    

When these tests are compiled, they generate SQL code like this:

 <br>

![ae45](images/ae45.jpg)
<br><br>


If there are no results, the data is valid. Otherwise, it will produce warnings, helping us identify and fix issues in our data quickly:

 <br>

![ae46](images/ae46.jpg)
<br><br>


## Documentation

_[Video source](https://www.youtube.com/watch?v=2dNJXHFCHaY)_

dbt also provides a way to generate documentation for your dbt project and render it as a website. The dbt generated docs will include the following:

- Information about the project:
  - Model code (both from the .sql files and compiled code)
  - Model dependencies
  - Sources
  - Auto generated DAGs from the ref() and source() macros
  - Descriptions from the .yml files and tests

- Information about the Data Warehouse (information_schema):
  - Column names and data types
  - Table stats like size and rows

dbt docs can be generated on the cloud or locally with this command:

```
dbt docs generate
```

## Deployment

_[Video source](https://www.youtube.com/watch?v=V2m5C0n8Gro)_

We now have our whole project, so it's time to take it into production, analyze the data, and serve it to our 
stakeholders. If we recall what we learned about dbt at the very beginning, we introduced layers to our 
development. We’ve already seen how to handle development, testing, and documentation, all happening in our 
development environment.

Now, to take it into production, we go through a process called deployment. This involves taking all our code, 
opening a pull request, and merging the code into the main branch, which affects our production environment. 
In production, we’ll run the models, but there will be some differences.

For example, during development, we often limit the data. In production, we need all the data without limits. 
Additionally, in a real-life production scenario, not everyone will have the same access rights. Not everyone 
will be able to write or read all the data. This is likely handled in a different database or schema with 
specific access controls.

The deployment workflow works as follows:

- Development is done in custom branches. Each team member works in their own development branch.

- Meanwhile, production continues using the main branch, unaffected by the development branches.

- When a development branch is ready for production, a pull request is opened.

- Once approved, the code is merged into the main branch.

- Run the new models in the production environment using the main branch.

- Schedule the models updating on a nightly, daily or hourly basis to keep the data up to date.

### Running a dbt project in production

We are now going to discuss how to run projects in production. First, under the environment settings, we create
 a new deployment environment called "production." This environment is labeled as a deployment and categorized 
 under "prod." Once saved, we're ready to create our first job.

We’ll create a deployment job that runs, for example, nightly. This is where the data transitions to the 
production environment. By default, it includes a dbt build step, but this can be customized. Within the 
deployment process, we can create dbt jobs that run multiple commands. A single job can execute multiple steps,
 such as *dbt build*, *dbt test*, *dbt seed*, or *dbt source freshness*. These runs can be triggered manually, on a 
 scheduled basis (e.g., using a cron schedule), or via an API.

During execution, these jobs generate metadata that can be used for monitoring and alerting the data platform. 
In a real-world scenario, this is crucial for ensuring reliability and visibility. For instance, we can perform
 a complete dbt build, generate documentation for production, and ensure that documentation is accessible to 
 everyone on the team. We can also run dbt source freshness to validate source data.

The scheduled runs can be set up to occur daily at a specific time, excluding weekends if no data is received on
 Saturdays or Sundays. Advanced settings include options like timeout configurations and the number of models 
 to run in parallel. Once saved, jobs can also be triggered on an ad hoc basis.

For API-based triggering, tools like Airflow, Prefect, or Mage can integrate seamlessly with dbt runs. For 
example, a pipeline could load fresh data into BigQuery and then trigger a dbt run to process it.

After a job is triggered, we can monitor its status. For example, we can view the commit hash associated with 
the run to see exactly what changes were made in the repository. We can also track the duration of the job and 
the steps it performed. These include cloning the repository, establishing a connection to the data platform 
(e.g., BigQuery), installing packages with dbt deps, running source freshness checks, and executing the dbt 
build.

At the end of the process, the system generates documentation and artifacts such as catalog.json and other 
metadata files. These files can be analyzed or hosted for further use. The documentation can be made accessible
 under the settings by defining which job is used to generate it. Once configured, the documentation is readily 
 available in production, which is invaluable for team collaboration and exposing data sources.

This workflow ensures that all documentation, data sources, and metadata from production runs are centralized,
 making it easier to share insights and maintain consistency across the team.

### Continuous Integration


Another important feature we can implement is creating a continuous integration (CI) job. When working with 
pull requests, it's essential to ensure automation and quality through CI/CD practices.

What is CI/CD?

- CI (Continuous Integration): Regularly merging code changes into the main branch while automating builds and
 tests to avoid breaking production.

- CD (Continuous Deployment): Automating the deployment process after the changes pass tests.

The goal is to ensure code is integrated and deployed smoothly without affecting production or development
 environments. dbt Cloud makes it simple to implement this process.

Setting Up CI in dbt Cloud

1. Create a CI Job:

- This job is triggered by pull requests and helps prevent breaking production.
- For example, dbt Cloud creates a schema named dbt_cloud_PR_<PR_name> for the pull request. This schema is 
automatically dropped when the pull request is closed, ensuring that production and development environments 
remain unaffected.

2. Default and Custom Commands:

- By default, it runs commands on modified models and their dependencies.
- Additional steps can be included, such as dbt test, which can enforce documentation or other requirements for
 models.

3. Advanced Settings:

- Define the number of threads, timeouts, or other configurations to optimize the job's performance.

Example Workflow

- Open a pull request for a code change (e.g., fixing a "drop-off location" field mistakenly labeled as "pick-up
 location").

- Commit the fix and link it to the pull request.

- dbt Cloud, already connected to the repository, automatically detects the changes and triggers the CI job.

- The job compares the changes to the nightly production run, identifies affected models (e.g., fact_trips), 
and executes tasks only for these models and their children.

- Once the job completes successfully, the pull request can be merged, building trust in the process and ensuring
 data accuracy.

Benefits of CI Jobs in dbt Cloud:

- Automates tests and builds, reducing manual effort and errors.
- Prevents breaking production by isolating changes in a temporary schema.
- Builds confidence in the integration and deployment process.
- Streamlines collaboration within the team by ensuring consistent workflows.

In this case, the process detected the modified fact_trips model and its children, ran the required tasks, and
 displayed a successful check. The fix was verified and ready for deployment, illustrating how CI jobs make the 
 workflow efficient and reliable.

## Visualising the transformed data 

_[Video source](https://www.youtube.com/watch?v=39nLTs74A3E)_

Now that we created our models and transformed our data, we are now going to visualize this data.

### 1: Process the full dataset

Before you start with the visualization, make sure that you have processed all the data without the limit of 100
 in the stg_green_tripdata.sql and stg_yellow_tripdata.sql models.

To run the query without this limit and process the full dataset in production, you need to explicitly set the 
variable to false by using the following command: 

```
dbt build --select +fact_trips.sql+ --vars '{is_test_run: false}'
```

### 2: Open [Looker Studio](https://lookerstudio.google.com/).

Looker Studio (formerly known as Google Data Studio) is a free tool by Google that allows you to create 
interactive dashboards and visualizations of data. It enables users to connect various data sources—such as
 Google Sheets, Google Analytics, BigQuery, and more—and transform raw data into visually engaging reports 
 that are easy to share and understand.

### 3: Create a BigQuery data source 

On the left sidebar, click on Create --> Data source

 <br>

![ae49](images/ae49.jpg)
<br><br>

Select BigQuery (it may be necessary to authorize Google Data Studio to access BigQuery)

Then select fact_trips from your project

 <br>

![ae50](images/ae50.jpg)
<br><br>

Click on Connect

### 4: Set Default aggregations

 in the next screen, we can see that the tool already suggests some aggregations for us. In this example, we set
  all of them to None, except for passenger_count, for which we keep the "Sum" aggregation.

   <br>

![ae51](images/ae51.jpg)
<br><br>

Then click on CREATE REPORT --> Add report

### 5: Add a date range control 

First, eliminate the default chart. Then click on Add a control --> Date range control

- Select start date Jan 1, 2019
- Select end date Dec 31, 2020

   <br>

![ae52](images/ae52.jpg)
<br><br>

### 6: Add a time series chart

Select Add a chart --> Time series chart

   <br>

![ae53](images/ae53.jpg)
<br><br>

Let's add a breakdown dimension

On the rigth menu, click on add dimension --> drag and drop service_type

   <br>

![ae53](images/ae54.jpg)
<br><br>

The chart now should look like this:

   <br>

![ae55](images/ae55.jpg)
<br><br>

If you look at the graph, the drop that you can see in march because of covid


### 7: Add a scorecard

Select Add a chart --> Scorecard with compact numbers

   <br>

![ae56](images/ae56.jpg)
<br><br>

### 8: Add a pie chart

Select Add a chart --> pie chart

<br>

![ae57](images/ae57.jpg)
<br><br>


### 9: Add a table with heatmap

Select Add a chart --> table with heatmap

Select pickup_zone as dimension

<br>

![ae58](images/ae58.jpg)
<br><br>

The table should look like this:

<br>

![ae59](images/ae59.jpg)
<br><br>

### 10: Add a stacked column chart

Select Add a chart --> stacked column chart

We will also add a Stacked Column Bar showing trips per month. Since we do not have that particular dimension, 
what we can do instead is to create a new field that will allow us to filter by month:

1. In the Available Fields sidebar, click on Add a field at the bottom --> Add calculated field
2. Name the new field pickup_month.
3. In the Formula field, type MONTH(pickup_datetime).
4. Click on Save and then on Done.
5. Back in the main page, drag the new pickup_month field  to the Dimension field. 
6. Get rid of all breakdown dimensions.

Our bar chart will now display trips per month but we still want to discriminate by year:

7. Add a new field and name it pickup_year.
8. Type in the formula YEAR(pickup_datetime).
9. Click on Save and Done.
10. Add the pickup_year field as a breakdown dimension for the bar chart.
11. Change the Sort dimension to pickup_month and make it ascending.

<br>

![ae60](images/ae60.jpg)
<br><br>

The table should look like this:

<br>

![ae61](images/ae61.jpg)
<br><br>