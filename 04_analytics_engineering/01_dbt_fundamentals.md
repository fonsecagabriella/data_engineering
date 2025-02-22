# DBT Fundamentals


## INDEX 📝

1.  **Vocabulary**
    * [DAG (Directed Acyclic Graph)](#vocabulary)
2.  **Overview of a project**
    * [Lineage Graph Explanation](#overview-of-a-project)
    * [Green Nodes (Raw Data)](#overview-of-a-project)
    * [Blue Nodes (DBT Created)](#overview-of-a-project)
3.  **dbt Project Structure Summary**
    * [Staging Models (`/staging/`)](#1-staging-models-staging)
        * [Purpose](#1-staging-models-staging)
        * [Characteristics](#1-staging-models-staging)
        * [Examples](#1-staging-models-staging)
        * [Location in Lineage Graph](#1-staging-models-staging)
    * [Core Models (`/core/`)](#2-core-models-core)
        * [Purpose](#2-core-models-core)
        * [Characteristics](#2-core-models-core)
        * [Examples](#2-core-models-core)
        * [Location in Lineage Graph](#2-core-models-core)
    * [Seed Files (`/seeds/`)](#3-seed-files-seeds)
        * [Purpose](#3-seed-files-seeds)
        * [Characteristics](#3-seed-files-seeds)
        * [Examples](#3-seed-files-seeds)
        * [Location in Lineage Graph](#3-seed-files-seeds)
4.  **Simple commands**
    * [`dbt run`](#simple-commands)
    * [`dbt test`](#simple-commands)
    * [`dbt docs generate`](#simple-commands)
    * [`dbt build --select +fact_trips.sql+ --vars '{is_test_run: false}'`](#simple-commands)
5.  **dbt run vs. dbt build**
    * [`dbt run` Explanation](#dbt-run-vs-dbt-build)
    * [`dbt build` Explanation](#dbt-run-vs-dbt-build)
    * [Key Differences](#dbt-run-vs-dbt-build)
    * [Simple Terms Summary](#dbt-run-vs-dbt-build)
6.  **Building Up to a Specific Node in dbt (run or build)**
    * [Key Points ( `+` prefix, `+` suffix, `--exclude`)](#building-up-to-a-specific-node-in-dbt-run-or-build)
    * [Build with Dependencies](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)
    * [Build Only the Node](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)
    * [Build Node and Immediate Children](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)
    * [Build Nodes in a Directory](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Build Nodes in a Directory with Downstream Dependencies](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)
    * [Exclude Nodes](#building-up-to-a-specific-node-in-dbt-run-or-build)
        * [Command and Example](#building-up-to-a-specific-node-in-dbt-run-or-build)

-----


## Vocabulary

- **DAG:** Directed Acyclic Graph. A DAG is just a **way to organize tasks (like cooking or transforming data) so that they happen in the right order**, without any repeating steps. It's like a flowchart for your data.

## Overview of a project

green node: came from a data  (connect to stage nodes directly)
blue node: you create in DBT (core)

<img src="../images/dbd-lineage-graph.png" width="70%">

### dbt Project Structure Summary

#### 1. Staging Models (`/staging/`)

* **Purpose:**
    * Transform raw data sources into a usable format.
    * Initial cleaning and standardization.
* **Characteristics:**
    * Minimal transformations (renaming, casting, filtering).
    * Directly reflect source table structure.
    * First step in the transformation pipeline.
* **Example:**
    * `stg_green_tripdata.sql`
    * `stg_yellow_tripdata.sql`
* **Location in Lineage Graph:**
    * Directly connected to raw data sources.

#### 2. Core Models (`/core/`)

* **Purpose:**
    * Implement core business logic.
    * Create dimension and fact tables.
* **Characteristics:**
    * Complex transformations (joins, aggregations, calculations).
    * Represent key business entities and relationships.
    * Used for analytics.
* **Example:**
    * `dim_customers.sql`
    * `fct_orders.sql`
    * `dim_taxi_trips.sql`
    * `fct_taxi_monthly_zone_revenue.sql`
* **Location in Lineage Graph:**
    * Downstream from staging models.
    * Often involve joins and aggregations.

#### 3. Seed Files (`/seeds/`)

* **Purpose:**
    * Load static data (lookup tables, mappings) into the data warehouse.
* **Characteristics:**
    * Data stored in `.csv` files.
    * Materialized as tables.
    * Used for dimension tables or reference data.
* **Example:**
    * `taxi_zone_lookup.csv`
* **Location in Lineage Graph:**
    * Starting point for dimension models.
    * Independent of raw data sources.

-----

## Simple commands

`dbt run` from left to right, it build the (staged) models

`dbt test` tests the models while they are being built

`dbt docs generate` generates docs, locally or on cloud

`dbt build --select +fact_trips.sql+ --vars '{is_test_run: false}'` command with a variable that be manipulated

----


## dbt run vs. dbt build

* **`dbt run`:**
    * Executes SQL models to create or replace tables/views.
    * Focuses solely on model materialization.
    * Use for transforming data via models.
* **`dbt build`:**
    * A comprehensive command that executes models, seeds, snapshots, and tests.
    * Covers a broader range of dbt operations.
    * Use for complete project execution and CI/CD pipelines.

**Key Differences:**

* `dbt run` is for model execution; `dbt build` is for full project execution.
* `dbt build` includes the functionality of `dbt run` and adds seed loading, snapshotting, and testing.

**In Simple Terms:**

* `dbt run` = "Build my models."
* `dbt build` = "Build and test everything."

---

## Building Up to a Specific Node in dbt (run or build)

**Key Points:**

* Use `+` prefix to include upstream dependencies.
* Use `+` suffix to include immediate downstream dependencies.
* Use `--exclude` to remove specific nodes.
* These selection principles apply to both dbt run, and dbt build.

**Build with Dependencies:**
    * `dbt build --select +model.node_name` (or `dbt run`)
    * Builds the specified node and all its upstream dependencies.
    * Example: `dbt build --select +model.fct_taxi_monthly_zone_revenue`

**Build Only the Node:**
    * `dbt build --select model.node_name` (or `dbt run`)
    * Builds only the specified node, excluding dependencies.
    * Example: `dbt build --select model.fct_taxi_monthly_zone_revenue`

**Build Node and Immediate Children:**
    * `dbt build --select model.node_name+` (or `dbt run`)
    * Builds the specified node and its direct downstream dependencies.
    * Example: `dbt build --select model.dim_taxi_trips+`

**Build Nodes in a Directory:**
    * `dbt build --select models/directory_name` (or `dbt run`)
    * Builds all nodes in the specified directory.
    * Example: `dbt build --select models/staging`
    * `dbt build --select models/directory_name/+` (or `dbt run`)
    * Builds all nodes in the directory and all downstream dependencies.
    * Example: `dbt build --select models/staging/+`


**Exclude Nodes:**
    * `dbt build --select +model.node_name --exclude model.exclude_node` (or `dbt run`)
    * Builds the selected node and its dependencies, excluding the specified node.
    * Example: `dbt build --select +model.fct_taxi_monthly_zone_revenue --exclude model.dim_zone_lookup`


