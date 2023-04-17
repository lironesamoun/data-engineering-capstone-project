# data-engineering-capstone-project

Cloud: GCP
Infrastructure as code (IaC): Terraform
Workflow orchestration: Prefect
Data Wareshouse: BigQuery
Data transformation: DBT
Batch processing: Spark

Problem description
[Problem is well described and it's clear what the problem the project solves]

Cloud
[The project is developed in the cloud and IaC tools are used]

Data ingestion: Batch / Workflow orchestration
[End-to-end pipeline: multiple steps in the DAG, uploading data to data lake]

Data warehouse
[Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)]

Transformations (dbt, spark, etc)
[Tranformations are defined with dbt, Spark or similar technologies]

Dashboard
[A dashboard with 2 tiles]

Reproducibility
[Instructions are clear, it's easy to run the code, and the code works]



to do
services account IAM
Create a new service account
    BigQuery Admin
    Storage Object Admin
    Compute Storage Admin

Create and download the json key file


dbt run --select global_terrorism_lite --vars '{"is_test_run": "true"}'