Noora_Health_Main/
│
├── config/
│   ├── credentials.ini               # GDrive and PostgreSQL credentials
│   └── key-<gdrive>.json             # Google Service Account key
│
├── docker/
│   ├── Dockerfile                    # Docker setup for PySpark + Java
│   ├── docker-compose.yml            # Docker Compose for PostgreSQL + app
│   └── requirements.txt              # Python package requirements
│
├── utils/
│   └── client.py                     # GoogleSheetClient & PostgresClient classes
│
├── src/
│   ├── create_table.py               # PostgreSQL table creation logic
│   ├── ingest_data.py                # Loads data from Google Sheets to DB
│   ├── transform.py                  # SQL-based data transformation
│   ├── validation.py                 # Data quality checks
│   └── visualization.py              # Generates charts with matplotlib/seaborn
│
├── pipelineRunner.py                 # Main script to orchestrate the full pipeline
└── README.md
