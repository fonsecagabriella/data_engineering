# DBT Fundamentals

## Vocabulary

- **DAG:** Directed Acyclic Graph

## Overview of a project

green node: came from a data source
blue node: you create in DBT

<img src="../images/dbd-lineage-graph.png" width="70%">

`dbt run` from left to right, it build the (staged) models
`dbt test` tests the models while they are being built
`dbd docs generate` 

## dbd Cloud and BigQuery