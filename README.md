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


# 📝 Project Workflow Summary

This project follows a structured approach to build a reliable data pipeline using Google Sheets, PostgreSQL, and Python.

---

## ✅ Steps Followed

1. **Google Sheets Setup**  
   First, I copied the original Google Sheet data into a new Google Sheet where I had the necessary permissions to use the **Google Sheets API**.

2. **Read Data via API**  
   Then, I used the **Google Sheets API** to read the data directly into my Python code.

3. **PostgreSQL Connection**  
   I created a client to connect to a **PostgreSQL** database from Python.

4. **Table Creation**  
   After setting up the database connection, I created the necessary **tables** in the PostgreSQL database.

5. **Data Ingestion**  
   Once the setup was done, I loaded the data from Google Sheets into those tables.

6. **Data Processing**  
   Finally, I wrote **SQL and Python** code to:
   - **Transform** the data (combine and clean it)
   - **Validate** it (check for data quality issues)
   - **Visualize** the results using charts and graphs
---

This end-to-end pipeline ensures automated ingestion, clean data, and meaningful insights.


# 📝 Additional Notes

### 📊 User Metrics Clarification

The project was expected to compute and visualize:

- **Total Users Over Time**: Users who sent or received a message
- **Active Users Over Time**: Users who sent a message (inbound direction)

However, after inspecting the data:
- All entries share the same `number_id`, indicating there is only **one unique user**.
- Given this, user-based metrics and visualizations were not meaningful or created, as they would not offer insights beyond a single user's activity.

---

### ⚙️ On the Use of PySpark

While **PySpark** was initially considered for this pipeline:

- The dataset is small and does not require distributed processing.
- Using Spark in this context would add unnecessary complexity without any real performance benefit.

In a **production environment**, Spark would be recommended for:
- Large-scale datasets
- Parallel processing of real-time or batch data
- Integration with distributed storage systems (e.g., HDFS, S3)

For this use case, **standard Python (pandas + SQL)** was optimal for both simplicity and performance.

---


