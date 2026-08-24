# Data Orchestration

Apache Airflow orchestration layer for the Data-Portfolio ETL and dataset generation pipeline.

This project runs the existing Data-Portfolio export pipeline through Apache Airflow without changing the core ETL logic.

## Architecture

```text
Data-Orchestration
        │
        │ Airflow DAG
        ▼
data_portfolio_export
        │
        │ calls
        ▼
Data-Portfolio
        │
        ├── SQL Server
        ├── PostgreSQL
        │
        ▼
Dataset Export
        │
        ├── CSV
        ├── JSON
        └── Parquet
```

The orchestration layer is responsible for scheduling and executing the existing Data-Portfolio pipeline.

The Data-Portfolio project remains responsible for database access, query execution, transformation, and dataset export.


## Requirements

- Docker Desktop
- Docker Compose
- Data-Portfolio repository

Expected directory structure:

```text
project-root/
├── data-orchestration/
└── data-portfolio/
```

The `data-orchestration` project expects the `data-portfolio` project to be located next to it.

The `Data-Portfolio` project is mounted into the Airflow container through Docker Compose.

## Start Airflow

Open PowerShell and navigate to the `data-orchestration` directory:

```powershell
cd D:\IMG-DE\data-orchestration
```

Start the Airflow environment:

```powershell
docker compose up -d
```

Check the container status:

```powershell
docker compose ps
```
The Airflow service should be running.

Airflow Web UI:
```
http://localhost:8080/
```

## Login to Airflow

Open the Airflow Web UI:

http://localhost:8080

The default username is:

```text
admin
```
If the password is not known, retrieve it from the Airflow logs:
```powershell
docker compose logs airflow | Select-String "password"
```
Use the password displayed in the logs to log in.

## Database Configuration

Data-Portfolio uses a separate database configuration for the Docker/Airflow environment.

The configuration file is:

```text
data-portfolio/config/db_config.data-portfolio.docker.json
```
This file contains the database connection settings used when Data-Portfolio runs inside the Airflow container.

For the local Docker environment, the database hosts are:

```
SQL Server:  host.docker.internal:1433
PostgreSQL:  host.docker.internal:5432
```

The Docker-specific configuration also contains the required SQL Server encryption and certificate settings for the local development environment.

The configuration is mounted into the Airflow container together with the Data-Portfolio project.

## Airflow DAG

The main DAG is:

```text
data_portfolio_export
```
The DAG is responsible for running the Data-Portfolio dataset generation process.

It is configured for manual execution and does not use a scheduled interval.

To run the DAG:

1. Open the Airflow Web UI.
2. Find `data_portfolio_export`.
3. Open the DAG.
4. Click **Trigger DAG**.
5. Monitor the execution from the DAG graph and task logs.

## Dataset Generation

The Data-Portfolio pipeline generates datasets from all configured export jobs.

The dataset builder can be executed from the command line:

```powershell
python .\powerbi\build_dataset.py
```

A specific output format can also be provided:

``` powershell
python .\powerbi\build_dataset.py csv
```

Supported output formats:

- CSV
- JSON
- Parquet

When executed through Airflow, the same dataset generation process is triggered by the data_portfolio_export DAG.


## Output

Generated datasets are stored in the `data` directory of the Data-Portfolio project.

Example:

```text
data-portfolio/
└── data/
    ├── orders_per_year.csv
    ├── top_actors_by_film_count.csv
    └── ...

```
The generated datasets can be used directly by Power BI or other downstream processes.

## Logs

Airflow task logs can be viewed directly from the Airflow Web UI.

Local Airflow logs are stored in:

```text
data-orchestration/logs/
```

## Stop Airflow

To stop the Airflow environment:

```powershell
docker compose down
```

To start it again:

```powershell
docker compose up -d
```

## Troubleshooting

### Airflow container is not running

Check the service status:

```powershell
docker compose ps
```

Start the environment if necessary:

```powershell
docker compose up -d
```

SQL Server connection timeout

Verify that SQL Server is running and port 1433 is available.

Test connectivity from the Airflow container:

```powershell
docker compose exec airflow python -c "import socket; print(socket.create_connection(('host.docker.internal',1433),5))"
```

PostgreSQL connection error

Verify that PostgreSQL is running and port 5432 is available.

Test connectivity from the Airflow container:
```powershell
docker compose exec airflow python -c "import socket; print(socket.create_connection(('host.docker.internal',5432),5))"
````

SQL Server ODBC Driver

Check the installed ODBC drivers:

```powershell
docker compose exec airflow python -c "import pyodbc; print(pyodbc.drivers())"
```
The output should include:

```
ODBC Driver 18 for SQL Server
```

## Development Notes

Airflow is used as the orchestration layer, while the Data-Portfolio project remains responsible for the ETL process.

The Data-Portfolio pipeline handles:

- Job configuration
- Database connections
- Query loading
- Data transformation
- Dataset export
- Logging

This separation allows the Data-Portfolio pipeline to run independently from Airflow.

## Cleanup

`HelloAirflow.py` was used during the initial Airflow setup and testing phase.

It is no longer required because the project now uses the `data_portfolio_export` DAG.

The test file can therefore be removed from the project.