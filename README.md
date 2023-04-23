# Data Engineering Captsone Project - Exploring Global Terrorism Dataset

## Preface

This repository contains the course project for the Data Engineering Zoomcamp (Cohort 2023) organized by the by
DataTalks.Club community. The project covers main data engineering skills taught in the course:

- Cloud: `Google Cloud`
- Infrastructure: `Terraform`
- Orchestration: `Prefect`
- Data lake: `Google Cloud Storage`
- Data transformation: `DBT`
- Data warehouse: `BigQuery`
- Data visualization: `Google Looker Studio`

<b>TL;DR</b>: This project is analyzing the Global terrorism Dataset. Follow the steps mentioned
under `How to make it work?` to set it up.

## Dataset description

### Global Terrorism Dataset

The data has been downloaded from the [Global Terrorism Database (GTD)](https://www.start.umd.edu/gtd/)

The Global Terrorism Database™ (GTD) is an open-source database including information on terrorist events around the
world from 1970 through 2021 (with annual updates planned for the future). Unlike many other event databases, the GTD
includes systematic data on domestic as well as international terrorist incidents that have occurred during this time
period and now includes more than 200,000 cases

Statistical information contained in the Global Terrorism Database is based on reports from a variety of open media
sources. Information is not added to the GTD unless and until we have determined the sources are credible. Users should
not infer any additional actions or results beyond what is presented in a GTD entry and specifically, users should not
infer an individual associated with a particular incident was tried and convicted of terrorism or any other criminal
offense. If new documentation about an event becomes available, an entry may be modified, as necessary and appropriate.

**Characteristics of the GTD**

- Contains information on over 200,000 terrorist attacks
- Currently the most comprehensive unclassified database on terrorist attacks in the world
- Includes information on more than 88,000 bombings, 19,000 assassinations, and 11,000 kidnappings since 1970
- Includes information on at least 45 variables for each case, with more recent incidents including information on more than 120 variables
- More than 4,000,000 news articles and 25,000 news sources were reviewed to collect incident data from 1998 to 2017 alone

### Dataset Structure

##

## Architecture

![architecture-captstone-project](https://user-images.githubusercontent.com/8614763/233844475-c1cd6fc8-76f7-4c45-851b-fab24629039d.jpeg)

### What technologies are being used?

- Cloud: `Google Cloud`
- Infrastructure: `Terraform`
- Orchestration: `Prefect`
- Data lake: `Google Cloud Storage`
- Data transformation: `DBT`
- Data warehouse: `BigQuery`
- Data visualization: `Google Looker Studio`

## What questions am I trying to answer?

- Which countries have had the most attacks?
- Which cities have had the most attacks?
- What is the most common type of attack?
- What are the main reasons for these attacks?
- What are the main targets?
- Who are the main perpetrators?
- The total number of deaths since the beginning
- The number of deaths per country


### Repository organization

## Data visualization: Dashboards

[Click here](https://lookerstudio.google.com/reporting/5436069c-3071-4119-88b0-dc0a27c547ff) to see the Looker
dashboard.

## How to reproduce this project?

**Step 1: Clone this repo and install necessary requirements**

1. Clone the repo into your local machine:
```bash
git clone https://github.com/lironesamoun/data-engineering-capstone-project.git
```
2. Install all required dependencies into your environment
```bash
pip3 install -r requirements.txt
```

## TODO create make for installation (virtual env + installatino requirements)

#### Step 2: Setup of GCP
1. Create a [Google Cloud Platform (GCP)](https://cloud.google.com/) free account with your Google e-mail
2. Create a new GCP project with the name **de-capstone-project-23** (Note: Save the assigned Project ID. Projects have a unique ID and for that reason another ID will be assigned)
3. Create a Service Account:
    - Go to **IAM & Admin > Service accounts > Create service account**
    - Provide a service account name and grant the roles: **Viewer** + **BigQuery Admin** + **Storage Admin** + **Storage Object Admin**
    - Download the Service Account json file
    - Download [SDK](https://cloud.google.com/sdk/docs/install-sdk) for local setup
    - Set environment variable to point to your downloaded GCP keys:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
    ```
    ```bash
    # Refresh token/session, and verify authentication
    gcloud auth application-default login
    ```

4. Enable the following APIs:
    - [Identity and Access Management (IAM) API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
    - [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)


#### Step 3: Creation of a GCP Infrastructure
1. Install [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
2. Copy files (**main.tf** and **variables.tf**) for the infrastructure creation (Use files created in Zoomcamp course: [Terraform files](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform))
3. In the file variables.tf change variable **BQ_DATASET** to: **us_traffic_accidents_data**
4. Execute the following commands to plan the creation of the GCP infrastructure:
```bash
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
# -var="project=<your-gcp-project-id>"

terraform plan -var="project=dezoomcamp-finalproject"
```

```bash
# Create new infra
# -var="project=<your-gcp-project-id>"

terraform apply -var="project=dezoomcamp-finalproject"
```

It is possible to see in the GCP console that the Infrastructure was correctly created.

#### Step 4: Setup orchestration using Prefect
1. Setup the prefect server so that you can access the UI. Run the following command in a CL terminal:
```bash
make prefect-init
make prefect-start
 ```
2. Access the UI in your browser: **http://127.0.0.1:4200/**
3. For the connection with GCP Buckets it is necessary to init prefect blocks

```bash
python3 src/blocks/init_prefect_blocks.py
 ```

4. To execute the flow, run the following commands in a different CL terminal than step 1:
```bash
python3 src/flows/parameterized_flow_http_pipeline.py
 ```

#### Step 5: Running the dbt flow
1. Create a [dbt cloud](https://www.getdbt.com/product/what-is-dbt/) free account
2. Clone this repo
3. In the command line of dbt running the following command:
```bash
dbt run
```

## Potential next steps

- Add unit tests
- Improvement of CI/CD pipeline
- Containerize the project
- Perform deeper data analysis
- Add pipeline for Machine Learning

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

dbt run --select global_terrorism_lite --vars '{"is_test_run": true}'
dbt run --select global_terrorism_lite --vars '{"is_test_run": false}'
dbt seed

prefect agent start -p 'default-agent-pool'
prefect deployment build -n "Online Parameterized ETL" -p default-agent-pool -q main-queue
src/flows/parameterized_flow_http_pipeline.py:end_to_end_pipeline_from_http_to_bq
prefect deployment apply end_to_end_pipeline_from_http_to_bq-deployment.yaml
