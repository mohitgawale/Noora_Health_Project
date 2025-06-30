WhatsApp Data Pipeline
This project is an end-to-end data pipeline that extracts WhatsApp-based message and status data from Google Sheets, loads it into a PostgreSQL database, applies data transformations and validations, and produces insightful visualizations using matplotlib and seaborn.
📁 Project Structure
Noora_Health_Main/
│
├── config/
│   ├── credentials.ini               # GDrive and PostgreSQL credentials
│   └── key-<gdrive>.json             # Google Service Account key
│
├── docker/
│   ├── Dockerfile                    # Docker setup for PySpark + Java
│   ├── docker-compose.yml           # Docker Compose for PostgreSQL + app
│   └── requirements.txt             # Python package requirements
│
├── utils/
│   └── client.py                     # GoogleSheetClient & PostgresClient classes
│
├── src/
│   ├── create_table.py               # PostgreSQL table creation logic
│   ├── ingest_data.py                # Loads data from Google Sheets to DB
│   ├── transform.py                  # SQL-based data transformation
│   ├── validation.py                 # Data quality checks
│   └── visualization.py             # Generates charts with matplotlib/seaborn
│
├── pipelineRunner.py                # Main script to orchestrate the full pipeline
└── README.md
🚀 Getting Started
1. Clone the Repository
bashgit clone https://github.com/your-org/noora-project.git
cd noora-project
2. Add Credentials
Place your credentials inside the config/ directory:

credentials.ini — defines DB and Google credentials
key-<project>.json — Google service account key

3. Build and Start Docker
bashcd docker/
docker-compose up --build
This will:

Set up a PostgreSQL instance
Run a PySpark container with required dependencies

🧪 Run the Pipeline
You can run the full pipeline using:
bashpython pipelineRunner.py
This will:

Create tables
Ingest data from Google Sheets
Transform and join the tables
Run validation queries
Generate charts

🛠 Technologies Used

Python 3.10 - Core programming language
PostgreSQL 14 - Database for storing processed data
Docker + Docker Compose - Containerization and orchestration
gspread - Google Sheets integration
psycopg2 - PostgreSQL database interaction
pandas - Data processing and manipulation
matplotlib & seaborn - Data visualization
PySpark - Big data processing (when needed)

📋 Pipeline Components
Data Extraction

Connects to Google Sheets using service account credentials
Extracts WhatsApp message and status data

Data Loading

Creates PostgreSQL tables with appropriate schema
Loads raw data into staging tables

Data Transformation

Applies SQL-based transformations
Joins multiple data sources
Cleans and standardizes data formats

Data Validation

Performs data quality checks
Validates data integrity and completeness
Generates validation reports

Data Visualization

Creates insightful charts and graphs
Generates reports using matplotlib and seaborn
Exports visualizations for stakeholders

🔧 Configuration
Database Configuration
Configure your PostgreSQL connection in config/credentials.ini:
ini[database]
host = localhost
port = 5432
database = your_db_name
username = your_username
password = your_password
Google Sheets Configuration

Create a Google Service Account
Download the JSON key file
Place it in config/ directory as key-<project>.json
Share your Google Sheets with the service account email

📊 Output
The pipeline generates:

Cleaned and transformed data in PostgreSQL
Data quality validation reports
Interactive visualizations and charts
Summary statistics and insights

🐳 Docker Setup
The project includes a complete Docker setup:

Dockerfile: Contains PySpark and Java dependencies
docker-compose.yml: Orchestrates PostgreSQL and application containers
requirements.txt: Python package dependencies
