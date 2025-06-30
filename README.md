# 📊 Noora Health Data Pipeline

This project is an end-to-end data pipeline that extracts WhatsApp-based **message** and **status** data from Google Sheets, loads it into a **PostgreSQL** database, applies **data transformations** and **validations**, and generates insightful **visualizations** using `matplotlib` and `seaborn`.

---

## 📁 Project Structure

```
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
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/noora-project.git
cd noora-project
```

### 2. Add Credentials

Place your credentials inside the `config/` directory:

- `credentials.ini` — defines PostgreSQL and Google Sheets API credentials
- `key-<project>.json` — Google Service Account key file

---

## 🐳 Build and Start Docker

```bash
cd docker/
docker-compose up --build
```

This will:

- Set up a PostgreSQL instance
- Run a PySpark container with required dependencies

---

## 🧪 Run the Pipeline

You can execute the full pipeline using:

```bash
python pipelineRunner.py
```

This will:

- Create necessary PostgreSQL tables
- Ingest data from Google Sheets
- Transform and join the tables using SQL
- Run validation queries
- Generate summary visualizations

---

## 🛠 Technologies Used

- **Python 3.10**
- **PostgreSQL 14**
- **Docker + Docker Compose**
- `gspread` – for Google Sheets API integration
- `psycopg2` – for PostgreSQL DB interaction
- `pandas`, `matplotlib`, `seaborn` – for data processing and visualization

---
