# Data Engineering Captsone Project - Exploring Global Terrorism Dataset
![START_GTD-Heatmap_2020](https://user-images.githubusercontent.com/8614763/233846836-a3010a1b-bf1b-438d-9902-5436e5e30a54.jpg)

## Preface

This repository contains the course project for the Data Engineering Zoomcamp (Cohort 2023) organized by the by
DataTalks.Club community. The project covers main data engineering skills taught in the course:

- **Workflow Orchestration**: Data Lake, Prefect tool, ETL with GCP & Prefect
- **Data Warehouse**: BigQuery
- **Analytics engineering**: dbt (data build tool)
- **Data Analysis and visualisation**: Looker Studio

<b>TL;DR</b>: This project is analyzing the Global terrorism Dataset. Follow the steps mentioned
under `How to reproduce this project?` to set it up.

## Dataset description

### Global Terrorism Dataset

The data has been downloaded from the [Global Terrorism Database (GTD)](https://www.start.umd.edu/gtd/)

The Global Terrorism Database™ (GTD) is an open-source database including information on terrorist events around the
world **from 1970 through 2021** (with annual updates planned for the future). Unlike many other event databases, the GTD
includes systematic data on domestic as well as international terrorist incidents that have occurred during this time
period and now includes more than 200,000 cases.

**Characteristics of the GTD**

- 1970 to 2021 data
- Contains information on over 200,000 terrorist attacks
- Currently the most comprehensive unclassified database on terrorist attacks in the world
- Includes information on more than 88,000 bombings, 19,000 assassinations, and 11,000 kidnappings since 1970
- Includes information on at least 45 variables for each case, with more recent incidents including information on more than 120 variables
- More than 4,000,000 news articles and 25,000 news sources were reviewed to collect incident data from 1998 to 2017 alone


### Dataset Structure

The dataset has about 120 columns, but for the present project I decided to select only the relevant columns for my analysis (27 in total). The following columns will be used:
<div align="center">

| #  | Attribute             |                     Description                                      |
|:--:|:---------------------:|----------------------------------------------------------------------|
|  1 | **event_id**                | This is a unique identifier of the terrorism attack record.                  |
|  2 | **event_date**          | Reconstruction of the date from attributes: year, month, day.        |
|  3 | **country**        | the country or location where the incident occurred.             |
|  4 | **region**          | the region in which the incident occurred.                       |
|  5 | **provstate**       |  the name (at the time of event) of the 1st order subnational administrative region in which the event occurs.	            |
|  6 | **city**            | the name of the city, village, or town in which the incident occurred.	                            |
|  7 | **summary**              | A brief narrative summary of the incident, noting the “when, where, who, what, how, and why.”.	                                    |
|  8 | **reason1**             | The violent act must be aimed at attaining a political, economic, religious, or social goal.	                                  |
|  9 | **reason2**           | To satisfy this criterion there must be evidence of an intention to coerce, intimidate, or convey some other message to a larger audience (or audiences) than the immediate victims.                                  |
| 10 | **reason3** | The action is outside the context of legitimate warfare activities, insofar as it targets non-combatants 	  |
| 11 | **doubt_terrorism_proper**    | In certain cases there may be some uncertainty whether an incident meets all of the criteria for inclusion.	|
| 12 | **attack_type**    | the general method of attack and often reflects the broad class of tactics used.	|
| 13 | **target_type**    | captures the general type of target/victim.	|
| 14 | **weapon_type**    | the general type of weapon used in the incident.	|
| 15 | **perpetrator_group_name**    | the name of the group that carried out the attack.	|
| 16 | **nkill**    | the number of total confirmed fatalities for the incident.	|
| 17 | **nwound**    | the number of confirmed non-fatal injuries to both perpetrators and victims.	|

</div>

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

## Data visualization: Dashboards

<img width="686" alt="Exemple Dashboard" src="https://user-images.githubusercontent.com/8614763/233846604-575afffe-083a-41d9-aa77-4bbac33cc0c5.png">


### What questions am I trying to answer?

- Which countries have had the most attacks?
- Which cities have had the most attacks?
- What is the most common type of attack?
- What are the main reasons for these attacks?
- What are the main targets?
- Who are the main perpetrators?
- The total number of deaths since the beginning
- The number of deaths per country


[Click here](https://lookerstudio.google.com/reporting/5436069c-3071-4119-88b0-dc0a27c547ff) to see the
dashboard.

## How to reproduce this project?

**Step 1: Clone this repo and install necessary requirements**

1. Clone the repo into your local machine:
```bash
git clone https://github.com/lironesamoun/data-engineering-capstone-project.git
```
2. Create a virtual env and install all required dependencies into your environment
```bash
make install
```

#### Step 2: Setup of GCP
1. Create a [Google Cloud Platform (GCP)](https://cloud.google.com/) free account with your Google e-mail
2. Create a new GCP project with the name **de-capstone-project-23** (Note: Save the assigned Project ID. Projects have a unique ID and for that reason another ID will be assigned)
3. Create a Service Account:
    - Go to **IAM & Admin > Service accounts > Create service account**
    - Provide a service account name and grant the roles: **Viewer** + **BigQuery Admin** + **Storage Admin** + **Storage Object Admin** + **Compute Storage Admin**
    - Download the Service Account json file
    - Download [SDK](https://cloud.google.com/sdk/docs/install-sdk) for local setup
    - Set environment variable to point to your downloaded GCP keys in the .env file:
    ```bash
    TF_VAR_GCP_CREDS="<path/to/your/service-account-authkeys>.json"
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
2. Execute the following commands to plan the creation of the GCP infrastructure:
```bash
make init-infrastructure
```

It is possible to see in the GCP console that the Infrastructure was correctly created.

At the end of the process, you should see the bucket created and the table in Google Big Query.
You can change the name of the variable inside the .env file.


#### Step 4: Setup orchestration using Prefect
1. Setup the prefect server so that you can access the UI. Run the following command in a CL terminal:
```bash
make prefect-init
make prefect-start
 ```
2. Access the UI in your browser: **http://127.0.0.1:4200/**
3. For the connection with GCP Buckets it is necessary to init prefect blocks

Fill in the github env variable:
```bash
GITHUB_REPOSITORY_URL="your repo"
GITHUB_REPO_ACCESS_TOKEN=""
 ```

Then:
```bash
make prefect-init-blocks
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
dbt run --vars 'is_test_run: false'
```
You should see the following lineage in DBT:
<img width="1071" alt="DBT Lineage" src="https://user-images.githubusercontent.com/8614763/233846665-ea2e175b-59d5-4f55-98c3-7904bf2a0e60.png">

#### Step 5b: Running the dbt flow on Production

Create a production environment on DBT.
Add the following command:

```bash
dbt seed
dbt build --vars 'is_test_run: false'
dbt test
```

Execute the flow.

After running all those steps, you should see in Google Big query the following table created
<img width="657" alt="Table created in Google Big Query" src="https://user-images.githubusercontent.com/8614763/233846616-1133fdee-dab7-4b0f-bb75-d259de2fee68.png">


#### (Optional) Uninstall
```bash
make destroy-infrastructure
make uninstall
```

## Potential next steps

- Add unit tests
- Improvement of CI/CD pipeline
- Containerize the project
- Perform deeper data analysis
- Add pipeline for Machine Learning


##### Memento
prefect agent start -p 'default-agent-pool'
prefect deployment build -n "Online Parameterized ETL" -p default-agent-pool -q main-queue
src/flows/parameterized_flow_http_pipeline.py:end_to_end_pipeline_from_http_to_bq
prefect deployment apply end_to_end_pipeline_from_http_to_bq-deployment.yaml