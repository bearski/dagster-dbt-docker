## Stack

- Dagster
- dbt core
- Docker
- DuckDB
- Superset

## Setup

1. Create a `.env` file and set the following
    - PGUSER
    - POSTGRES_DB
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - SUPERSET_ADMIN
    - SUPERSET_PASSWORD

2. Run  `docker-compose up --build` from the root folder of the project.

3. Once the Docker suite has finished loading, open up [Dagster (dagit)](http://localhost:3000) , go to `Assets`, select all and click `Materialize selected`

4. When the assets have been materialized, go to the [Superset interface](http://localhost:8088)
